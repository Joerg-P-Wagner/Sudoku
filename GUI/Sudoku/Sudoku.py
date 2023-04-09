from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QStackedLayout, QPushButton, QLabel

from .ASudoku import AInteractionFrame, ANavigationFrame, ALabelFrame, AFieldFrame, ASubField, ASingleField
from Source import Backend


##### ACTION FRAMES ###############################################################################


class InteractionFrame(AInteractionFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        
        self.number_block = NumberBlock(parent=self)
        self.info_field = InfoField(parent=self)
        
        self.layout = QStackedLayout()
        self.layout.addWidget(self.number_block)
        self.layout.addWidget(self.info_field)
        self.layout.setCurrentWidget(self.info_field)
        
        self.setLayout(self.layout)
    
    def toggle_edit(self, checked):
        if checked:
            self.layout.setCurrentWidget(self.number_block)
        else:
            self.info_field.make_update()
            self.layout.setCurrentWidget(self.info_field)
            self.parent().parent().field_setting_frame.field_frame.set_style()


class InfoField(QLabel):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.backend_field = self.parent().parent().parent().field_setting_frame.field_frame.backend_field
        self.make_update()

    def make_update(self):
        text = ""
        for k, v in self.backend_field.number_amount.items():
            text += f"{k}: {v}x"
            text += "\n" if k in [3, 6, 9] else "\t"
            
        self.setText(text)
        self.update()


class NumberBlock(ASubField):
    def __init__(self, parent) -> None:
        super().__init__(parent, (0,0), field_class=NumberButtom)
        self.field_coords = []
    
        n = 1
        for x in self.single_fields:
            for y in x:
                y.setText(str(n))
                n += 1
        
    def add_field_coords(self, coords):
        self.field_coords += tuple(coords)
        print(self.field_coords)
    
    def remove_field_coords(self, coords):
        self.field_coords.remove(*coords)
        print(self.field_coords)


class NumberButtom(ASingleField):
    def __init__(self, parent, coords: tuple) -> None:
        super().__init__(parent, coords)
        self.clicked.connect(self.save_number)
        
        self.setFixedSize(40,40)
        self.setFont(QFont("Arial", 15))
    
    def save_number(self):
        self.root.field_setting_frame.field_frame.backend_field.set_numbers(int(self.text()), self.parent().field_coords)
        while(len(self.parent().field_coords) > 0):
            coord = self.parent().field_coords[0]
            self.root.field_setting_frame.field_frame.sub_fields[coord[0][0]][coord[0][1]].single_fields[coord[1][0]][coord[1][1]].set_text()
            self.root.field_setting_frame.field_frame.sub_fields[coord[0][0]][coord[0][1]].single_fields[coord[1][0]][coord[1][1]].click()
        self.root.field_setting_frame.field_frame.backend_field.count_numbers()


class NavigationFrame(ANavigationFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        
        self.edit_button = QPushButton("Edit")
        self.edit_button.setCheckable(True)
        self.edit_button.clicked.connect(self.parent().toggle_edit)
        
        self.block_button = QPushButton("Block")
        self.block_button.clicked.connect(self.parent().parent().field_setting_frame.field_frame.backend_field.step)
        self.block_button.clicked.connect(self.parent().parent().field_setting_frame.field_frame.set_style)
        
        layout = QVBoxLayout()
        layout.addWidget(self.block_button)
        layout.addWidget(self.edit_button)
        
        self.setLayout(layout)


##### FIELD FRAMES ################################################################################


class LabelFrame(ALabelFrame):
    def __init__(self, parent, label_text) -> None:
        super().__init__(parent, label_text)
    
    def design(self):
        self.setFont(QFont("Arial", 20))
        self.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)


class FieldFrame(AFieldFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.backend_field = Backend.Field()
        self.sub_fields = []
        
        layout = QGridLayout()
        
        for x in range(3):
            sub_field_row = []
            for y in range(3):
                sub_field = SubField(parent=self, coords=(x, y))
                sub_field_row.append(sub_field)
                layout.addWidget(sub_field, x, y)
            self.sub_fields.append(sub_field_row)
                
        self.setLayout(layout)
    
    def set_style(self):
        [ sub_field.set_style() for x in self.sub_fields for sub_field in x ]
        


class SubField(ASubField):
    def __init__(self, parent, coords: tuple) -> None:
        super().__init__(parent, coords, field_class=SingleField)
    
    def set_style(self):
        [ single_field.set_style(self.parent().backend_field.sub_fields[self.coords[0]][self.coords[1]].blocked) for x in self.single_fields for single_field in x ]


class SingleField(ASingleField):
    def __init__(self, parent, coords: tuple) -> None:
        super().__init__(parent, coords)
        self.backend_single_field = self.parent().parent().backend_field.sub_fields[self.coords[0][0][0]][self.coords[0][0][1]].single_fields[self.coords[0][1][0]][self.coords[0][1][1]]
        
        self.setFixedSize(40,40)
        self.setFont(QFont("Arial", 15))
        
        self.set_style()
        self.set_text()
    
    def toggle_edit(self, checked):
        if checked:
            self.clicked.connect(self.check)
            self.setCheckable(True)
        else:
            if self.isChecked():
                self.click()
            self.setCheckable(False)
            self.clicked.disconnect()
        self.update()
        
    def check(self, self_checked):
        if self_checked:
            self.setStyleSheet("background-color: #ccffc7; border: 1px solid black;")
            self.root.action_frame.interaction_frame.number_block.add_field_coords(self.coords)
        else:
            self.setStyleSheet("background-color: #fffaf0; border: 1px solid black;")
            self.root.action_frame.interaction_frame.number_block.remove_field_coords(self.coords)
        self.update()
    
    def set_style(self, subfield_blocked=False):
        if self.backend_single_field.blocked or subfield_blocked:
            self.setStyleSheet("background-color: #B5B5B5; border: 1px solid black;")
        else:
            self.setStyleSheet("background-color: #fffaf0; border: 1px solid black;")
    
    def set_text(self):
        v = self.backend_single_field.number
        text = str(v) if v else ""
        self.setText(text)
        self.update()
