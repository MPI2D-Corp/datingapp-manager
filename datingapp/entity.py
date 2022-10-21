
PRIVILEGES = [
    "LIST_USERS",
    "VIEW_USER",
    "VIEW_USER_OTHER",
    "VIEW_PROFILE",
    "VIEW_PROFILE_OTHER",
    "EDIT_USER",
    "EDIT_USER_OTHER",
    "EDIT_USER_PROTECTED",
    "DELETE_USER",
    "DELETE_USER_OTHER",
    "VIEW_USER_SETTINGS",
    "VIEW_USER_SETTINGS_OTHER",
    "EDIT_USER_SETTINGS",
    "EDIT_USER_SETTINGS_OTHER",
    "LIST_ROLES",
    "VIEW_ROLE",
    "EDIT_ROLE",
    "CREATE_ROLE",
    "DELETE_ROLE",
    "LIST_ROLE_USERS",
    "VIEW_USER_ROLES",
    "EDIT_USER_ROLES",
    "VIEW_INTEREST_WEIGHT",
    "CREATE_INTEREST",
    "EDIT_INTEREST",
    "DELETE_INTEREST",
    "VIEW_USER_INTERESTS",
    "VIEW_USER_INTERESTS_OTHER",
    "USE_MATCHING",
    "LIST_CONVERSATIONS",
    "VIEW_CONVERSATION_OTHER",
    "CREATE_CONVERSATION",
    "DELETE_CONVERSATION",
    "BYPASS_CLOSED_CONVERSATION",
    "VIEW_USER_CONVERSATIONS",
    "SEND_SPECIAL_MESSAGES"
]

PRIVILEGES.sort()

FILIERES = [
    "MP2I",
    "MPSI",
    "PCSI",
    "PTSI",
    "HK",
    "BCPST",
    "MP",
    "MPI",
    "PC",
    "PT",
    "PSI",
    "K",
    "ECG",
    "BIO",
    "Autre"
]

DEFAULT_SETTINGS = {'lastNamePublic': False, 'filierePublic': False, 'birthdayPublic': False, 'agePublic': False,
                    'sexPreferences': [], 'profileHidden': False}


class User:

    def __init__(self, id, email, username, firstName, lastName, filiere, birthday, sex, bio, hasProfilePicture, expired, enabled, locked, emailVerified, registerDate, roles, firebaseTokens, displayName, profilePicture):

        self.displayName = displayName
        self.registerDate = registerDate
        self.emailVerified = emailVerified
        self.locked = locked
        self.enabled = enabled
        self.expired = expired
        self.hasProfilePicture = hasProfilePicture
        self.bio = bio
        self.sex = sex
        self.birthday = birthday
        self.filiere = filiere
        self.lastName = lastName
        self.firstName = firstName
        self.username = username
        self.profilePicture = profilePicture
        self.email = email
        self.id = id

        self.firebaseTokens = firebaseTokens

        self.roles = set([role["id"] for role in roles])

    def __eq__(self, other):

        if other is None or type(other) != type(self):
            return False

        return self.__dict__ == other.__dict__

    def json(self):
        json = self.__dict__.copy()
        if self.filiere == "":
            json.pop("filiere")
        for k, v in json.items():
            if type(v) == str and v == "":
                json[k] = None
        json.pop("roles")
        return json


class Role:

    def __init__(self, id, name, displayName, privileges):
        self.privileges = privileges
        self.displayName = displayName
        self.name = name
        self.id = id


class Interest:

    INTEREST_TYPES = [
        "CENTRE_OF_INTEREST",
        "HOBBY"
    ]

    def __init__(self, id, name, weight, type):
        self.type = type
        self.weight = weight
        self.name = name
        self.id = id
