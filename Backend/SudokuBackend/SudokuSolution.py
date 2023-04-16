import logging, sys

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)
logger.setLevel(10)

class SudokuSolution:
    def __init__(self, field) -> None:
        self.field = field
        self.total_number_amount = 0
        self.progress = True
        
        self.number = 0
        self.blocked = False
        self.free_fields = []
        self.single_free_fields = []
        
        self.expected_blocked = False
        self.unblocked_expectation = []
        self.expected_lines = []
        
        self.count = 0
        
        self.steps_1 = [self.toggle_block, self.get_free_fields, self.get_single_free_fields, self.set_numbers, self.toggle_block]
        self.steps_2 = [self.toggle_block, self.get_free_fields, self.toggle_expectation, self.get_free_fields, self.get_single_free_fields, self.toggle_expectation, self.toggle_block]
    
    def block(self):
        self.toggle_block()
    
    def toggle_block(self):
        self.blocked = True if not self.blocked else False
        logger.debug("in toggle_block; block = {self.blocked}")
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
    
    def block_horizontal(self, x1, x2, on, exp=False):
        logger.debug(f"in block horizontal x1={x1} x2={x2} on={on} exp={exp}")
        for y in range(3):
            for z in range(3):
                if exp:
                    if not self.field.sub_fields[x1][y].single_fields[x2][z].expected_number:   # toggle also expected numbers if they are not themself
                        self.field.sub_fields[x1][y].single_fields[x2][z].is_expected_blocked = on
                else:
                    if not self.field.sub_fields[x1][y].single_fields[x2][z].number:
                        self.field.sub_fields[x1][y].single_fields[x2][z].is_blocked = on
    
    def block_vertical(self, y1, y2, on, exp=False):
        logger.debug(f"in block vertical y1={y1} y2={y2} on={on} exp={exp}")
        for x in range(3):
            for z in range(3):
                if exp:
                    if not self.field.sub_fields[x][y1].single_fields[z][y2].expected_number:
                        self.field.sub_fields[x][y1].single_fields[z][y2].is_expected_blocked = on
                else:
                    if not self.field.sub_fields[x][y1].single_fields[z][y2].number:
                        self.field.sub_fields[x][y1].single_fields[z][y2].is_blocked = on

    @staticmethod
    def subfield_full_block(sub_field, on):
        for x in range(3):
            for y in range(3):
                if not sub_field.single_fields[x][y].number:
                    sub_field.single_fields[x][y].is_blocked = on
    
    def get_free_fields(self) -> None:
        self.free_fields = []
        for x in self.field.sub_fields:
            for sub_field in x:
                l = []
                l = [ single_field.coords for sl in sub_field.single_fields for single_field in sl if not (single_field.is_blocked or single_field.is_expected_blocked) ]
                self.free_fields.append(l)
        print(f"free_fields -> {self.free_fields}")

    def get_single_free_fields(self):
        self.single_free_fields = []
        for l in self.free_fields:
            if len(l) == 1:
                self.field.sub_fields[l[0][0][0]][l[0][0][1]].single_fields[l[0][1][0]][l[0][1][1]].is_single_free_field = True
                self.single_free_fields.append(*l)
                print(l)

    def set_numbers(self) -> None:
        self.field.set_numbers(self.number, self.single_free_fields)

    def toggle_expectation(self):   # find lines -> set expected numbers -> block
        self.expected_blocked = True if not self.expected_blocked else False
        self.expected_lines = []
        for fields in self.free_fields:
            if 1 < len(fields) < 4:
                horizontal = True
                vertical = True
                h_coord = fields[0][1][0]
                v_coord = fields[0][1][1]
                for coord_pair in fields:
                    if h_coord != coord_pair[1][0]:
                        horizontal = False
                        break
                for coord_pair in fields:
                    if v_coord != coord_pair[1][1]:
                        vertical = False
                        break
                if horizontal or vertical:
                    self.expected_lines.append((fields, horizontal))
        self.toggle_expected_numbers(on=self.expected_blocked)
        self.toggle_expected_block(on=self.expected_blocked)
    
    def toggle_expected_numbers(self, on) -> None:
        for coords in self.expected_lines:
            if on:
                self.field.set_numbers(self.number, coords[0], is_expected=True)
            else:
                self.field.set_numbers(None, coords[0], is_expected=True)   

    def toggle_expected_block(self, on):
        print(f"block is {on} self.expected_lines -> {self.expected_lines}")
        for line in self.expected_lines:
            if line[1]:
                self.block_horizontal(line[0][0][0][0], line[0][0][1][0], on, exp=True)
            else:
                self.block_vertical(line[0][0][0][1], line[0][0][1][1], on, exp=True)
    
    def detect_progress(self):
        if self.number == 1:
            if self.total_number_amount != self.field.number_amount['total']:
                self.total_number_amount = self.field.number_amount['total']
            else:
                self.progress = False
                self.count = 0
                print("No progress")

    def step(self):
        if self.progress:
            self.cross_block_method()
        else:
            self.block_of_expectation()
    
    def cross_block_method(self):
        i = self.count % len(self.steps_1)  #####
        if i == 0:
            while(True):
                self.number += 1
                self.number = 1 if self.number == 10 else self.number
                self.detect_progress()
                if self.field.number_amount[self.number] != 9: break
        self.steps_1[i]()   #####
        self.count += 1
    
    def block_of_expectation(self):
        i = self.count % len(self.steps_2)  #####
        if i == 0:
            while(True):
                self.number += 1
                self.number = 1 if self.number == 10 else self.number
                self.detect_progress()
                if self.field.number_amount[self.number] != 9: break
        self.steps_2[i]()   #####
        self.count += 1
    
    def missing_in_square(self):
        ...
    
    def missing_in_line(self):
        ...
