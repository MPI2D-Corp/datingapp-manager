# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources\user-dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UserDialog(object):
    def setupUi(self, UserDialog):
        UserDialog.setObjectName("UserDialog")
        UserDialog.resize(717, 533)
        UserDialog.setWindowTitle("")
        UserDialog.setSizeGripEnabled(False)
        UserDialog.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(UserDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.content_layout = QtWidgets.QHBoxLayout()
        self.content_layout.setSpacing(10)
        self.content_layout.setObjectName("content_layout")
        self.left_col_groupbox = QtWidgets.QGroupBox(UserDialog)
        self.left_col_groupbox.setObjectName("left_col_groupbox")
        self.left_col_layout = QtWidgets.QVBoxLayout(self.left_col_groupbox)
        self.left_col_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.left_col_layout.setObjectName("left_col_layout")
        self.profile_picture_label = QtWidgets.QLabel(self.left_col_groupbox)
        self.profile_picture_label.setMinimumSize(QtCore.QSize(128, 128))
        self.profile_picture_label.setMaximumSize(QtCore.QSize(128, 128))
        self.profile_picture_label.setText("")
        self.profile_picture_label.setObjectName("profile_picture_label")
        self.left_col_layout.addWidget(self.profile_picture_label)
        self.displayname_label = QtWidgets.QLabel(self.left_col_groupbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.displayname_label.sizePolicy().hasHeightForWidth())
        self.displayname_label.setSizePolicy(sizePolicy)
        self.displayname_label.setAlignment(QtCore.Qt.AlignCenter)
        self.displayname_label.setObjectName("displayname_label")
        self.left_col_layout.addWidget(self.displayname_label)
        self.line_2 = QtWidgets.QFrame(self.left_col_groupbox)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.left_col_layout.addWidget(self.line_2)
        self.roles_label = QtWidgets.QLabel(self.left_col_groupbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.roles_label.sizePolicy().hasHeightForWidth())
        self.roles_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.roles_label.setFont(font)
        self.roles_label.setObjectName("roles_label")
        self.left_col_layout.addWidget(self.roles_label)
        self.roles_scrollarea = QtWidgets.QScrollArea(self.left_col_groupbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.roles_scrollarea.sizePolicy().hasHeightForWidth())
        self.roles_scrollarea.setSizePolicy(sizePolicy)
        self.roles_scrollarea.setWidgetResizable(True)
        self.roles_scrollarea.setObjectName("roles_scrollarea")
        self.roles_scrollarea_content = QtWidgets.QWidget()
        self.roles_scrollarea_content.setGeometry(QtCore.QRect(0, 0, 126, 69))
        self.roles_scrollarea_content.setObjectName("roles_scrollarea_content")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.roles_scrollarea_content)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.roles_scrollarea.setWidget(self.roles_scrollarea_content)
        self.left_col_layout.addWidget(self.roles_scrollarea)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.left_col_layout.addItem(spacerItem)
        self.content_layout.addWidget(self.left_col_groupbox)
        self.general_info_form_layout = QtWidgets.QFormLayout()
        self.general_info_form_layout.setObjectName("general_info_form_layout")
        self.id_label = QtWidgets.QLabel(UserDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.id_label.setFont(font)
        self.id_label.setObjectName("id_label")
        self.general_info_form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.id_label)
        self.id_text = QtWidgets.QLabel(UserDialog)
        self.id_text.setText("")
        self.id_text.setObjectName("id_text")
        self.general_info_form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.id_text)
        self.username_label = QtWidgets.QLabel(UserDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.username_label.setFont(font)
        self.username_label.setObjectName("username_label")
        self.general_info_form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.username_label)
        self.username_field = QtWidgets.QLineEdit(UserDialog)
        self.username_field.setObjectName("username_field")
        self.general_info_form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.username_field)
        self.email_label = QtWidgets.QLabel(UserDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.email_label.setFont(font)
        self.email_label.setObjectName("email_label")
        self.general_info_form_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.email_label)
        self.email_field = QtWidgets.QLineEdit(UserDialog)
        self.email_field.setObjectName("email_field")
        self.general_info_form_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.email_field)
        self.lastName_label = QtWidgets.QLabel(UserDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lastName_label.setFont(font)
        self.lastName_label.setObjectName("lastName_label")
        self.general_info_form_layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.lastName_label)
        self.lastName_field = QtWidgets.QLineEdit(UserDialog)
        self.lastName_field.setObjectName("lastName_field")
        self.general_info_form_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lastName_field)
        self.firstName_label = QtWidgets.QLabel(UserDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.firstName_label.setFont(font)
        self.firstName_label.setObjectName("firstName_label")
        self.general_info_form_layout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.firstName_label)
        self.firstName_field = QtWidgets.QLineEdit(UserDialog)
        self.firstName_field.setObjectName("firstName_field")
        self.general_info_form_layout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.firstName_field)
        self.birthday_label = QtWidgets.QLabel(UserDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.birthday_label.setFont(font)
        self.birthday_label.setObjectName("birthday_label")
        self.general_info_form_layout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.birthday_label)
        self.birthday_field = QtWidgets.QDateEdit(UserDialog)
        self.birthday_field.setDateTime(QtCore.QDateTime(QtCore.QDate(1970, 1, 1), QtCore.QTime(0, 0, 0)))
        self.birthday_field.setCalendarPopup(True)
        self.birthday_field.setObjectName("birthday_field")
        self.general_info_form_layout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.birthday_field)
        self.sex_label = QtWidgets.QLabel(UserDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.sex_label.setFont(font)
        self.sex_label.setObjectName("sex_label")
        self.general_info_form_layout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.sex_label)
        self.sex_field = QtWidgets.QComboBox(UserDialog)
        self.sex_field.setObjectName("sex_field")
        self.sex_field.addItem("")
        self.sex_field.addItem("")
        self.sex_field.addItem("")
        self.general_info_form_layout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.sex_field)
        self.filiere_label = QtWidgets.QLabel(UserDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.filiere_label.setFont(font)
        self.filiere_label.setObjectName("filiere_label")
        self.general_info_form_layout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.filiere_label)
        self.filiere_field = QtWidgets.QComboBox(UserDialog)
        self.filiere_field.setObjectName("filiere_field")
        self.general_info_form_layout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.filiere_field)
        self.bio_label = QtWidgets.QLabel(UserDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.bio_label.setFont(font)
        self.bio_label.setObjectName("bio_label")
        self.general_info_form_layout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.bio_label)
        self.line_main_info = QtWidgets.QFrame(UserDialog)
        self.line_main_info.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_main_info.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_main_info.setObjectName("line_main_info")
        self.general_info_form_layout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.line_main_info)
        self.register_date_label = QtWidgets.QLabel(UserDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.register_date_label.setFont(font)
        self.register_date_label.setObjectName("register_date_label")
        self.general_info_form_layout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.register_date_label)
        self.register_date_field = QtWidgets.QDateTimeEdit(UserDialog)
        self.register_date_field.setEnabled(False)
        self.register_date_field.setDateTime(QtCore.QDateTime(QtCore.QDate(1970, 1, 1), QtCore.QTime(0, 0, 0)))
        self.register_date_field.setCalendarPopup(True)
        self.register_date_field.setObjectName("register_date_field")
        self.general_info_form_layout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.register_date_field)
        self.admin_prop_label = QtWidgets.QLabel(UserDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.admin_prop_label.setFont(font)
        self.admin_prop_label.setObjectName("admin_prop_label")
        self.general_info_form_layout.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.admin_prop_label)
        self.admin_prop_layout = QtWidgets.QHBoxLayout()
        self.admin_prop_layout.setObjectName("admin_prop_layout")
        self.enabled_checkbox = QtWidgets.QCheckBox(UserDialog)
        self.enabled_checkbox.setObjectName("enabled_checkbox")
        self.admin_prop_layout.addWidget(self.enabled_checkbox)
        self.expired_checkbox = QtWidgets.QCheckBox(UserDialog)
        self.expired_checkbox.setObjectName("expired_checkbox")
        self.admin_prop_layout.addWidget(self.expired_checkbox)
        self.locked_checkbox = QtWidgets.QCheckBox(UserDialog)
        self.locked_checkbox.setObjectName("locked_checkbox")
        self.admin_prop_layout.addWidget(self.locked_checkbox)
        self.email_verified_checkbox = QtWidgets.QCheckBox(UserDialog)
        self.email_verified_checkbox.setObjectName("email_verified_checkbox")
        self.admin_prop_layout.addWidget(self.email_verified_checkbox)
        self.general_info_form_layout.setLayout(11, QtWidgets.QFormLayout.FieldRole, self.admin_prop_layout)
        self.bio_field = QtWidgets.QTextEdit(UserDialog)
        self.bio_field.setMarkdown("")
        self.bio_field.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>")
        self.bio_field.setObjectName("bio_field")
        self.general_info_form_layout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.bio_field)
        self.content_layout.addLayout(self.general_info_form_layout)
        self.right_col_box = QtWidgets.QGroupBox(UserDialog)
        self.right_col_box.setObjectName("right_col_box")
        self.right_col_layout = QtWidgets.QVBoxLayout(self.right_col_box)
        self.right_col_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.right_col_layout.setObjectName("right_col_layout")
        self.settings_label = QtWidgets.QLabel(self.right_col_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settings_label.sizePolicy().hasHeightForWidth())
        self.settings_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.settings_label.setFont(font)
        self.settings_label.setObjectName("settings_label")
        self.right_col_layout.addWidget(self.settings_label)
        self.lastname_public_checkbox = QtWidgets.QCheckBox(self.right_col_box)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lastname_public_checkbox.setFont(font)
        self.lastname_public_checkbox.setObjectName("lastname_public_checkbox")
        self.right_col_layout.addWidget(self.lastname_public_checkbox)
        self.filiere_public_checkbox = QtWidgets.QCheckBox(self.right_col_box)
        self.filiere_public_checkbox.setObjectName("filiere_public_checkbox")
        self.right_col_layout.addWidget(self.filiere_public_checkbox)
        self.birthday_public_checkbox = QtWidgets.QCheckBox(self.right_col_box)
        self.birthday_public_checkbox.setObjectName("birthday_public_checkbox")
        self.right_col_layout.addWidget(self.birthday_public_checkbox)
        self.age_public_checkbox = QtWidgets.QCheckBox(self.right_col_box)
        self.age_public_checkbox.setObjectName("age_public_checkbox")
        self.right_col_layout.addWidget(self.age_public_checkbox)
        self.hide_profile_checkbox = QtWidgets.QCheckBox(self.right_col_box)
        self.hide_profile_checkbox.setObjectName("hide_profile_checkbox")
        self.right_col_layout.addWidget(self.hide_profile_checkbox)
        self.settings_sex_groupbox = QtWidgets.QGroupBox(self.right_col_box)
        self.settings_sex_groupbox.setObjectName("settings_sex_groupbox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.settings_sex_groupbox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.sex_settings_male_checkbox = QtWidgets.QCheckBox(self.settings_sex_groupbox)
        self.sex_settings_male_checkbox.setObjectName("sex_settings_male_checkbox")
        self.verticalLayout_4.addWidget(self.sex_settings_male_checkbox)
        self.sex_settings_female_checkbox = QtWidgets.QCheckBox(self.settings_sex_groupbox)
        self.sex_settings_female_checkbox.setObjectName("sex_settings_female_checkbox")
        self.verticalLayout_4.addWidget(self.sex_settings_female_checkbox)
        self.sex_settings_other_checkbox = QtWidgets.QCheckBox(self.settings_sex_groupbox)
        self.sex_settings_other_checkbox.setObjectName("sex_settings_other_checkbox")
        self.verticalLayout_4.addWidget(self.sex_settings_other_checkbox)
        self.right_col_layout.addWidget(self.settings_sex_groupbox)
        self.line = QtWidgets.QFrame(self.right_col_box)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.right_col_layout.addWidget(self.line)
        self.interest_label = QtWidgets.QLabel(self.right_col_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.interest_label.sizePolicy().hasHeightForWidth())
        self.interest_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.interest_label.setFont(font)
        self.interest_label.setObjectName("interest_label")
        self.right_col_layout.addWidget(self.interest_label)
        self.interests_scroll_area = QtWidgets.QScrollArea(self.right_col_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.interests_scroll_area.sizePolicy().hasHeightForWidth())
        self.interests_scroll_area.setSizePolicy(sizePolicy)
        self.interests_scroll_area.setMaximumSize(QtCore.QSize(200, 16777215))
        self.interests_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.interests_scroll_area.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.interests_scroll_area.setWidgetResizable(True)
        self.interests_scroll_area.setObjectName("interests_scroll_area")
        self.interests_scroll_area_content = QtWidgets.QWidget()
        self.interests_scroll_area_content.setGeometry(QtCore.QRect(0, 0, 117, 85))
        self.interests_scroll_area_content.setObjectName("interests_scroll_area_content")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.interests_scroll_area_content)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.interests_scroll_area.setWidget(self.interests_scroll_area_content)
        self.right_col_layout.addWidget(self.interests_scroll_area)
        self.important_interests_label = QtWidgets.QLabel(self.right_col_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.important_interests_label.sizePolicy().hasHeightForWidth())
        self.important_interests_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.important_interests_label.setFont(font)
        self.important_interests_label.setObjectName("important_interests_label")
        self.right_col_layout.addWidget(self.important_interests_label)
        self.important_interests_scrollarea = QtWidgets.QScrollArea(self.right_col_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.important_interests_scrollarea.sizePolicy().hasHeightForWidth())
        self.important_interests_scrollarea.setSizePolicy(sizePolicy)
        self.important_interests_scrollarea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.important_interests_scrollarea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.important_interests_scrollarea.setWidgetResizable(True)
        self.important_interests_scrollarea.setObjectName("important_interests_scrollarea")
        self.important_interests_scrollarea_content = QtWidgets.QWidget()
        self.important_interests_scrollarea_content.setGeometry(QtCore.QRect(0, 0, 117, 84))
        self.important_interests_scrollarea_content.setObjectName("important_interests_scrollarea_content")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.important_interests_scrollarea_content)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.important_interests_scrollarea.setWidget(self.important_interests_scrollarea_content)
        self.right_col_layout.addWidget(self.important_interests_scrollarea)
        self.content_layout.addWidget(self.right_col_box)
        self.verticalLayout.addLayout(self.content_layout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.save_button = QtWidgets.QPushButton(UserDialog)
        self.save_button.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_button.sizePolicy().hasHeightForWidth())
        self.save_button.setSizePolicy(sizePolicy)
        self.save_button.setMinimumSize(QtCore.QSize(100, 0))
        self.save_button.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.save_button.setShortcut("")
        self.save_button.setCheckable(False)
        self.save_button.setChecked(False)
        self.save_button.setObjectName("save_button")
        self.horizontalLayout.addWidget(self.save_button)
        self.cancel_button = QtWidgets.QPushButton(UserDialog)
        self.cancel_button.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel_button.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(sizePolicy)
        self.cancel_button.setMinimumSize(QtCore.QSize(100, 0))
        self.cancel_button.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(UserDialog)
        self.sex_field.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(UserDialog)

    def retranslateUi(self, UserDialog):
        _translate = QtCore.QCoreApplication.translate
        self.displayname_label.setText(_translate("UserDialog", "Nom"))
        self.roles_label.setText(_translate("UserDialog", "Rôles :"))
        self.id_label.setText(_translate("UserDialog", "Id :"))
        self.username_label.setText(_translate("UserDialog", "Pseudo :"))
        self.email_label.setText(_translate("UserDialog", "Email :"))
        self.lastName_label.setText(_translate("UserDialog", "Nom :"))
        self.firstName_label.setText(_translate("UserDialog", "Prénom :"))
        self.birthday_label.setText(_translate("UserDialog", "Date de naissance :"))
        self.sex_label.setText(_translate("UserDialog", "Sexe :"))
        self.sex_field.setItemText(0, _translate("UserDialog", "MALE"))
        self.sex_field.setItemText(1, _translate("UserDialog", "FEMALE"))
        self.sex_field.setItemText(2, _translate("UserDialog", "OTHER"))
        self.filiere_label.setText(_translate("UserDialog", "Filière :"))
        self.bio_label.setText(_translate("UserDialog", "Biographie :"))
        self.register_date_label.setText(_translate("UserDialog", "Date d\'inscription :"))
        self.admin_prop_label.setText(_translate("UserDialog", "Propriétés :"))
        self.enabled_checkbox.setText(_translate("UserDialog", "Activé"))
        self.expired_checkbox.setText(_translate("UserDialog", "Expiré"))
        self.locked_checkbox.setText(_translate("UserDialog", "Verrouillé"))
        self.email_verified_checkbox.setText(_translate("UserDialog", "Email vérifié"))
        self.settings_label.setText(_translate("UserDialog", "Paramètres :"))
        self.lastname_public_checkbox.setText(_translate("UserDialog", "Nom public"))
        self.filiere_public_checkbox.setText(_translate("UserDialog", "Filière publique"))
        self.birthday_public_checkbox.setText(_translate("UserDialog", "Anniversaire public"))
        self.age_public_checkbox.setText(_translate("UserDialog", "Age public"))
        self.hide_profile_checkbox.setText(_translate("UserDialog", "Cacher le profil"))
        self.settings_sex_groupbox.setTitle(_translate("UserDialog", "Préférences de sexe"))
        self.sex_settings_male_checkbox.setText(_translate("UserDialog", "MALE"))
        self.sex_settings_female_checkbox.setText(_translate("UserDialog", "FEMALE"))
        self.sex_settings_other_checkbox.setText(_translate("UserDialog", "OTHER"))
        self.interest_label.setText(_translate("UserDialog", "Intérêts :"))
        self.important_interests_label.setText(_translate("UserDialog", "Intérêts importants :"))
        self.save_button.setText(_translate("UserDialog", "Enregistrer"))
        self.cancel_button.setText(_translate("UserDialog", "Annuler"))