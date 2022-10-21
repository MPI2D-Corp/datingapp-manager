from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QDoubleValidator
from copy import copy
from datingapp import api, cache
from datingapp.ui.views.login import Ui_LoginDialog
from datingapp.ui.views.rolescreen import Ui_RoleScreen
from datingapp.ui.views.userscreen import Ui_UserScreen
from datingapp.ui.views.userdialog import Ui_UserDialog
from datingapp.ui.views.interestscreen import Ui_InterestScreen
from datingapp.entity import PRIVILEGES, Role, FILIERES, DEFAULT_SETTINGS, Interest


def _init_checkbox_list(parent: QtWidgets.QWidget, objects, key_func, name_func, foreach_func=None):
    """
    Initialise un widget avec des checkbox correspondant à des objets. Renvoie un dictionnaire dont les clés sont
    données par `key_func(obj)`, et les valeurs les checkbox correspondantes. Le nom des checkbox est déterminé
    par `name_func(obj)`. Optionnellement, on peut passer une fonction `foreach_func(obj, checkbox)` qui sera appelée
    sur chacune des checkbox
    :param parent: Le Widget parent des checkbox. Doit contenir un layout.
    :param objects: Une liste d'objets
    :param key_func: La fonction qui associe un objet à une clé pour le dictionnaire
    :param name_func: La fonction qui donne le texte à afficher pour un objet
    :param foreach_func: Une fonction appelée pour chaque checkbox
    :return:Un dictionnaire contenant toutes les checkbox ajoutées
    """
    checkboxes = {}

    i = 0
    for o in objects:

        checkbox = QtWidgets.QCheckBox(parent)
        checkbox.setText(name_func(o))

        if foreach_func is not None:
            foreach_func(o, checkbox)

        parent.layout().addWidget(checkbox)

        checkboxes[key_func(o)] = checkbox

        i += 1

    spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
    parent.layout().addItem(spacerItem)

    return checkboxes


class LoginDialog(QtWidgets.QMainWindow, Ui_LoginDialog):

    def __init__(self):
        super(LoginDialog, self).__init__()
        self.setupUi(self)
        self.login_button.clicked.connect(self.login)

    def login(self):

        username = self.username.text()
        password = self.password.text()

        if username is None or password is None or username == "" or password == "":
            return

        try:
            api.login(username, password, rememberme=self.rememberCheckbox.isChecked())
        except RuntimeError as e:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)

            msgBox.setWindowTitle("Erreur")
            msgBox.setText(str(e))

            msgBox.exec_()

        if api.authenticated:
            self.close()


