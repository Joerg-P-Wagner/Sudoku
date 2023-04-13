

class SudokuTask:
    def __init__(self):
        ...


class Field:
    def __init__(self) -> None:
        self.number_amount = {x:0 for x in range(1,10)}
        self.sub_fields = [[SubField(sub_field_coords=(x,y)) for y in range(3)] for x in range(3)]
        self.unblocked = []
    
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

    def set_numbers(self, number, coords, is_start_number=False):
        for coord in coords:
            self.sub_fields[coord[0][0]][coord[0][1]].set_numbers(number, coord[1], is_start_number)


class SubField:
    def __init__(self, sub_field_coords) -> None:
        self.coords = sub_field_coords
        self.single_fields = [[SingleField(single_field_coords=(sub_field_coords,(x,y))) for y in range(3)] for x in range(3)]
        self.blocked = False

    def set_numbers(self, n, coords, is_start_number) -> None:
        self.single_fields[coords[0]][coords[1]].number = n
        self.single_fields[coords[0]][coords[1]].is_start_number = is_start_number
    
    def get_numbers(self) -> list:
        return [ single_field.number for sl in self.single_fields for single_field in sl if single_field.number ]


class SingleField:
    def __init__(self, single_field_coords) -> None:
        self.__number = None
        self.__is_start_number = False
        self.__is_blocked = False
        self.__coords = single_field_coords
    
    @property
    def number(self) -> int:
        return self.__number
    
    @number.setter
    def number(self, n: int) -> None:
        self.__number = n
        self.is_blocked = True if n else False
    
    @property
    def is_start_number(self) -> bool:
        return self.__is_start_number
    
    @is_start_number.setter
    def is_start_number(self, b: bool) -> None:
        self.__is_start_number = b
    
    @property
    def is_blocked(self) -> None:
        return self.__is_blocked
    
    @is_blocked.setter
    def is_blocked(self, b: bool) -> None:
        self.__is_blocked = b
    
    @property
    def coords(self) -> tuple:
        return self.__coords
