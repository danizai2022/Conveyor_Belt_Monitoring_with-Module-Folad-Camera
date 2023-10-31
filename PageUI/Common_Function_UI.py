from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets, QtCore


class Common_Function_UI:
    def __init__(self):
        """Description of the code"""

        # self.ui = ui

    def set_message(self, label_name, text, level=1):
        """Show warning with time delay 2 second , all labels for show warning has been set here"""

        if text != None:
            if level == 1:
                label_name.setText(" " + text + " ")
                label_name.setStyleSheet(
                    "background-color:rgb(140, 140, 140);border-radius:2px;color:black"
                )

            QTimer.singleShot(10000, lambda: self.set_message(label_name, None))

        else:
            label_name.setText("")
            label_name.setStyleSheet("")

    def show_alert_window(self, title, message, need_confirm=False, level=1):
        """this function is used to create a confirm window
        :param title: _description_, defaults to 'Message'
        :type title: str, optional
        :param message: _description_, defaults to 'Message'
        :type message: str, optional
        :return: _description_
        :rtype: _type_
        """

        level = 0 if level < 0 or level > 2 else level

        # create message box
        alert_window = QtWidgets.QMessageBox()

        # icon
        if level == 0:
            alert_window.setIcon(QtWidgets.QMessageBox.Information)
        elif level == 1:
            alert_window.setIcon(QtWidgets.QMessageBox.Warning)
        elif level == 2:
            alert_window.setIcon(QtWidgets.QMessageBox.Critical)

        # Message and title
        alert_window.setText(message)
        alert_window.setWindowTitle(title)
        # buttons
        if not need_confirm:
            alert_window.setStandardButtons(QtWidgets.QMessageBox.Ok)
            alert_window.button(QtWidgets.QMessageBox.Ok).setText("ok")
        else:
            alert_window.setStandardButtons(
                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Ok
            )
            alert_window.button(QtWidgets.QMessageBox.Ok).setText("Yes")
            alert_window.button(QtWidgets.QMessageBox.Cancel).setText("Cancel")

        alert_window.setWindowFlags(
            QtCore.Qt.Dialog
            | QtCore.Qt.CustomizeWindowHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint
        )
        returnValue = alert_window.exec()

        if not need_confirm:
            return True if returnValue == QtWidgets.QMessageBox.Ok else True
        else:
            return True if returnValue == QtWidgets.QMessageBox.Ok else False
