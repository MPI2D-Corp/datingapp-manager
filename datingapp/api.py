import requests as re
from datingapp.entity import User, Role, Interest
import os
import base64
import json
import time
from datingapp import cache

baseurl = ""
token_file = ""
user = None
session = re.Session()
authenticated = False


def init(url, cache_directory) -> bool:
    """
    Initialise the API and try to login if a token was saved
    :param url: The base url of the api (without the trailing slash)
    :param cache_directory: The path to the cache directory (where the auth token is saved)
    :return: True if the api could authenticate with the saved token
    """
    global baseurl, token_file, session, user, authenticated

    token_file = cache_directory + "auth_token"
    baseurl = url

    __init_session()

    # Try to connect if a token was saved
    if os.path.exists(token_file):
        print("Trying to login with saved token ...")
        with open(token_file, "r") as f:
            token = f.read()

        # Get the expiration time and the user id
        try:
            payload = json.loads(base64.urlsafe_b64decode(token.split(".")[1]))
            exp = payload["exp"]
            user_id = int(payload["sub"])

        except Exception :
            # Invalid token
            print("Could not login with saved token : Malformed token")
            os.remove(token_file)
            return False

        # Expired token
        if exp < time.time():
            os.remove(token_file)
            print("Could not login with saved token : Expired token")
            return False
        
        # Check if the token is still valid

        session.headers["Authorization"] = f"Bearer {token}"
        try:
            user = get_user(user_id)

        except Exception:
            os.remove(token_file)
            user = None
            session.headers["Authorization"] = None
            print("Could not login with saved token : Invalid token")
            return False

        print("Successfully logged in with saved token !")

        authenticated = True
        cache.save_user(user)
        return True


def __init_session():
    global session, authenticated
    session = re.Session()
    session.hooks["response"].append(__unauthenticated_error_hook)
    authenticated = False


# Utilisée pour signaler que le token d'authentification n'est plus valide
class AuthenticationError(RuntimeError):
    pass


def __unauthenticated_error_hook(r: re.Response, *args, **kwargs):
    global authenticated

    if r.status_code == 401:
        authenticated = False
        raise AuthenticationError

    if r.status_code == 403:
        raise RuntimeError("Erreur 403 : vous n'avez pas accès à la ressource demandée")

    return r


def login(username, password, rememberme=False):
    global session, user, authenticated

    # Close the current session if open
    if session is not None:
        session.close()

    __init_session()

    payload = {"username": username, "password": password}

    if rememberme:
        payload["expiration"] = 1000 * 60 * 60 * 24 * 30    # 30 days

    # Authenticate with the given credentials
    r = session.post(baseurl + "/auth/signin", json=payload)

    if r.status_code == 400 or r.status_code != 200:

        msg = r.json().get("message")
        if msg is None:
            msg = r.json().get("error")
        if msg is None:
            msg = r.json()

        raise RuntimeError("Erreur lors de l'authentification : \n{}".format(msg))

    data = r.json()

    session.headers["Authorization"] = f"{data['type']} {data['token']}"

    user = User(**data["user"])
    
    cache.save_user(user)

    authenticated = True

    if rememberme:
        with open(token_file, "w") as f:
            f.write(data["token"])


def get_users():

    r = session.get(f"{baseurl}/users?size=150")

    if r.status_code != 200:
        raise RuntimeError("Erreur lors de la récupération de la liste des utilisateurs : \n{}".format(r.content))

    nb_pages = r.json()["totalPages"]

    users = [User(**u) for u in r.json()["content"]]

    # Get other pages
    for page_nb in range(1, nb_pages):

        r = session.get(f"{baseurl}/users?size=150&page={page_nb}")

        if r.status_code != 200:
            raise RuntimeError(
                "Erreur lors de la récupération de la liste des utilisateurs {} : \n{}".format(id, r.content))

        users += [User(**u) for u in r.json()["content"]]


    return users


def get_user(id):

    r = session.get(f"{baseurl}/users/{id}")

    if r.status_code == 404:
        return None

    if r.status_code != 200:
        raise RuntimeError("Erreur lors de la récupération de l'utilisateur {} : \n{}".format(id, r.content))

    return User(**r.json())


def save_user(user):
    
    r = session.put(f"{baseurl}/users/{user.id}", json=user.json())

    if r.status_code == 404:
        raise RuntimeError(f"Erreur lors de la sauvegarde de l'utilisateur {user.id} : L'utilisateur n'existe pas.")

    if r.status_code == 400:
        raise RuntimeError(f"Erreur lors de la sauvegarde de l'utilisateur {user.id} : {r.content}")

    if r.status_code != 200:
        raise RuntimeError(f"Erreur lors de la sauvegarde de l'utilisateur {user.id} : {r.content}")

    cache.save_user(user)


def delete_user(id):
    
    r = session.delete(f"{baseurl}/users/{id}")

    if r.status_code != 200:
        raise RuntimeError(f"Erreur lors de la suppression de l'utilisateur {user.id} : {r.content}")

    cache.delete_user(id)


