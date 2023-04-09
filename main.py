import sys
from PySide6.QtWidgets import QApplication
from GUI.MainWindow import MainWindow
from Source.Backend import Field


app = QApplication(sys.argv)
window = MainWindow("Sudoku")
logic = Field()

app.exec()