class RoleScreen(QtWidgets.QWidget, Ui_RoleScreen):

    def __init__(self):
        super(RoleScreen, self).__init__()
        self.setupUi(self)

        # Set table header width
        self.roleTable.setColumnWidth(0, 50)
        self.roleTable.setColumnWidth(1, 200)
        self.load_data()

        # Init role widget
        self.__init_privileges_list()
        self.editing_role = False
        self.creating_role = False

        self.__init_connections()

        self.roleTable.selectRow(0)
        self.load_role()

    def __init_privileges_list(self):

        key_func = lambda p: p
        foreach_func = lambda o, c: c.setEnabled(False)

        self.privileges_checkboxes = _init_checkbox_list(self.privileges_scroll_area_content, PRIVILEGES, key_func, key_func, foreach_func=foreach_func)

    def __init_connections(self):

        self.roleTable.itemSelectionChanged.connect(self.load_role)
        self.edit_button.clicked.connect(self.edit_role)
        self.save_button.clicked.connect(self.save_role)
        self.create_button.clicked.connect(self.create_role)
        self.delete_button.clicked.connect(self.delete_role)

    def load_role(self):

        if self.creating_role:
            role = Role(None, "", "", [])
        else:
            role = self.current_role()

        self.id_text.setText(str(role.id))
        self.name_field.setText(role.name)
        self.displayname_field.setText(role.displayName)

        for c in self.privileges_checkboxes.values():
            c.setChecked(False)

        for p in role.privileges:
            self.privileges_checkboxes[p].setChecked(True)

    def current_role(self):
        role_id = int(self.roleTable.item(self.roleTable.currentRow(), 0).text())

        return cache.get_role(role_id)

    def load_data(self):

        roles = cache.get_roles()

        if len(roles) <= 0:
            self.delete_button.setEnabled(False)
        else:
            self.delete_button.setEnabled(True)

        row = 0
        self.roleTable.setRowCount(len(roles))
        for role in roles:
            self.roleTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(role.id)))
            self.roleTable.setItem(row, 1, QtWidgets.QTableWidgetItem(role.name))
            self.roleTable.setItem(row, 2, QtWidgets.QTableWidgetItem(role.displayName))
            row += 1

    def _update_role(self):
        """Update the role at the current row"""

        role = self.current_role()

        row = self.roleTable.currentRow()
        self.roleTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(role.id)))
        self.roleTable.setItem(row, 1, QtWidgets.QTableWidgetItem(role.name))
        self.roleTable.setItem(row, 2, QtWidgets.QTableWidgetItem(role.displayName))

    def __update_enabled(self):
        edit = self.editing_role

        self.save_button.setEnabled(edit)
        self.name_field.setEnabled(edit)
        self.displayname_field.setEnabled(edit)
        self.roleTable.setEnabled(not edit)
        self.create_button.setEnabled(not edit)
        self.delete_button.setEnabled(not edit)

        for c in self.privileges_checkboxes.values():
            c.setEnabled(edit)

    def edit_role(self):

        self.editing_role = not self.editing_role
        self.__update_enabled()

        if self.editing_role:
            self.edit_button.setText("Annuler")
        else:
            self.creating_role = False
            self.load_role()
            self.edit_button.setText("Modifier")

    def save_role(self):

        if not self.editing_role:
            return

        if self.creating_role:
            role = Role(-1, "", "", [])
        else:
            role = self.current_role()

        role.name = self.name_field.text()
        role.displayName = self.displayname_field.text()

        privileges = []
        for p, c in self.privileges_checkboxes.items():
            if c.isChecked():
                privileges.append(p)

        role.privileges = privileges

        try:
            if self.creating_role:
                api.create_role(role)
            else:
                api.update_role(role)

        except RuntimeError as e:

            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)

            msgBox.setWindowTitle("Erreur")
            msgBox.setText("Impossible d'enregistrer les changements")
            msgBox.setInformativeText(str(e))

            msgBox.exec_()

            return

        self.editing_role = False
        self.edit_button.setText("Modifier")
        self.__update_enabled()

        if self.creating_role:
            self.load_data()
            self.creating_role = False

        self.load_role()
        self._update_role()

    def delete_role(self):

        if self.editing_role or self.creating_role or self.roleTable.currentRow() < 0:
            return

        role = self.current_role()

        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)

        msgBox.setWindowTitle(f"Supprimer {role.displayName} ?")
        msgBox.setText("Êtes-vous sûr de vouloir supprimer le rôle {} ?".format(role.name))
        msgBox.setInformativeText("Si vous supprimez un rôle auquel vous appartenez, vous risquez de perdre l'accès aux fonctions d'administration.")

        choice = msgBox.exec_()

        if choice == QtWidgets.QMessageBox.StandardButton.Cancel:
            return

        api.delete_role(role)
        self.roleTable.removeRow(self.roleTable.currentRow())

    def create_role(self):

        if self.editing_role:
            return

        self.editing_role = True
        self.creating_role = True

        self.__update_enabled()
        self.load_role()
        self.edit_button.setText("Annuler")


