from .ASudokuFrames import AInteractionFrame, AInfoField, ANavigationFrame, ALabelFrame, AFieldFrame, ASubField, ASingleField


##### ACTION FRAMES ###############################################################################


class InteractionFrame(AInteractionFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent, EditField, InfoField)
    
    def toggle_edit(self, checked):
        if checked:
            self.layout.setCurrentWidget(self.edit_field)
        else:
            self.info_field.make_update()
            self.layout.setCurrentWidget(self.info_field)


class InfoField(AInfoField):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.backend = self.root.backend
        self.make_update()

    def make_update(self):
        self.backend.count_numbers()
        text = ""
        for k, v in self.backend.number_amount.items():
            text += f"{k}: {v}x"
            text += "\n" if k in [3, 6, 9] else "\t"
            
        self.setText(text)
        self.update()


class EditField(ASubField):
    def __init__(self, parent) -> None:
        super().__init__(parent, (0,0), field_class=NumberButtom)
        self.field_coords = []
        self.field_value = []
        self.connected_button = None
    
        n = 1
        for x in self.single_fields:
            for y in x:
                y.setText(str(n))
                n += 1
        
    def add_field_coords(self, coords):
        self.field_coords += tuple(coords)
    
    def remove_field_coords(self, coords):
        self.field_coords.remove(*coords)
    
    def toggle_button(self):
        if self.connect_button.isChecked():...
    
    def connect_button(self, number):
        if number == 1:
            self.connected_button = self.single_fields[0][0]
        elif number == 2:
            self.connected_button = self.single_fields[0][1]
        elif number == 3:
            self.connected_button = self.single_fields[0][2]
        elif number == 4:
            self.connected_button = self.single_fields[1][0]
        elif number == 5:
            self.connected_button = self.single_fields[1][1]
        elif number == 6:
            self.connected_button = self.single_fields[1][2]
        elif number == 7:
            self.connected_button = self.single_fields[2][0]
        elif number == 8:
            self.connected_button = self.single_fields[2][1]
        elif number == 9:
            self.connected_button = self.single_fields[2][2]
            
        self.connected_button.clicked.disconnect()
        self.connected_button.setCheckable(True)
        self.connected_button.setChecked(True)
        self.connected_button.clicked.connect(self.connected_button.delete_number)
    
    def disconnect_button(self):
        if self.connected_button:
            self.connected_button.clicked.disconnect()
            self.connected_button.setChecked(False)
            self.connected_button.setCheckable(False)
            self.connected_button.clicked.connect(self.connected_button.save_number)


class NumberButtom(ASingleField):
    def __init__(self, parent, coords: tuple) -> None:
        super().__init__(parent, coords)
        self.clicked.connect(self.save_number)

    def save_number(self) -> None:
        self.root.backend.set_numbers(int(self.text()), self.parent().field_coords, is_start_number=True)
        # self.parent().field_value.append
        self.root.make_update()
    
    def delete_number(self) -> None:
        self.root.backend.set_numbers(None, self.parent().field_coords, is_start_number=False)
        self.root.make_update()
        self.parent().disconnect_button()

class NavigationFrame(ANavigationFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        
        
    def step(self):
        self.root.solution.step()
        self.root.make_update()
        
    def block(self):
        self.root.solution.block()
        self.root.make_update()


##### FIELD FRAMES ################################################################################


class LabelFrame(ALabelFrame):
    def __init__(self, parent, label_text) -> None:
        super().__init__(parent, label_text)


class FieldFrame(AFieldFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent, SubField)


class SubField(ASubField):
    def __init__(self, parent, coords: tuple) -> None:
        super().__init__(parent, coords, field_class=SingleField)


class SingleField(ASingleField):
    def __init__(self, parent, coords: tuple) -> None:
        super().__init__(parent, coords, True)
        self.make_update()
        self.connected_numbutton = None
    
    def toggle_edit(self, checked):
        if checked:
            self.clicked.connect(self.check)
            self.setCheckable(True)
        else:
            if self.isChecked():
                self.click()
            self.setCheckable(False)
            self.clicked.disconnect()
        
    def check(self, self_checked):
        if self_checked:
            self.root.action_frame.interaction_frame.edit_field.add_field_coords(self.coords)
            self.root.action_frame.interaction_frame.edit_field.field_value.append(self.backend_single_field.number)
            value_count = self.root.action_frame.interaction_frame.edit_field.field_value.count(self.root.action_frame.interaction_frame.edit_field.field_value[-1])
            
            if value_count == len(self.root.action_frame.interaction_frame.edit_field.field_value) and self.backend_single_field.number:
                self.root.action_frame.interaction_frame.edit_field.connect_button(self.backend_single_field.number)
            else:
                self.root.action_frame.interaction_frame.edit_field.disconnect_button()
        else:
            self.root.action_frame.interaction_frame.edit_field.remove_field_coords(self.coords)
            self.root.action_frame.interaction_frame.edit_field.field_value.pop(-1)
            if len(self.root.action_frame.interaction_frame.edit_field.field_value) <= 0:
                self.root.action_frame.interaction_frame.edit_field.disconnect_button()
        self.__set_style()
        self.update()
    
    def __set_style(self, subfield_blocked=False):
        if self.backend_single_field.is_start_number:
            if self.isChecked():
                self.setStyleSheet("background-color: #9fff94; border: 1px solid black;")
            else:
                self.setStyleSheet("background-color: #c9c9c9; border: 1px solid black;")
        elif self.isChecked():
            self.setStyleSheet("background-color: #ccffc7; border: 1px solid black;")
        elif self.backend_single_field.number:
            self.setStyleSheet("background-color: #DBEEFF; border: 1px solid black;")
        elif self.backend_single_field.is_blocked or subfield_blocked:
            self.setStyleSheet("background-color: #c9f3f3; border: 1px solid black;")
        else:
            self.setStyleSheet("background-color: #fffaf0; border: 1px solid black;")
    
    def __set_text(self):
        v = self.backend_single_field.number
        text = str(v) if v else ""
        self.setText(text)
        self.update()
    
    def make_update(self) -> None:
        if self.isChecked():
            self.click()
        self.__set_style()
        self.__set_text()
        self.update()
