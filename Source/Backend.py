

class Field:
    def __init__(self) -> None:
        self.number_amount = {x:0 for x in range(1,10)}
        self.sub_fields = [[SubField(sub_field_coords=(x,y)) for x in range(3)] for y in range(3)]
        
    def block(self, number):
        for x in self.sub_fields:
            for sub_field in x:
                sub_field.blocked = True if number in sub_field.get_numbers() else False
                for y in sub_field.single_fields:
                    for single_field in y:
                        single_field.blocked = True if number == single_field.number else False
                        if single_field.blocked:
                            self.block_cross(single_field.coords)
    
    def block_cross(self, coords):
        ...
    
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
        self.single_fields = [[SingleField(single_field_coords=(sub_field_coords,(x,y))) for x in range(3)] for y in range(3)]
        self.blocked = False

    def set_numbers(self, number, coords):
        self.single_fields[coords[0]][coords[1]].set_number(number)
    
    def get_numbers(self) -> list:
        return [ [ single_field.number for single_field in single_field_row ] for single_field_row in self.single_fields ]


class SingleField:
    def __init__(self, single_field_coords) -> None:
        self.number = None
        self.blocked = False
        self.coords = single_field_coords
    
    def set_number(self, number: int):
        self.number = number