class InterestScreen(QtWidgets.QWidget, Ui_InterestScreen):

    def __init__(self):
        super(InterestScreen, self).__init__()
        self.setupUi(self)

        # Set table header width
        self.interestTable.setColumnWidth(0, 50)
        self.interestTable.setColumnWidth(1, 200)
        self.load_data()

        self.editing_interest = False
        self.creating_interest = False

        self.__init_connections()

        # Init interest types list
        self.type_field.addItems(Interest.INTEREST_TYPES)

        self.interestTable.selectRow(0)
        self.load_interest()

    def __init_connections(self):

        self.interestTable.itemSelectionChanged.connect(self.load_interest)
        self.edit_button.clicked.connect(self.edit_interest)
        self.save_button.clicked.connect(self.save_interest)
        self.create_button.clicked.connect(self.create_interest)
        self.delete_button.clicked.connect(self.delete_role)

    def load_interest(self):

        if self.creating_interest:
            interest = Interest(None, "", 1.0, Interest.INTEREST_TYPES[0])
        else:
            interest = self.current_interest()

        self.id_text.setText(str(interest.id))
        self.name_field.setText(interest.name)
        self.weight_field.setText(str(interest.weight))
        self.type_field.setCurrentIndex(Interest.INTEREST_TYPES.index(interest.type))

    def current_interest(self):
        interest_id = int(self.interestTable.item(self.interestTable.currentRow(), 0).text())

        return cache.get_interest(interest_id)

    def load_data(self):

        interests = cache.get_interests()

        if len(interests) <= 0:
            self.delete_button.setEnabled(False)
        else:
            self.delete_button.setEnabled(True)

        row = 0
        self.interestTable.setRowCount(len(interests))
        for i in interests:
            self.interestTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i.id)))
            self.interestTable.setItem(row, 1, QtWidgets.QTableWidgetItem(i.name))
            self.interestTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(i.weight)))
            self.interestTable.setItem(row, 3, QtWidgets.QTableWidgetItem(i.type))
            row += 1

    def _update_interest(self):
        """Update the interest at the current row"""

        i = self.current_interest()

        row = self.interestTable.currentRow()
        self.interestTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i.id)))
        self.interestTable.setItem(row, 1, QtWidgets.QTableWidgetItem(i.name))
        self.interestTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(i.weight)))
        self.interestTable.setItem(row, 3, QtWidgets.QTableWidgetItem(i.type))

    def __update_enabled(self):
        edit = self.editing_interest

        self.save_button.setEnabled(edit)
        self.name_field.setEnabled(edit)
        self.weight_field.setEnabled(edit)
        self.type_field.setEnabled(edit)
        self.interestTable.setEnabled(not edit)
        self.create_button.setEnabled(not edit)
        self.delete_button.setEnabled(not edit)

    def edit_interest(self):

        self.editing_interest = not self.editing_interest
        self.__update_enabled()

        if self.editing_interest:
            self.edit_button.setText("Annuler")
        else:
            self.creating_interest = False
            self.load_interest()
            self.edit_button.setText("Modifier")

    def save_interest(self):

        if not self.editing_interest:
            return

        if self.creating_interest:
            interest = Interest(None, "", 1.0, Interest.INTEREST_TYPES[0])
        else:
            interest = self.current_interest()

        interest.name = self.name_field.text()

        try:
            interest.weight = float(self.weight_field.text())
        except ValueError:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msgBox.setWindowTitle("Erreur")
            msgBox.setText("Valeur de poids invalide")
            msgBox.exec_()
            return

        interest.type = self.type_field.currentText()

        try:
            if self.creating_interest:
                api.create_interest(interest)
            else:
                api.update_interest(interest)

        except RuntimeError as e:

            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)

            msgBox.setWindowTitle("Erreur")
            msgBox.setText("Impossible d'enregistrer les changements")
            msgBox.setInformativeText(str(e))

            msgBox.exec_()

            return

        self.editing_interest = False
        self.edit_button.setText("Modifier")
        self.__update_enabled()

        if self.creating_interest:
            self.load_data()
            self.creating_interest = False

        self.load_interest()
        self._update_interest()

    def delete_role(self):

        if self.editing_interest or self.creating_interest or self.interestTable.currentRow() < 0:
            return

        interest = self.current_interest()

        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)

        msgBox.setWindowTitle(f"Supprimer {interest.name} ?")
        msgBox.setText("Êtes-vous sûr de vouloir supprimer l'intérêt' {} ?".format(interest.name))
        msgBox.setInformativeText("Cette action est irréversible.")

        choice = msgBox.exec_()

        if choice == QtWidgets.QMessageBox.StandardButton.Cancel:
            return

        api.delete_interest(interest)
        self.interestTable.removeRow(self.interestTable.currentRow())

    def create_interest(self):

        if self.editing_interest:
            return

        self.editing_interest = True
        self.creating_interest = True

        self.__update_enabled()
        self.load_interest()
        self.edit_button.setText("Annuler")


