import sys
import threading
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog
from PyQt5.uic import loadUi
from main import Geospatial_Location_Webscraper

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        loadUi('Gui_window.ui', self)
        self.toolButton.clicked.connect(self.browsefile)
        self.Open_file.triggered.connect(self.browsefile)
        self.actionClose.triggered.connect(self.close)
        self.pushButton.clicked.connect(self.buttonclick)
        self.pushButton_1.clicked.connect(self.stop_program)
        self.stop_request = False
        self.show()
        self.progressTimer = QtCore.QTimer(self)
        self.progressTimer.timeout.connect(self.update_progress_bar)

    def browsefile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:/', 'CSV files (*.csv)')
        self.File_Name.setText(fname[0])

    def stop_program(self):
        self.stop_request = True
        self.progressTimer.stop()
        self.progressBar.setValue(0)  # Optionally reset the progress bar to 0

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Confirm Close',
                                               'Are you sure you want to close the application?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def buttonclick(self):
        self.Target_Lat = float(self.lineEdit.text())
        self.Target_Long = float(self.lineEdit_2.text())
        filename = self.File_Name.text()
        self.progressBar.setValue(0)
        self.progressTimer.start(1850)  # Update every 1800 ms
        self.stop_request = False
        self.background_thread = threading.Thread(target=self.perform_web_scraping,
                                                  args=(filename, self.Target_Lat, self.Target_Long),
                                                  daemon=True)
        self.background_thread.start()

    def update_progress_bar(self):
        value = self.progressBar.value()
        if value < 100:
            self.progressBar.setValue(value + 10)

    def perform_web_scraping(self, filename, Target_Lat, Target_Long):
        scraper = Geospatial_Location_Webscraper()

        # Step 1: Submit batch of addresses for geocoding
        if not self.stop_request:
            scraper.submit_batch_csv(filename, 'geocoded_addresses_results.csv')

        # Step 2: Process the geocoded results
        if not self.stop_request:
            scraper.process_geocoded_results('geocoded_addresses_results.csv', 'sorted_geocoded_addresses.csv')

        # Step 3: Calculate the closest address
        if not self.stop_request:
            closest_address = scraper.calculate_closest_address_to_target('sorted_geocoded_addresses.csv', 'addresses.csv', Target_Lat, Target_Long)

        if not self.stop_request:
            QtCore.QMetaObject.invokeMethod(self.textEdit_1, "setText", QtCore.Q_ARG(str, str(closest_address)))

        # Reset the stop flag and progress bar
        self.stop_request = False
        self.progressTimer.stop()
        QtCore.QMetaObject.invokeMethod(self.progressBar, "setValue", QtCore.Q_ARG(int, 100))

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Ui()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


    #  37.065984, -79.601172