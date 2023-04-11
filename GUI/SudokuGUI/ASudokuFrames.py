from abc import ABCMeta, abstractmethod
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QGridLayout, QStackedLayout, QLabel


##### ACTION FRAMES ###############################################################################


class AInteractionFrame(QFrame):
    __metaclass__ = ABCMeta
    def __init__(self, parent, edit_field, info_field) -> None:
        super().__init__(parent)                # parent == ActionFrame
        self.root = self.parent().root          # root == MainFrame
        self.edit_field = edit_field(parent=self)
        self.info_field = info_field(parent=self)
        
        self.layout = QStackedLayout()
        self.layout.addWidget(self.edit_field)
        self.layout.addWidget(self.info_field)
        self.layout.setCurrentWidget(self.info_field)
        self.setLayout(self.layout)
    
    @abstractmethod
    def toggle_edit(self, checked): ...


class AInfoField(QLabel):
    def __init__(self, parent) -> None:
        super().__init__(parent)                        # parent == InteractionFrame
        self.root = self.parent().root                  # root == MainFrame


class ANavigationFrame(QFrame):
    __metaclass__ = ABCMeta
    def __init__(self, parent) -> None:
        super().__init__(parent)                # parent == ActionFrame
        self.root = self.parent().root          # root == MainFrame
        
        self.edit_button = QPushButton("Edit")
        self.edit_button.setCheckable(True)
        self.edit_button.clicked.connect(self.toggle_edit)
        
        self.step_button = QPushButton("Step")
        self.step_button.clicked.connect(self.step)

        self.block_button = QPushButton("Block")
        self.block_button.clicked.connect(self.block)
        
        layout = QVBoxLayout()
        layout.addWidget(self.block_button)
        layout.addWidget(self.step_button)
        layout.addWidget(self.edit_button)
        
        self.setLayout(layout)
    
    @abstractmethod
    def toggle_edit(self, checked):
        self.parent().toggle_edit(checked)
    
    @abstractmethod
    def step(self):
        ...
    
    @abstractmethod
    def block(self):
        ...


##### FIELD FRAMES ################################################################################


class ALabelFrame(QLabel):
    __metaclass__ = ABCMeta
    def __init__(self, parent, label_text) -> None:
        super().__init__(parent)                # parent == FieldSettingFrame
        self.root = self.parent().root          # root == MainFrame
        self.label = QLabel(parent=self, text=label_text)
        self.design()
    
    @abstractmethod
    def design(self):
        self.setFont(QFont("Arial", 20))
        # self.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
    
    @abstractmethod
    def toggle_edit(self, checked): ...


class AFieldFrame(QFrame):
    __metaclass__ = ABCMeta
    def __init__(self, parent, sub_field) -> None:
        super().__init__(parent)                # parent == FieldSettingFrame
        self.root = self.parent().root          # root == MainFrame
        self.sub_fields = []
        
        layout = QGridLayout()

        for x in range(3):
            sub_field_row = []
            for y in range(3):
                s_field = sub_field(parent=self, coords=(x, y))
                sub_field_row.append(s_field)
                layout.addWidget(s_field, x, y)
            self.sub_fields.append(sub_field_row)
                
        self.setLayout(layout)
    
    @abstractmethod
    def toggle_edit(self, checked):
        for x in self.sub_fields:
            for y in x:
                y.toggle_edit(checked)


class ASubField(QFrame):
    __metaclass__ = ABCMeta
    def __init__(self, parent, coords: tuple, field_class) -> None:
        super().__init__(parent)            # parent == FieldFrame
        self.root = self.parent().root      # root == MainFrame
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
        super().__init__(parent)            # parent == SubField
        self.root = self.parent().root      # root == MainFrame
        self.coords = coords
        
        self.setFixedSize(40,40)
        self.setFont(QFont("Arial", 15))
    
    @abstractmethod
    def toggle_edit(self, checked): ...
