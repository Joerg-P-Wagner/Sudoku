

class Field:
    def __init__(self) -> None:
        self.number_amount = {x:0 for x in range(1,10)}
        self.sub_fields = [[SubField(sub_field_coords=(x,y)) for y in range(3)] for x in range(3)]
        self.blocked = False
    
    def step(self):
        self.toggle_block(7)
    
    def toggle_block(self, number):
        self.blocked = True if not self.blocked else False
        for x in self.sub_fields:
            for sub_field in x:
                sub_field.blocked = self.blocked if number in sub_field.get_numbers() else False
                for y in sub_field.single_fields:
                    for single_field in y:
                        if single_field.number == number:
                            
                            self.block_cross(single_field.coords, self.blocked)
    
    def block_cross(self, coords, on):
        self.block_horizontal(coords[0][0], coords[1][0], on)
        self.block_vertical(coords[0][1], coords[1][1], on)
    
    def block_horizontal(self, x1, x2, on):
        for y in range(3):
            self.sub_fields[x1][y].block_horizontal(x2, on)
    
    def block_vertical(self, y1, y2, on):
        for x in range(3):
            self.sub_fields[x][y1].block_vertical(y2, on)
    
    def count_numbers(self):
        self.number_amount = {x:0 for x in range(1,10)}
        for x in self.sub_fields:
            for sub_field in x:
                for y in sub_field.single_fields:
                    for single_field in y:
                        if single_field.number:
                            self.number_amount[single_field.number] += 1
    
    def set_numbers(self, number, coords):
        for coord in coords:
            self.sub_fields[coord[0][0]][coord[0][1]].set_numbers(number, coord[1])


class SubField:
    def __init__(self, sub_field_coords) -> None:
        self.coords = sub_field_coords
        self.single_fields = [[SingleField(single_field_coords=(sub_field_coords,(x,y))) for y in range(3)] for x in range(3)]
        self.blocked = False

    def set_numbers(self, number, coords):
        self.single_fields[coords[0]][coords[1]].set_number(number)
    
    def get_numbers(self) -> list:
        return [ single_field.number for sl in self.single_fields for single_field in sl if single_field.number ]

    def block_horizontal(self, x, on):
        for y in range(3):
            self.single_fields[x][y].blocked = on
    
    def block_vertical(self, y, on):
        for x in range(3):
            self.single_fields[x][y].blocked = on


class SingleField:
    def __init__(self, single_field_coords) -> None:
        self.number = None
        self.blocked = False
        self.coords = single_field_coords
    
    def set_number(self, number: int):
        self.number = number
