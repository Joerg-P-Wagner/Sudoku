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
            self.root.field_setting_frame.field_frame.set_style()


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
        print(self.field_coords)
    
    def remove_field_coords(self, coords):
        self.field_coords.remove(*coords)
        print(self.field_coords)


class NumberButtom(ASingleField):
    def __init__(self, parent, coords: tuple) -> None:
        super().__init__(parent, coords)
        self.clicked.connect(self.save_number)

    def save_number(self):
        self.root.backend.set_numbers(int(self.text()), self.parent().field_coords)
        while(len(self.parent().field_coords) > 0):
            coord = self.parent().field_coords[0]
            self.root.field_setting_frame.field_frame.sub_fields[coord[0][0]][coord[0][1]].single_fields[coord[1][0]][coord[1][1]].set_text()
            self.root.field_setting_frame.field_frame.sub_fields[coord[0][0]][coord[0][1]].single_fields[coord[1][0]][coord[1][1]].click()
        self.root.backend.count_numbers()


class NavigationFrame(ANavigationFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        
        
    def step(self):
        self.root.field_setting_frame.field_frame.set_text
        self.root.field_setting_frame.field_frame.set_style
        self.parent().interaction_frame.info_field.make_update
        
    def block(self):
        self.root.backend.block()
        self.root.field_setting_frame.field_frame.set_style()
        
        


##### FIELD FRAMES ################################################################################


class LabelFrame(ALabelFrame):
    def __init__(self, parent, label_text) -> None:
        super().__init__(parent, label_text)


class FieldFrame(AFieldFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent, SubField)

    def set_style(self):
        [ sub_field.set_style() for x in self.sub_fields for sub_field in x ]
    
    def set_text(self):
        [ sub_field.set_text() for x in self.sub_fields for sub_field in x ]
        


class SubField(ASubField):
    def __init__(self, parent, coords: tuple) -> None:
        super().__init__(parent, coords, field_class=SingleField)
    
    def set_style(self):
        [ single_field.set_style(self.root.backend.sub_fields[self.coords[0]][self.coords[1]].blocked) for x in self.single_fields for single_field in x ]
    
    def set_text(self):
        [ single_field.set_text() for x in self.single_fields for single_field in x ]


class SingleField(ASingleField):
    def __init__(self, parent, coords: tuple) -> None:
        super().__init__(parent, coords)
        self.backend_single_field = self.root.backend.sub_fields[self.coords[0][0][0]][self.coords[0][0][1]].single_fields[self.coords[0][1][0]][self.coords[0][1][1]]

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
            # if number == None:
            self.setStyleSheet("background-color: #ccffc7; border: 1px solid black;")
            self.root.action_frame.interaction_frame.edit_field.add_field_coords(self.coords)
            # else check number in edit_field
            #   -> if uncheck in edit_field -> delete number in backend
        else:
            self.setStyleSheet("background-color: #fffaf0; border: 1px solid black;")
            self.root.action_frame.interaction_frame.edit_field.remove_field_coords(self.coords)
        self.update()
    
    def set_style(self, subfield_blocked=False):
        if self.backend_single_field.number:
            self.setStyleSheet("background-color: #c9c9c9; border: 1px solid black;")
        elif self.backend_single_field.blocked or subfield_blocked:
            self.setStyleSheet("background-color: #c9f3f3; border: 1px solid black;")
        else:
            self.setStyleSheet("background-color: #fffaf0; border: 1px solid black;")
    
    def set_text(self):
        v = self.backend_single_field.number
        text = str(v) if v else ""
        self.setText(text)
        self.update()
