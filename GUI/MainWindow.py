import sys

from PySide6.QtWidgets import QApplication

from . import Sudoku
from .AbstractFields import AMainWindow, AMainFrame, AActionFrame, AFieldSettingFrame


##################################################################################################
##### BASE FRAMES ################################################################################
##################################################################################################


class MainWindow(AMainWindow):
    def __init__(self, label_text) -> None:
        super().__init__(main_frame=MainFrame, label_text=label_text)
        
        self.setWindowTitle("Sudoku Solver")
        # self.setFixedSize(1000,1000)
        self.setStyleSheet("background-color: #fff3d1")


class MainFrame(AMainFrame):
    def __init__(self, parent, label_text) -> None:
        super().__init__(parent, field_setting_frame=FieldSettingFrame, action_frame=ActionFrame, label_text=label_text)


##### ACTION FRAMES ###############################################################################


class ActionFrame(AActionFrame):
    def __init__(self, parent):
        super().__init__(parent, interaction_frame=Sudoku.InteractionFrame, navigation_frame=Sudoku.NavigationFrame)


##### FIELD FRAMES ################################################################################


class FieldSettingFrame(AFieldSettingFrame):
    def __init__(self, parent, label_text) -> None:
        super().__init__(parent, field_frame=Sudoku.FieldFrame, label_frame = Sudoku.LabelFrame, label_text=label_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    
    app.exec()
