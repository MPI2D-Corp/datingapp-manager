from datingapp import api
import pickle
import os
import time

"""Temps de validité du cache des utilisateurs en secondes"""
USER_CACHE_EXPIRATION = 3600
PROFILE_PICTURE_CACHE_EXPIRATION = 3600 * 24

PROFILE_PIC_FOLDER = "profile-pic/"

# Contient des tuples (user, timestamp)
# avec timestamp le timestamp de la récupération de l'utilisateur depuis le serveur
user_cache = {}
settings_cache = {}
user_interest_cache = {}
profile_picture_cache = {}
roles_cache = {}
interest_cache = {}

__loaded_role_list = False
__loaded_user_list = False
__loaded_user_list_timestamp = 0
__loaded_interest_list = False


def init(cache_directory):
    global PROFILE_PIC_FOLDER
    PROFILE_PIC_FOLDER = cache_directory + PROFILE_PIC_FOLDER

    if not os.path.exists(PROFILE_PIC_FOLDER):
        os.makedirs(PROFILE_PIC_FOLDER)


#
#   Users
#

def get_users():
    global __loaded_user_list, __loaded_user_list_timestamp

    if len(user_cache) > 0 and __loaded_user_list and __loaded_user_list_timestamp + USER_CACHE_EXPIRATION >= time.time():
        users = [user for user, _ in user_cache.values()]
        return users

    users = api.get_users()
    for u in users:
        save_user(u)

    __loaded_user_list = True
    __loaded_user_list_timestamp = time.time()
    return users


def get_user(id):

    try:
        cached = user_cache[id]
    except KeyError:
        cached = (None, - USER_CACHE_EXPIRATION - 1)

    user = cached[0]
    timestamp = cached[1]

    if timestamp + USER_CACHE_EXPIRATION < time.time():

        user = api.get_user(id)

        if user is None:
            raise RuntimeError(f"L'utilisateur d'id {id} n'existe pas.")

        user_cache[id] = (user, time.time())

    return user


def save_user(user):
    user_cache[user.id] = (user, time.time())


def delete_user(id):
    user_cache.pop(id)


def get_profile_picture(id):

    picfile = f"{PROFILE_PIC_FOLDER}/{id}"
    cached = os.path.isfile(picfile)

    if cached:
        with open(picfile, "rb") as f:
            timestamp, pic = pickle.load(f)

        if timestamp + PROFILE_PICTURE_CACHE_EXPIRATION >= time.time():
            return pic

    pic = api.get_profile_picture(id)

    if pic is None:
        return None

    with open(f"{PROFILE_PIC_FOLDER}/{id}", "wb") as f:
        pickle.dump((time.time(), pic), f)

    profile_picture_cache[id] = time.time()

    return pic


def get_settings(id):
    try:
        settings, timestamp = settings_cache[id]
    except KeyError:
        settings, timestamp = (None, None)

    if timestamp is not None and timestamp + USER_CACHE_EXPIRATION >= time.time():
        return settings

    settings = api.get_settings(id)

    if settings is None:
        raise RuntimeError(f"Les paramètres de l'utilisateur d'id {id} n'existent pas.")

    settings_cache[id] = (settings, time.time())

    return settings


def save_settings(id, settings):
    settings_cache[id] = (settings, time.time())


def save_user_roles(id, roles):
    user_cache[id][0].roles = roles.copy()


def get_user_interests(id):

    try:
        interest, important, timestamp = user_interest_cache[id]
    except KeyError:
        interest, important, timestamp = (None, None, None)

    if timestamp is not None and timestamp + USER_CACHE_EXPIRATION >= time.time():
        return interest, important

    interest, important = api.get_user_interests(id)

    if interest is None:
        raise RuntimeError(f"Les intérêts de l'utilisateur d'id {id} n'existent pas.")

    user_interest_cache[id] = (interest, important, time.time())

    return interest, important


def save_user_interests(id, interests, important):
    user_interest_cache[id] = (interests, important, time.time())


def update_user_interests(id, interests):
    _, important, t = user_interest_cache[id]
    user_interest_cache[id] = (interests, important, t)


def update_user_important_interests(id, important_interests):
    interests, _, t = user_interest_cache[id]
    user_interest_cache[id] = (interests, important_interests, t)


#
#   Roles
#

def get_roles():
    global __loaded_role_list

    if len(roles_cache) > 0 and __loaded_role_list:
        return list(roles_cache.values())

    roles = api.get_roles()
    update_roles(roles)

    __loaded_role_list = True

    return roles


def update_role(role):
    roles_cache[role.id] = role


def update_roles(roles):

    for role in roles:
        update_role(role)


def get_role(id):

    try:
        return roles_cache[id]

    except KeyError:

        role = api.get_role(id)

        if role is None:
            raise RuntimeError(f"Le rôle d'id {id} n'existe pas.")

        update_role(role)

        return role


def delete_role(role):
    try:
        roles_cache.pop(role.id)
    except KeyError:
        pass


#
#   Interests
#

def get_interests():
    global __loaded_interest_list

    if len(interest_cache) > 0 and __loaded_interest_list:
        return list(interest_cache.values())

    interests = api.get_interests()
    update_interests(interests)

    __loaded_interest_list = True

    return interests


def get_interest(id):
    try:
        return interest_cache[id]

    except KeyError:

        interest = api.get_interest(id)

        if interest is None:
            raise RuntimeError(f"L'intérêt' d'id {id} n'existe pas.")

        update_interest(interest)

        return interest


def update_interests(interests):
    for i in interests:
        update_interest(i)


def update_interest(interest):
    interest_cache[interest.id] = interest


def delete_interest(interest):
    interest_cache.pop(interest.id)
