from abc import ABCMeta, abstractmethod
from PySide6.QtWidgets import QMainWindow, QFrame, QHBoxLayout, QVBoxLayout

from Backend import SudokuBackend


##################################################################################################
##### BASE FRAMES ################################################################################
##################################################################################################


class AMainWindow(QMainWindow):
    __metaclass__ = ABCMeta
    def __init__(self, main_frame, label_text) -> None:
        super().__init__()
        self.main_frame = main_frame(parent=self, label_text=label_text)
        self.setCentralWidget(self.main_frame)
        self.show()


class AMainFrame(QFrame):   # AMainFrame == ROOT-Frame
    __metaclass__ = ABCMeta
    def __init__(self, parent, field_setting_frame, action_frame, label_text) -> None:
        super().__init__(parent)
        if label_text == "Sudoku":
            self.backend = SudokuBackend.SudokuTask.Field()
            self.solution = SudokuBackend.SudokuSolution(self.backend)
        self.field_setting_frame = field_setting_frame(parent=self, label_text=label_text)
        self.action_frame = action_frame(parent=self)

        layout = QHBoxLayout()
        layout.addWidget(self.field_setting_frame)
        layout.addWidget(self.action_frame)
        self.setLayout(layout)
    
    @abstractmethod
    def toggle_edit(self, checked):
        self.field_setting_frame.toggle_edit(checked)
    
    @abstractmethod
    def make_update(self) -> None:
        self.field_setting_frame.make_update()


##### ACTION FRAMES ###############################################################################


class AActionFrame(QFrame):
    __metaclass__ = ABCMeta
    def __init__(self, parent, interaction_frame, navigation_frame) -> None:
        super().__init__(parent)        # parent == MainFrame
        self.root = self.parent()       # root == MainFrame
        self.interaction_frame = interaction_frame(parent=self)
        self.navigation_frame = navigation_frame(parent=self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.interaction_frame)
        layout.addWidget(self.navigation_frame)
        self.setLayout(layout)
    
    @abstractmethod
    def toggle_edit(self, checked):
        self.parent().toggle_edit(checked)
        self.interaction_frame.toggle_edit(checked)
    
    @abstractmethod
    def make_update(self) -> None:
        self.interaction_frame.make_update()
        # self.navigation_frame.make_update()     # will be not neccessary i think


##### FIELD FRAMES ################################################################################


class AFieldSettingFrame(QFrame):
    __metaclass__ = ABCMeta
    def __init__(self, parent, field_frame, label_frame, label_text) -> None:
        super().__init__(parent)        # parent == MainFrame
        self.root = self.parent()       # root == MainFrame
        self.label_frame = label_frame(parent=self, label_text=label_text)
        self.field_frame = field_frame(parent=self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label_frame)
        layout.addWidget(self.field_frame)
        self.setLayout(layout)
    
    @abstractmethod
    def toggle_edit(self, checked):
        self.label_frame.toggle_edit(checked)
        self.field_frame.toggle_edit(checked)
    
    @abstractmethod
    def make_update(self) -> None:
        self.label_frame.make_update()
        self.field_frame.make_update()
