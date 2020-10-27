#Author Sean Di Rienzo
import sys

from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import *
import PyQt5
import PyQt5.QtWidgets
from Application import Session as api


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        MainWindow.setWindowTitle(self, "Sean Di Rienzo Final Project")
        self.app = api()
        self.tableView = QTableView()
        self.filter_string = ""
        """bind model to view"""
        self.model = self.app.database_session.model.model
        self.tableView.setModel(self.model)

        self.layout = QVBoxLayout()
        self.combo = QComboBox(self)
        self.combo.addItem("CheeseId")
        self.combo.addItem("CheeseNameEn")
        self.combo.addItem("ManufacturerNameEn")
        self.combo.addItem("ManufacturerProvCode")
        self.combo.addItem("ManufacturingTypeEn")
        self.combo.addItem("WebSiteEn")
        self.combo.addItem("FatContentPercent")
        self.combo.addItem("MoisturePercent")
        self.combo.addItem("ParticularitiesEn")
        self.combo.addItem("FlavourEn")
        self.combo.addItem("CharacteristicsEn")
        self.combo.addItem("RipeningEn")
        self.combo.addItem("Organic")
        self.combo.addItem("CategoryTypeEn")
        self.combo.addItem("MilkTypeEn")
        self.combo.addItem("MilkTreatmentTypeEN")
        self.combo.addItem("RindTypeEn")
        self.combo.addItem("LastUpdateDate")
        self.filterButton = QPushButton("Filter")
        addButton = QPushButton("add")
        deleteButton = QPushButton("delete")
        reloadButton = QPushButton("reload")
        resetFilterButton = QPushButton("reset filters")
        hLayout = QHBoxLayout()
        hLayout.addWidget(reloadButton)
        hLayout.addWidget(addButton)
        hLayout.addWidget(deleteButton)
        hLayout.addWidget(resetFilterButton)
        hLayout.addWidget(self.combo)
        hLayout.addWidget(self.filterButton)
        self.layout.addWidget(self.tableView)
        self.layout.addLayout(hLayout)
        self.setLayout(self.layout)
        self.resize(1280, 720)

        addButton.clicked.connect(self.onAddRow)
        deleteButton.clicked.connect(self.onDeleteRow)
        reloadButton.clicked.connect(self.reload)
        resetFilterButton.clicked.connect(self.resetFilters)
        self.filterButton.clicked.connect(self.showDialog)

    def filterBuilder(self, column, value):
        tempString = column + "=" + "'" + value + "'"
        if self.filter_string == "":
            self.filter_string = tempString

        else:
            self.filter_string = self.filter_string + " AND " + tempString

        self.updateFilter()

    def updateFilter(self):
        print(self.filter_string)
        self.model.setFilter(self.filter_string)

    def resetFilters(self):
        self.model.setFilter("")
        self.filter_string = ""

    def reload(self):
        """function to reload data from the provided dataset"""
        self.app.database_session.create_working_table()
        self.app.database_session.model.initializedModel()

    def onAddRow(self):
        """function to add a row to the database table and refresh tableview"""
        self.tableView.scrollToBottom()
        print(self.model.rowCount())

        self.model.insertRows(self.app.get_model().rowCount(), 1)

        self.model.submit()

    def onDeleteRow(self):
        """function to remove a row from the database table and refresh tableview"""
        self.app.d(self.tableView.currentIndex().row())
        self.model.submit()
        self.model.select()

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Filter: ' + self.combo.currentText(), 'Enter text:')
        if ok:
            self.filterBuilder(self.combo.currentText(), text)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
