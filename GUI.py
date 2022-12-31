from PyQt5 import QtWidgets, uic
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('Gui_window.ui', self)
        self.show()
        self.setWindowTitle("Geospatial Location Webscraper")


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Ui()
    app.exec_()

if __name__ == "__main__":
    main()