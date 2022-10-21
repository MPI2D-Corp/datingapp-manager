from PyQt5.QtWidgets import QApplication
import datingapp
from datingapp.ui import LoginDialog, MainWindow
from datingapp import api
import sys

datingapp.baseurl = "http://localhost:8080"
datingapp.cache_directory = ".cache/"

datingapp.init()


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook


app = QApplication(sys.argv)

if not api.authenticated:
    loginWin = LoginDialog()
    loginWin.show()
    app.exec_()

print(f"Logged in as {api.user.displayName} !")

win = MainWindow()
win.show()
exit(app.exec_())

