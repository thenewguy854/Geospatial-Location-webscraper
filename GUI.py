from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QProgressBar
from PyQt5.uic import loadUi
import sys
import os
from main import Geospatial_Location_Webscraper

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()


        loadUi('Gui_window.ui', self)
        self.toolButton.clicked.connect(self.browsefile)
        self.show()
        self.pushButton.clicked.connect(self.buttonclick)



    def browsefile (self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:/', 'CSV files (*.csv)')
        self.File_Name.setText(fname[0])

    def buttonclick(self):
        Target_Lat = self.lineEdit.text()
        Target_Long = self.lineEdit_2.text()
        filename = self.File_Name.text()
        self.Target_Lat = float(Target_Lat)
        self.Target_Long = float(Target_Long)
        self.perform_web_scraping(filename)

    def perform_web_scraping(self, filename):
        scrapper = Geospatial_Location_Webscraper()
        url, addresses = scrapper.URL_Generator(filename)
        textEdit_1 = scrapper.get_page(url, self.Target_Lat, self.Target_Long, addresses)
        answer = "".join(textEdit_1)
        self.textEdit_1.setText(answer)



def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Ui()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

    #  37.065984, -79.601172   C:/Users/Chuck Husak/PycharmProjects/Geospatial Location webscraper/addresses.csv