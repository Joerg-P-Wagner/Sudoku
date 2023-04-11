

class SudokuSolution:
    def __init__(self, field) -> None:
        self.field = field
        self.steps = 0
        self.numbers = [x + 1 for x in range(9)]
        self.working_number = 1
        self.max_number_amount_steps = [self.field.toggle_block, self.field.get_unblocked, self.field.set_numbers, self.field.toggle_block]
    
        
    def step(self):
        self.max_number_amount()
    
    def max_number_amount(self):
        self.field.working_number = self.working_number
        print(f"working number -> {self.working_number} step {self.steps % len(self.max_number_amount_steps)}")
        self.max_number_amount_steps[self.steps%len(self.max_number_amount_steps)]()
        self.steps += 1
        if self.steps % len(self.max_number_amount_steps) == 0:
            self.working_number += 1
    
    def missing_in_square(self):
        ...
    
    def missing_in_line(self):
        ...
