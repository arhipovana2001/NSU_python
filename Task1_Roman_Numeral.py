import math


class RomanNumeral:
    """Класс представляет Римское число"""

    def __init__(self, roman_num):
        """Метод инициализации"""
        self.roman_num = roman_num
        self.roman_num_bool = None
        if self.is_valid():
            self.int_value = self.to_int()

    def __repr__(self):
        return str(self.roman_num)

    def __str__(self):
        return str(self.roman_num)

    def is_valid(self):
        if isinstance(self.roman_num, int):
            return True
        roman_numerals = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }
        prev_value = 0
        sum_num = 0

        for char in self.roman_num:
            if char not in roman_numerals:
                self.roman_num_bool = False
                return False

            current_value = roman_numerals[char]

            if current_value > prev_value:
                sum_num += current_value - 2 * prev_value
            else:
                sum_num += current_value

            prev_value = current_value
        self.roman_num_bool = True
        return True

    def to_int(self):
        """Перевод римского числа в арабское"""
        roman_dict = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        int_value = 0
        prev_value = 0

        for char in reversed(self.roman_num):
            value = roman_dict[char]
            if value < prev_value:
                int_value -= value
            else:
                int_value += value
            prev_value = value

        return int_value

    @staticmethod
    def to_roman(number):
        """Перевод арабского числа в римское"""
        total = ''
        int_ = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        rom_ = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']
        for int_val, roman_val in zip(int_, rom_):
            total += (number // int_val) * roman_val
            number %= int_val
        return total

    def __add__(self, other):
        """Операция сложения"""
        if not self.roman_num_bool or not other.roman_num_bool:
            raise ValueError("Both Roman numerals must be valid for addition")

        result_int = self.int_value + other.int_value
        result_roman = RomanNumeral.to_roman(result_int)
        return RomanNumeral(result_roman)

    def __sub__(self, other):
        """Операция вычитания"""
        if not self.roman_num_bool or not other.roman_num_bool:
            raise ValueError("Both Roman numerals must be valid for addition")

        result_int = self.int_value - other.int_value
        result_roman = RomanNumeral.to_roman(result_int)
        return RomanNumeral(result_roman)

    def __mul__(self, other):
        """Операция умножения"""
        if not self.roman_num_bool or not other.roman_num_bool:
            raise ValueError("Both Roman numerals must be valid for addition")

        result_int = self.int_value * other.int_value
        result_roman = RomanNumeral.to_roman(result_int)
        return RomanNumeral(result_roman)

    def __truediv__(self, other):
        """Операция деления"""
        if not self.roman_num_bool or not other.roman_num_bool:
            raise ValueError("Both Roman numerals must be valid for division")

        result_int = self.int_value // other.int_value
        result_roman = RomanNumeral.to_roman(result_int)
        return RomanNumeral(result_roman)

    def __mod__(self, other):
        """Операция остатка от деления"""
        if not self.roman_num_bool or not other.roman_num_bool:
            raise ValueError("Both Roman numerals must be valid for division")

        result_int = self.int_value % other.int_value
        result_roman = RomanNumeral.to_roman(result_int)
        return RomanNumeral(result_roman)


roman1 = RomanNumeral('XXX')
print(roman1.is_valid())
print(roman1.to_int())
print(roman1)

a = 12
print(RomanNumeral.to_roman(a))

roman2 = RomanNumeral('XXII')
print(roman2.int_value)
print(roman2)
print(roman1 + roman2)
print(roman1 - roman2)
print(roman1 * roman2)
print(roman1 / roman2)
print(roman1 % roman2)
