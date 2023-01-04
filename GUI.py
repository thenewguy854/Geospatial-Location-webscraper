from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QProgressBar
from PyQt5.uic import loadUi
import sys
import time
from main import Geospatial_Location_Webscraper

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        n = 500
        loadUi('Gui_window.ui', self)
        self.toolButton.clicked.connect(self.browsefile)
        self.pushButton.clicked.connect(lambda status, n_size=n: self.buttonclick(n_size))
        self.progressBar.setRange(0, n)
        self.show()


    def browsefile (self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:/', 'CSV files (*.csv)')
        self.File_Name.setText(fname[0])

    def buttonclick(self, n):
        Target_Lat = self.lineEdit.text()
        Target_Long = self.lineEdit_2.text()
        filename = self.File_Name.text()
        self.Target_Lat = float(Target_Lat)
        self.Target_Long = float(Target_Long)
        textEdit_1 = Geospatial_Location_Webscraper.backed(self, self.Target_Lat, self.Target_Long, filename)
        answer = " ".join(textEdit_1)
        self.textEdit_1.setText(answer)
        for i in range(n):
            time.sleep(0.01)
            self.progressBar.setValue(i+n)



def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Ui()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

    #  37.065984, -79.601172