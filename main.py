#!/usr/local/bin/python
from pyqtUI import MainWindow as Window
from PyQt5.QtWidgets import QApplication
from passlogic import setUpSql
import sys

if __name__ == "__main__":
    setUpSql()
    app = QApplication(sys.argv)
    ui = Window()
    ui.show()
    sys.exit(app.exec_())
# to-do's:
# move DB to fireBase - > prob won't