def save_user_roles(id, roles):
    
    r = session.put(f"{baseurl}/users/{id}/roles", json=list(roles))

    if r.status_code != 200:
        raise RuntimeError(f"Erreur lors de la sauvegarde des rôles l'utilisateur {id} : {r.content}")

    cache.save_user_roles(id, roles)


def get_role(id):

    r = session.get(f"{baseurl}/roles/{id}")

    if r.status_code == 404:
        return None

    if r.status_code != 200:
        raise RuntimeError("Erreur lors de la récupération du rôle {} : \n{}".format(id, r.content))

    return Role(**r.json()[0])


def get_profile_picture(id):

    r = session.get(f"{baseurl}/users/{id}/profile-picture")

    if r.status_code == 404:
        return None

    if r.status_code != 200:
        raise RuntimeError("Erreur lors de la récupération de l'image de profil {} : \n{}".format(id, r.content))

    return r.content


def get_settings(id):

    r = session.get(f"{baseurl}/users/{id}/settings")

    if r.status_code != 200:
        raise RuntimeError("Erreur lors de la récupération des paramètres {} : \n{}".format(id, r.content))

    return r.json()


def save_settings(id, settings):

    r = session.put(f"{baseurl}/users/{id}/settings", json=settings)

    if r.status_code != 200:
        raise RuntimeError("Erreur lors de la sauvegarde des paramètres {} : \n{}".format(id, r.content))

    cache.save_settings(id, settings)


def get_user_interests(id):

    r = session.get(f"{baseurl}/users/{id}/interests")

    if r.status_code != 200:
        raise RuntimeError("Erreur lors de la récupération de la liste des intérêts de l'utilisateur {} : \n{}".format(id, r.content))

    interests = []
    important = []
    
    for i in r.json():

        interests.append(i["interest"]["id"])

        if i["important"]:
            important.append(i["interest"]["id"])

    return interests, important


def save_user_interests(id, interests):

    r = session.get(f"{baseurl}/users/{id}/interests", json=interests)

    if r.status_code != 200:
        raise RuntimeError("Erreur lors de la sauvegarde des intérêts de l'utilisateur {} : \n{}".format(id, r.content))

    cache.update_user_interests(id, interests)


def save_user_important_interests(id, important_interests):

    r = session.get(f"{baseurl}/users/{id}/interests/important", json=important_interests)

    if r.status_code != 200:
        raise RuntimeError("Erreur lors de la sauvegarde des intérêts de l'utilisateur {} : \n{}".format(id, r.content))

    cache.update_user_important_interests(id, important_interests)


#
#   Roles
#

def get_roles():

    r = session.get(f"{baseurl}/roles")

    if r.status_code != 200:
        raise RuntimeError("Erreur lors de la récupération de la liste des rôles : \n{}".format(r.content))

    roles = [Role(**ro) for ro in r.json()]

    return roles


def update_role(role):

    r = session.put(f"{baseurl}/roles/{role.id}", json=role.__dict__)

    if r.status_code != 200:
        raise RuntimeError("Erreur lors de la mise à jour du rôle {} : \n{}".format(role, r.content))

    cache.update_role(role)


def delete_role(role):

    r = session.delete(f"{baseurl}/roles/{role.id}", json=role.__dict__)

    if r.status_code != 200:
        raise RuntimeError("Erreur lors de la suppression du rôle {} : \n{}".format(role, r.content))

    cache.delete_role(role)


def create_role(role):

    r = session.post(f"{baseurl}/roles", json=role.__dict__)

    if r.status_code != 201:
        raise RuntimeError("Erreur lors de la création du rôle {} : \n{}".format(role, r.content))

    ro = Role(**r.json())

    cache.update_role(ro)


#
#   Interests
#

def get_interests():

    r = session.get(f"{baseurl}/interests?showWeight=true")

    if r.status_code != 200:
        raise RuntimeError("Erreur lors de la récupération de la liste des intérêts : \n{}".format(r.content))

    interests = [Interest(**ro) for ro in r.json()]

    return interests


def get_interest(id):
    r = session.get(f"{baseurl}/interests/{id}")

    if r.status_code == 404:
        return None

    if r.status_code != 200:
        raise RuntimeError("Erreur lors de la récupération de l'intérêt {} : \n{}".format(id, r.content))

    interest = Interest(**r.json())

    return interest


def update_interest(interest):
    
    r = session.put(f"{baseurl}/interests/{interest.id}", json=interest.__dict__)
    
    if r.status_code != 200:
        raise RuntimeError("Erreur lors de la récupération de l'intérêt {} : \n{}".format(interest.id, r.content))
    
    cache.update_interest(interest)


def create_interest(interest):
    r = session.post(f"{baseurl}/interests", json=interest.__dict__)

    if r.status_code != 201:
        raise RuntimeError("Erreur lors de la création de l'intérêt {} : \n{}".format(interest.id, r.content))

    interest = Interest(**r.json())

    cache.update_interest(interest)


def delete_interest(interest):

    r = session.delete(f"{baseurl}/interests/{interest.id}")

    if r.status_code != 200:
        raise RuntimeError("Erreur lors de la suppression de l'intérêt {} : \n{}".format(interest.id, r.content))

    cache.delete_interest(interest)
