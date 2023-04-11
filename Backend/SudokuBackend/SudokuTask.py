

class SudokuTask:
    def __init__(self):
        ...


class Field:
    def __init__(self) -> None:
        self.number_amount = {x:0 for x in range(1,10)}
        self.working_number = []
        self.sub_fields = [[SubField(sub_field_coords=(x,y)) for y in range(3)] for x in range(3)]
        self.blocked = False
        self.unblocked = []

    def block(self): # -> Solution
        self.toggle_block(2)    #
    
    def toggle_block(self, number):    # -> Solution
        self.blocked = True if not self.blocked else False
        for x in self.sub_fields:
            for sub_field in x:
                if number in sub_field.get_numbers():
                    sub_field.blocked = self.blocked
                    sub_field.full_block(self.blocked)
                for y in sub_field.single_fields:
                    for single_field in y:
                        if single_field.number == number:
                            if self.blocked:
                                self.unblocked = []
                            self.block_cross(single_field.coords, self.blocked)
    
    def block_cross(self, coords, on):  # -> Solution
        self.block_horizontal(coords[0][0], coords[1][0], on)
        self.block_vertical(coords[0][1], coords[1][1], on)
    
    def block_horizontal(self, x1, x2, on): # -> Solution
        for y in range(3):
            self.sub_fields[x1][y].block_horizontal(x2, on)
    
    def block_vertical(self, y1, y2, on):   # -> Solution
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
    
    def get_max_amount_number(self):
        m = 0
        r = 0
        self.count_numbers()
        for k, v in self.number_amount.items():
            r = k if v > m and v < 9 else r
            m = v if v > m and v < 9 else m
        self.max_amount_number = r
        print(f"working number -> {r}")

    def get_unblocked(self):    # -> Solution
        self.unblocked = []
        for x in self.sub_fields:
            for sub_field in x:
                l = sub_field.get_unblocked()
                if len(l) == 1:
                    self.unblocked.append(*l)
    
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

    def block_horizontal(self, x, on):  # -> Solution
        for y in range(3):
            self.single_fields[x][y].blocked = on
    
    def block_vertical(self, y, on):    # -> Solution
        for x in range(3):
            self.single_fields[x][y].blocked = on
    
    def full_block(self, on):   # -> Solution
        for x in range(3):
            for y in range(3):
                self.single_fields[x][y].blocked = on
    
    def get_unblocked(self):    # -> Solution
        l = [ single_field.coords for sl in self.single_fields for single_field in sl if not single_field.blocked]
        print(f"unblocked coordinates: {l}")
        return l


class SingleField:
    def __init__(self, single_field_coords) -> None:
        self.number = None
        self.blocked = False
        self.coords = single_field_coords
    
    def set_number(self, number: int):
        self.number = number
        self.blocked = True

Sudoku = Field()
