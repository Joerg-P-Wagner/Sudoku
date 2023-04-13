

class SudokuSolution:
    def __init__(self, field) -> None:
        self.field = field
        self.number = 0
        self.blocked = False
        self.unblocked = []
        
        self.count = 0
        # self.numbers = [x + 1 for x in range(9)]
        # self.working_number = 1
        self.steps = [self.toggle_block, self.get_unblocked, self.toggle_block]
    
    def block(self):
        self.toggle_block()
    
    def toggle_block(self):
        self.blocked = True if not self.blocked else False
        for x in self.field.sub_fields:
            for sub_field in x:
                if self.number in sub_field.get_numbers():
                    sub_field.blocked = self.blocked
                    self.subfield_full_block(sub_field, self.blocked)
                for y in sub_field.single_fields:
                    for single_field in y:
                        if single_field.number == self.number:
                            self.block_cross(single_field.coords, self.blocked)
    
    def block_cross(self, coords, on):
        self.block_horizontal(coords[0][0], coords[1][0], on)
        self.block_vertical(coords[0][1], coords[1][1], on)
    
    def block_horizontal(self, x1, x2, on):
        for y in range(3):
            for z in range(3):
                if not self.field.sub_fields[x1][y].single_fields[x2][z].number:
                    self.field.sub_fields[x1][y].single_fields[x2][z].is_blocked = on
    
    def block_vertical(self, y1, y2, on):
        for x in range(3):
            for z in range(3):
                if not self.field.sub_fields[x][y1].single_fields[z][y2].number:
                    self.field.sub_fields[x][y1].single_fields[z][y2].is_blocked = on

    @staticmethod
    def subfield_full_block(sub_field, on):
        for x in range(3):
            for y in range(3):
                if not sub_field.single_fields[x][y].number:
                    sub_field.single_fields[x][y].is_blocked = on

    def get_unblocked(self):
        self.unblocked = []
        for x in self.field.sub_fields:
            for sub_field in x:
                l = []
                l = [ single_field.coords for sl in sub_field.single_fields for single_field in sl if not single_field.is_blocked]
                print(f"l == {l}")
                if len(l) == 1:
                    self.unblocked.append(*l)
        print(self.unblocked)
        self.field.set_numbers(self.number, self.unblocked)





    def step(self):
        self.missing_in_field()
    
    def missing_in_field(self):
        i = self.count % len(self.steps)
        if i == 0:
            while(True):
                self.number += 1
                self.number = 1 if self.number == 10 else self.number
                if self.field.number_amount[self.number] != 9: break
        self.steps[i]()
        self.count += 1
        
        print(self.number)
    
    def missing_in_square(self):
        ...
    
    def missing_in_line(self):
        ...