class UserScreen(QtWidgets.QWidget, Ui_UserScreen):

    def __init__(self):
        super(UserScreen, self).__init__()
        self.setupUi(self)

        # Set table header width
        self.userTable.setColumnWidth(0, 50)        # Id
        self.userTable.setColumnWidth(2, 175)       # Email
        self.userTable.setColumnWidth(4, 80)        # Email vérifié
        self.userTable.setColumnWidth(5, 70)        # Expiré
        self.userTable.setColumnWidth(6, 70)        # Verrouillé
        self.userTable.setColumnWidth(7, 70)        # Activé
        self.userTable.setColumnWidth(8, 135)        # Date d'enregistrement

        self.userTable.itemActivated.connect(self.open_user)
        self.userTable.selectRow(0)

        self.delete_button.clicked.connect(self.delete_user)

        # Used by user dialog to signal an user must be updated
        self.need_update = False

        self.load_data()

    def load_data(self):

        users = cache.get_users()

        if len(users) <= 0:
            self.delete_button.setEnabled(False)

        row = 0
        col = 0

        def add_item(s):
            nonlocal col, row
            self.userTable.setItem(row, col, QtWidgets.QTableWidgetItem(s))
            col += 1

        bo = lambda b: "✓" if b else "🗙"

        self.userTable.setRowCount(len(users))
        for user in users:
            add_item(str(user.id))
            add_item(user.username)
            add_item(user.email)
            
            roles_names = ""
            for r in user.roles:
                role = cache.get_role(r)
                roles_names += role.name + ", "

            roles_names = roles_names[:-2]
            
            add_item(str(roles_names))
            add_item(bo(user.emailVerified))
            add_item(bo(user.expired))
            add_item(bo(user.locked))
            add_item(bo(user.enabled))
            add_item(user.registerDate)
            add_item(user.firstName)
            add_item(user.lastName)
            add_item(user.filiere)
            add_item(user.birthday)
            add_item(user.sex)
            add_item(bo(user.hasProfilePicture))

            col = 0
            row += 1

    def current_user(self):
        user_id = int(self.userTable.item(self.userTable.currentRow(), 0).text())
        return cache.get_user(user_id)

    def _update_user(self, user):
        """Update the user at the current row"""

        row = self.userTable.currentRow()
        col = 0

        def add_item(s):
            nonlocal col, row
            self.userTable.setItem(row, col, QtWidgets.QTableWidgetItem(s))
            col += 1

        bo = lambda b: "✓" if b else "🗙"

        add_item(str(user.id))
        add_item(user.username)
        add_item(user.email)

        roles_names = ""
        for r in user.roles:
            role = cache.get_role(r)
            roles_names += role.name + ", "

        roles_names = roles_names[:-2]

        add_item(str(roles_names))
        add_item(bo(user.emailVerified))
        add_item(bo(user.expired))
        add_item(bo(user.locked))
        add_item(bo(user.enabled))
        add_item(user.registerDate)
        add_item(user.firstName)
        add_item(user.lastName)
        add_item(user.filiere)
        add_item(user.birthday)
        add_item(user.sex)
        add_item(bo(user.hasProfilePicture))

    def open_user(self, item):
        user = self.current_user()
        dialog = UserDialog(user, self)
        dialog.exec_()

        if not self.need_update: return

        self.need_update = False
        user = cache.get_user(user.id)
        self._update_user(user)

    def delete_user(self):

        if self.userTable.currentRow() < 0:
            return

        user = self.current_user()

        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)

        msgBox.setWindowTitle(f"Supprimer {user.displayName} ?")
        msgBox.setText(f"Êtes-vous sûr de vouloir supprimer l'utilisateur {user.displayName} (id: {user.id}) ?\n\nCette action est irréversible.")

        choice = msgBox.exec_()

        if choice == QtWidgets.QMessageBox.StandardButton.Cancel:
            return

        api.delete_user(user.id)
        self.userTable.removeRow(self.userTable.currentRow())


