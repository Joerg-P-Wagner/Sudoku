from abc import ABCMeta, abstractmethod
from PySide6.QtWidgets import QFrame, QPushButton, QGridLayout, QLabel


##### ACTION FRAMES ###############################################################################


class AInteractionFrame(QFrame):
    __metaclass__ = ABCMeta
    def __init__(self, parent) -> None:
        super().__init__(parent)
    
    @abstractmethod
    def toggle_edit(self, checked): ...


class ANavigationFrame(QFrame):
    __metaclass__ = ABCMeta
    def __init__(self, parent) -> None:
        super().__init__(parent)
    
    @abstractmethod
    def toggle_edit(self, checked):
        self.parent().toggle_edit(checked)


##### FIELD FRAMES ################################################################################


class ALabelFrame(QLabel):
    __metaclass__ = ABCMeta
    def __init__(self, parent, label_text) -> None:
        super().__init__(parent)
        self.label = QLabel(parent=self, text=label_text)
        self.design()
    
    @abstractmethod
    def design(self): ...
    
    @abstractmethod
    def toggle_edit(self, checked): ...


class AFieldFrame(QFrame):
    __metaclass__ = ABCMeta
    def __init__(self, parent) -> None:
        super().__init__(parent)
    
    @abstractmethod
    def toggle_edit(self, checked): ...


class ASubField(QFrame):
    __metaclass__ = ABCMeta
    def __init__(self, parent, coords: tuple, field_class) -> None:
        super().__init__(parent)
        self.coords = coords
        self.single_fields = []
        
        layout = QGridLayout()
        
        for x in range(3):
            single_field_row = []
            for y in range(3):
                single_field = field_class(parent=self, coords=((self.coords,(x, y)), ))
                single_field_row.append(single_field)
                layout.addWidget(single_field, x, y)
            self.single_fields.append(single_field_row)
                
        self.setLayout(layout)
    
    @abstractmethod
    def toggle_edit(self, checked):
        for x in self.single_fields:
            for y in x:
                y.toggle_edit(checked)


class ASingleField(QPushButton):
    __metaclass__ = ABCMeta
    def __init__(self, parent, coords) -> None:
        super().__init__(parent)
        self.root = self.parent().parent().parent().parent()
        self.coords = coords
    
    @abstractmethod
    def toggle_edit(self, checked): ...
