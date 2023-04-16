

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
        self.number_amount['total'] = 0
        for x in self.sub_fields:
            for sub_field in x:
                for y in sub_field.single_fields:
                    for single_field in y:
                        if single_field.number:
                            self.number_amount[single_field.number] += 1
                            self.number_amount['total'] += 1

    def set_numbers(self, number, coords, is_start_number=False, is_expected=False):
        for coord in coords:
            self.sub_fields[coord[0][0]][coord[0][1]].set_numbers(number, coord[1], is_start_number, is_expected)


class SubField:
    def __init__(self, sub_field_coords) -> None:
        self.coords = sub_field_coords
        self.single_fields = [[SingleField(coords=(sub_field_coords,(x,y))) for y in range(3)] for x in range(3)]
        self.blocked = False

    def set_numbers(self, n, coords, is_start_number, is_expected) -> None:
        if is_expected:
            self.single_fields[coords[0]][coords[1]].expected_number = n
        else:
            self.single_fields[coords[0]][coords[1]].number = n
            self.single_fields[coords[0]][coords[1]].is_start_number = is_start_number
            self.single_fields[coords[0]][coords[1]].is_single_free_field = False
    
    def get_numbers(self) -> list:
        return [ single_field.number for sl in self.single_fields for single_field in sl if single_field.number ]


class SingleField:
    def __init__(self, coords) -> None:
        self.__coords = coords
        self.__number = None
        self.__is_start_number = False
        self.__is_blocked = False
        self.__expected_number = None
        self.__is_expected_blocked = False
        self.__is_single_free_field = False
    
    @property
    def coords(self) -> tuple:
        return self.__coords
    
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
    def is_blocked(self) -> bool:
        return self.__is_blocked
    
    @is_blocked.setter
    def is_blocked(self, b: bool) -> None:
        self.__is_blocked = b
    
    @property
    def expected_number(self) -> int:
        return self.__expected_number
    
    @expected_number.setter
    def expected_number(self, n: int) -> None:
        self.__expected_number = n
    
    @property
    def is_expected_blocked(self) -> bool:
        return self.__is_expected_blocked
    
    @is_expected_blocked.setter
    def is_expected_blocked(self, b: bool) -> None:
        self.__is_expected_blocked = b

    @property
    def is_single_free_field(self) -> bool:
        return self.__is_single_free_field
    
    @is_single_free_field.setter
    def is_single_free_field(self, b: bool) -> None:
        self.__is_single_free_field = b
    
    