class UserDialog(QtWidgets.QDialog, Ui_UserDialog):

    def __init__(self, user, userscreen, create=False):
        super(UserDialog, self).__init__()
        self.userscreen = userscreen
        self.setupUi(self)
        self._user = user
        self.user = copy(user)
        self.creating_user = create
        self._loading = False
        self.user_roles = set()


        if not create:
            self.setWindowTitle("Utilisateur - "+self.user.displayName)

            # Save a copy to detect changes
            self.user_roles = user.roles.copy()
            self._settings = cache.get_settings(user.id)
            self.settings = self._settings.copy()

            self.interests, self.important_interests = cache.get_user_interests(user.id)
            self.interests = set(self.interests)
            self.important_interests = set(self.important_interests)
            self._interests = self.interests.copy()
            self._important_interests = self.important_interests.copy()


        else:
            self.setWindowTitle("Nouvel utilisateur")
            self.settings = DEFAULT_SETTINGS
            self.interests = set()
            self.important_interests = set()

        # Init roles
        roles = cache.get_roles()
        self.roles_checkboxes = _init_checkbox_list(self.roles_scrollarea_content,
                                                    roles,
                                                    key_func=lambda role: role.id,
                                                    name_func=lambda role: role.name,
                                                    foreach_func=lambda role, c: c.clicked.connect(lambda: self._role_changed(role.id, c.isChecked())))

        # Init interests
        interests = cache.get_interests()
        self.interests_checkboxes = _init_checkbox_list(self.interests_scroll_area_content,
                                                        interests,
                                                        key_func=lambda interest: interest.id,
                                                        name_func=lambda interest: interest.name,
                                                        foreach_func=lambda i, c: c.clicked.connect(lambda: self._interest_changed(i.id, c.isChecked())))

        self.important_interests_checkboxes = {}

        # Init filières
        self.filiere_field.addItem("")
        self.filiere_field.addItems(FILIERES)

        self.cancel_button.clicked.connect(self._cancel_changes)
        self.save_button.clicked.connect(self._save_changes)

        # Init settings
        self.lastname_public_checkbox.clicked.connect(self._settings_changed)
        self.filiere_public_checkbox.clicked.connect(self._settings_changed)
        self.birthday_public_checkbox.clicked.connect(self._settings_changed)
        self.age_public_checkbox.clicked.connect(self._settings_changed)
        self.hide_profile_checkbox.clicked.connect(self._settings_changed)
        self.sex_settings_male_checkbox.clicked.connect(self._settings_changed)
        self.sex_settings_female_checkbox.clicked.connect(self._settings_changed)
        self.sex_settings_other_checkbox.clicked.connect(self._settings_changed)

        # Init central column
        central_layout_items = (self.general_info_form_layout.layout().itemAt(i) for i in range(self.general_info_form_layout.layout().count()))
        for o in central_layout_items:

            if type(o) is not QtWidgets.QWidgetItem:
                continue

            w = o.widget()

            if type(w) in [QtWidgets.QLineEdit, QtWidgets.QTextEdit]:
                w.textChanged.connect(self._main_info_changed)

            if type(w) is QtWidgets.QComboBox:
                w.currentIndexChanged.connect(self._main_info_changed)

            if type(w) is QtWidgets.QDateTimeEdit:
                w.dateTimeChanged.connect(self._main_info_changed)

            if type(w) is QtWidgets.QDateEdit:
                w.dateChanged.connect(self._main_info_changed)

        self.email_verified_checkbox.clicked.connect(self._main_info_changed)
        self.enabled_checkbox.clicked.connect(self._main_info_changed)
        self.expired_checkbox.clicked.connect(self._main_info_changed)
        self.locked_checkbox.clicked.connect(self._main_info_changed)

        self.load_user()

    def load_user(self):

        self._loading = True

        # Load backup of user
        if not self.creating_user:
            self.user = copy(self._user)
            self.user_roles = self._user.roles.copy()
            self.settings = self._settings.copy()
            self.interests = self._interests.copy()
            self.important_interests = self._important_interests.copy()

        u = self.user

        # Central content

        if u.birthday is not None and u.birthday != "":
            birthday = QtCore.QDate.fromString(u.birthday, "yyyy-MM-dd")

        else:
            birthday = QtCore.QDate()

        self.id_text.setText(str(u.id))
        self.username_field.setText(u.username)
        self.email_field.setText(u.email)
        self.lastName_field.setText(u.lastName)
        self.firstName_field.setText(u.firstName)
        self.birthday_field.setDate(birthday)
        self.bio_field.setText(u.bio)

        sex_index = ["MALE", "FEMALE", "OTHER"].index(u.sex)
        self.sex_field.setCurrentIndex(sex_index)

        filiere_index = 0
        if u.filiere is not None and u.filiere != "":
            filiere_index = FILIERES.index(u.filiere) + 1
        self.filiere_field.setCurrentIndex(filiere_index)

        if u.registerDate is not None and u.registerDate != "":
            registerDate = QtCore.QDateTime.fromString(u.registerDate, "yyyy-MM-ddThh:mm:ssZ")
        else:
            registerDate = QtCore.QDateTime()

        self.register_date_field.setDateTime(registerDate)

        self.enabled_checkbox.setChecked(u.enabled)
        self.expired_checkbox.setChecked(u.expired)
        self.locked_checkbox.setChecked(u.locked)
        self.email_verified_checkbox.setChecked(u.emailVerified)

        # Left column

        self.load_profile_picture()

        self.displayname_label.setText(u.displayName)

        for c in self.roles_checkboxes.values():
            c.setChecked(False)

        for r in u.roles:
            self.roles_checkboxes[r].setChecked(True)

        # Right column

        s = self.settings

        self.lastname_public_checkbox.setChecked(s["lastNamePublic"])
        self.filiere_public_checkbox.setChecked(s["filierePublic"])
        self.birthday_public_checkbox.setChecked(s["birthdayPublic"])
        self.age_public_checkbox.setChecked(s["agePublic"])
        self.hide_profile_checkbox.setChecked(s["profileHidden"])

        self.sex_settings_male_checkbox.setChecked("MALE" in s["sexPreferences"])
        self.sex_settings_female_checkbox.setChecked("FEMALE" in s["sexPreferences"])
        self.sex_settings_other_checkbox.setChecked("OTHER" in s["sexPreferences"])


        def foreach_func(i, checkbox):
            checkbox.setChecked(i in self.important_interests)
            self.interests_checkboxes[i].setChecked(True)
            checkbox.clicked.connect(lambda: self._important_interest_changed(i, checkbox.isChecked()))

        # Clear and reset interests

        for c in self.interests_checkboxes.values():
            c.setChecked(False)

        for c in self.important_interests_checkboxes.values():
            c.deleteLater()

        self.important_interests_checkboxes = \
            _init_checkbox_list(self.important_interests_scrollarea_content,
                                self.interests,
                                key_func=lambda i: i,
                                name_func=lambda i: cache.get_interest(i).name,
                                foreach_func=foreach_func)

        self._loading = False

    def load_profile_picture(self):

        label = self.profile_picture_label

        pic = cache.get_profile_picture(self.user.id)
        pixmap = QPixmap()
        pixmap.loadFromData(pic)
        pixmap = pixmap.scaled(label.width(), label.height(), QtCore.Qt.KeepAspectRatio)
        self.profile_picture_label.setPixmap(pixmap)

    def _role_changed(self, id, checked):

        if self._loading: return

        if checked:
            self.user_roles.add(id)
        else:
            self.user_roles.remove(id)

        self._handle_changes()

    def _interest_changed(self, id, checked):

        if self._loading: return

        if checked:
            self.interests.add(id)

            # Add checkbox for important interests
            checkbox = QtWidgets.QCheckBox(self.important_interests_scrollarea_content)
            checkbox.setText(cache.get_interest(id).name)
            checkbox.clicked.connect(lambda: self._important_interest_changed(id, checkbox.isChecked()))

            self.important_interests_checkboxes[id] = checkbox

            self.important_interests_scrollarea_content.layout().insertWidget(len(self.interests), checkbox)

        else:
            self.interests.remove(id)
            checkbox = self.important_interests_checkboxes[id]
            checkbox.deleteLater()
            self.important_interests_checkboxes.pop(id)

            if id in self.important_interests:
                self.important_interests.remove(id)

        self._handle_changes()

    def _important_interest_changed(self, id, checked):

        if self._loading: return

        if checked:
            self.important_interests.add(id)
        else:
            self.important_interests.remove(id)

        self._handle_changes()

    def _settings_changed(self):

        if self._loading: return

        self.settings["lastNamePublic"] = self.lastname_public_checkbox.isChecked()
        self.settings["filierePublic"] = self.filiere_public_checkbox.isChecked()
        self.settings["birthdayPublic"] = self.birthday_public_checkbox.isChecked()
        self.settings["agePublic"] = self.age_public_checkbox.isChecked()
        self.settings["profileHidden"] = self.hide_profile_checkbox.isChecked()

        self.settings["sexPreferences"] = []

        if self.sex_settings_male_checkbox.isChecked():
            self.settings["sexPreferences"].append("MALE")

        if self.sex_settings_female_checkbox.isChecked():
            self.settings["sexPreferences"].append("FEMALE")

        if self.sex_settings_other_checkbox.isChecked():
            self.settings["sexPreferences"].append("OTHER")

        self._handle_changes()

    def _main_info_changed(self):

        if self._loading: return

        u = self.user

        u.username = self.username_field.text()
        u.email = self.email_field.text()
        u.lastName = self.lastName_field.text()
        u.firstName = self.firstName_field.text()
        u.birthday = self.birthday_field.date().toString("yyyy-MM-dd")
        u.sex = self.sex_field.currentText()
        u.filiere = self.filiere_field.currentText()
        u.bio = self.bio_field.toPlainText()
        u.registerDate = self.register_date_field.dateTime().toString("yyyy-MM-ddThh:mm:ssZ")
        u.enabled = self.enabled_checkbox.isChecked()
        u.expired = self.expired_checkbox.isChecked()
        u.locked = self.locked_checkbox.isChecked()
        u.emailVerified = self.email_verified_checkbox.isChecked()

        self._handle_changes()

    def _handle_changes(self):

        if self._loading: return

        changed = self.user != self._user \
                or self.interests != self._interests \
                or self.important_interests != self._important_interests \
                or self.settings != self._settings \
                or self.user_roles != self._user.roles

        self.save_button.setEnabled(changed)
        self.cancel_button.setEnabled(changed)

    def _cancel_changes(self):
        if self.creating_user:
            self.close()

        self.load_user()
        self._handle_changes()

    def _save_changes(self):

        if self.user != self._user:
            api.save_user(self.user)
            self._user = copy(self.user)

        if self.settings != self._settings:
            api.save_settings(self.user.id, self.settings)
            self._settings = self.settings.copy()

        if self.user_roles != self._user.roles:
            api.save_user_roles(self.user.id, self.user_roles)
            self._user.roles = self.user_roles.copy()
            self.user.roles = self.user_roles.copy()

        if self.interests != self._interests:
            api.save_user_interests(self.user.id, list(self.interests))
            self._interests = self.interests.copy()

        if self.important_interests != self._important_interests:
            api.save_user_important_interests(self.user.id, list(self.important_interests))
            self._important_interests = self.important_interests.copy()

        self.userscreen.need_update = True

        self._handle_changes()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle("Datingapp Control Panel")
        self.resize(1000, 500)
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setStyleSheet("QTabBar::tab\n"
                                     "{\n"
                                     "    width: 50ex;\n"
                                     "    height: 12ex;\n"
                                     "}")
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setObjectName("tabWidget")

        self.tab_users = UserScreen()
        self.tab_users.setObjectName("tab_users")
        self.tabWidget.addTab(self.tab_users, "Utilisateurs")

        self.tab_roles = RoleScreen()
        self.tab_roles.setObjectName("tab_roles")
        self.tabWidget.addTab(self.tab_roles, "Rôles")

        self.tab_interests = InterestScreen()
        self.tab_interests.setObjectName("tab_interests")
        self.tabWidget.addTab(self.tab_interests, "Intérêts")

        self.tab_conversation = QtWidgets.QWidget()
        self.tab_conversation.setObjectName("tab_conversation")
        self.tabWidget.addTab(self.tab_conversation, "Conversations")

        self.setCentralWidget(self.tabWidget)

        self.tabWidget.setCurrentIndex(0)

