import unittest
from Task1_Roman_Numeral import RomanNumeral


class TestRomanNumeral(unittest.TestCase):

    def test_addition_valid(self):
        roman1 = RomanNumeral("IV")
        roman2 = RomanNumeral("VI")
        result = roman1 + roman2
        self.assertEqual(str(result), "X", "Сумма IV и VI должна быть X")

    def test_addition_invalid(self):
        roman1 = RomanNumeral("56")
        roman2 = RomanNumeral("VIII")
        with self.assertRaises(ValueError):
            result = roman1 + roman2

    def test_subtraction_valid(self):
        roman1 = RomanNumeral("X")
        roman2 = RomanNumeral("VI")
        result = roman1 - roman2
        self.assertEqual(str(result), "IV", "Разность X и VI должна быть IV")

    def test_subtraction_invalid(self):
        roman1 = RomanNumeral("56")
        roman2 = RomanNumeral("V")
        with self.assertRaises(ValueError):
            result = roman1 - roman2

    def test_multiplication_valid(self):
        roman1 = RomanNumeral("X")
        roman2 = RomanNumeral("IV")
        result = roman1 * roman2
        self.assertEqual(str(result), "XL", "Произведение X и IV должно быть XL")

    def test_multiplication_invalid(self):
        roman1 = RomanNumeral("45")
        roman2 = RomanNumeral("L")
        with self.assertRaises(ValueError):
            result = roman1 * roman2

    def test_division_valid(self):
        roman1 = RomanNumeral("XL")
        roman2 = RomanNumeral("V")
        result = roman1 / roman2
        self.assertEqual(str(result), "VIII", "Частное XL и V должно быть VIII")

    def test_division_by_zero(self):
        roman1 = RomanNumeral("XX")
        roman2 = RomanNumeral("O")
        with self.assertRaises(ValueError):
            result = roman1 / roman2

    def test_modulus_valid(self):
        roman1 = RomanNumeral("XVII")
        roman2 = RomanNumeral("V")
        result = roman1 % roman2
        self.assertEqual(str(result), "II", "Остаток от деления XVII на V должен быть II")

    def test_modulus_divide_by_zero(self):
        roman1 = RomanNumeral("X")
        roman2 = RomanNumeral("O")
        with self.assertRaises(ValueError):
            result = roman1 % roman2

if __name__ == "__main__":
    unittest.main()
