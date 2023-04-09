from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QStackedLayout, QPushButton, QLabel

from .ASudoku import AInteractionFrame, ANavigationFrame, ALabelFrame, AFieldFrame, ASubField, ASingleField
from Source import Backend


##### ACTION FRAMES ###############################################################################


class InteractionFrame(AInteractionFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        
        self.edit_number_field = EditNumberField(parent=self)
        self.info_field = InfoField(parent=self)
        
        self.layout = QStackedLayout()
        self.layout.addWidget(self.edit_number_field)
        self.layout.addWidget(self.info_field)
        self.layout.setCurrentWidget(self.info_field)
        
        self.setLayout(self.layout)
    
    def toggle_edit(self, checked):
        if checked:
            self.layout.setCurrentWidget(self.edit_number_field)
        else:
            self.info_field.make_update()
            self.layout.setCurrentWidget(self.info_field)


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


class EditNumberField(ASubField):
    def __init__(self, parent) -> None:
        super().__init__(parent, (0,0), field_class=NumberField)
        self.field_coords = []
    
        n = 1
        for x in self.single_fields:
            for y in x:
                y.setText(str(n))
                n += 1
        
    def add_field_coords(self, coords):
        self.field_coords += tuple(coords)
    
    def remove_field_coords(self, coords):
        try:
            self.field_coords.remove(*coords)
        except ValueError: ...


class NumberField(ASingleField):
    def __init__(self, parent, coords: tuple) -> None:
        super().__init__(parent, coords)
        self.clicked.connect(self.save_number)
        
        self.setFixedSize(40,40)
        self.setFont(QFont("Arial", 15))
    
    def save_number(self):
        self.root.field_setting_frame.field_frame.backend_field.set_numbers(int(self.text()), self.parent().field_coords)
        while(len(self.parent().field_coords) > 0):
            coord = self.parent().field_coords.pop(0)
            self.root.field_setting_frame.field_frame.sub_fields[coord[0][0]][coord[0][1]].single_fields[coord[1][0]][coord[1][1]].set_text()
            self.root.field_setting_frame.field_frame.sub_fields[coord[0][0]][coord[0][1]].single_fields[coord[1][0]][coord[1][1]].is_checked(False)
        self.root.field_setting_frame.field_frame.backend_field.count_numbers()


class NavigationFrame(ANavigationFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        
        self.edit_button = QPushButton("Edit")
        self.edit_button.setCheckable(True)
        self.edit_button.pos
        self.edit_button.clicked.connect(self.parent().toggle_edit)
        
        layout = QHBoxLayout()
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
        
    def toggle_edit(self, checked):
        for x in self.sub_fields:
            for y in x:
                y.toggle_edit(checked)


class SubField(ASubField):
    def __init__(self, parent, coords: tuple) -> None:
        super().__init__(parent, coords, field_class=SingleField)


class SingleField(ASingleField):
    def __init__(self, parent, coords: tuple) -> None:
        super().__init__(parent, coords)
        self.backend_single_field = self.parent().parent().backend_field.sub_fields[self.coords[0][0][0]][self.coords[0][0][1]].single_fields[self.coords[0][1][0]][self.coords[0][1][1]]
        
        self.setFixedSize(40,40)
        self.setFont(QFont("Arial", 15))
        
        self.set_style()
        self.set_text()
    
    def toggle_edit(self, edit_checked):
        if edit_checked:
            self.setCheckable(True)
            self.clicked.connect(self.is_checked)
        else:
            self.is_checked(False)
            self.setCheckable(False)
            self.clicked.connect(self.is_checked)
        self.update()
        
    def is_checked(self, self_checked):
        if self_checked:
            self.setStyleSheet("background-color: #ccffc7; border: 1px solid black;")
            self.root.action_frame.interaction_frame.edit_number_field.add_field_coords(self.coords)
        else:
            self.setStyleSheet("background-color: #fffaf0; border: 1px solid black;")
            self.root.action_frame.interaction_frame.edit_number_field.remove_field_coords(self.coords)
        self.update()
    
    def set_style(self):
        if self.backend_single_field.blocked:
            print("grau")
        else:
            self.setStyleSheet("background-color: #fffaf0; border: 1px solid black;")
    
    def set_text(self):
        v = self.backend_single_field.number
        text = str(v) if v else ""
        self.setText(text)
        self.update()
