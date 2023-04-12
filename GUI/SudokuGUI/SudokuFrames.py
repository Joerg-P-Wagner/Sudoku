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
    
        n = 1
        for x in self.single_fields:
            for y in x:
                y.setText(str(n))
                n += 1
        
    def add_field_coords(self, coords):
        self.field_coords += tuple(coords)
    
    def remove_field_coords(self, coords):
        self.field_coords.remove(*coords)


class NumberButtom(ASingleField):
    def __init__(self, parent, coords: tuple) -> None:
        super().__init__(parent, coords)
        self.clicked.connect(self.save_number)

    def save_number(self):
        self.root.backend.set_numbers(int(self.text()), self.parent().field_coords)
        self.root.backend.count_numbers()
        self.root.make_update()

class NavigationFrame(ANavigationFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        
        
    def step(self):
        self.root.solution.step()     # WIP   
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
        super().__init__(parent, coords)
        self.make_update()
    
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
            # if number == None:
            self.setStyleSheet("background-color: #ccffc7; border: 1px solid black;")
            self.root.action_frame.interaction_frame.edit_field.add_field_coords(self.coords)
            # else check number in edit_field
            #   -> if uncheck in edit_field -> delete number in backend
        else:
            self.setStyleSheet("background-color: #fffaf0; border: 1px solid black;")
            self.root.action_frame.interaction_frame.edit_field.remove_field_coords(self.coords)
        self.update()
    
    def __set_style(self, subfield_blocked=False):
        if self.backend_single_field.number:
            self.setStyleSheet("background-color: #c9c9c9; border: 1px solid black;")
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
