import sys
from PySide6.QtWidgets import QApplication
from GUI.MainWindow import MainWindow


app = QApplication(sys.argv)
window = MainWindow("Sudoku")

app.exec()
