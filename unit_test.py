import unittest

from file1 import *


class TestUserStoryTwentyFive(unittest.TestCase):
	
    #Unit test of US 25
	
	def test_family_names_success(self):
		print()
		actual = family_output(names = ['Sandip /Naik/', 'Sandhya /Naik/','Sandip /Naik/','Dev /Naik/', 'Ajay /Naik/'])
		expected = {'Sandip'}
		print("US25 - Unique first names in families")
		print(actual, expected, actual == expected)
		self.assertEqual(actual, expected)
	
	def test_family_names_not_equal(self):
		print()
		actual = family_output(names = ['Sandip /Naik/', 'Sandhya /Naik/','Dev /Naik/', 'Ajay /Naik/'])
		expected = {'Sandip'}
		print("US25 - Unique first names in families")
		print(actual, expected, actual == expected)
		self.assertNotEqual(actual, expected)

	def test_family_names_is_not_equal(self):
		print()
		actual = family_output(names = ['Sandip /Naik/', 'Sandhya /Naik/','Sandip /Naik/','Dev /Naik/', 'Ajay /Naik/'])
		expected = {'Devanand /Naik/'}
		print("US25 - Unique first names in families")
		print(actual, expected, actual == expected)
		self.assertNotEqual(actual, expected)

	def test_family_names_empty_set(self):
		print()
		actual = family_output(names = ['Tulsidas /More/', 'Kashibai /More/','Sandhya /Naik/', 'Vaishnavi /More/'])
		expected = set()
		print("US25 - Unique first names in families")
		print(actual, expected, actual == expected)
		self.assertEqual(actual, expected)

	def test_family_names_not_eq(self):
		print()
		actual = family_output(names = [])
		expected = {'Tulsidas /More/', 'Kashibai /More/','Sandhya /Naik/', 'Vaishnavi /More/'}
		print("US25 - Unique first names in families")
		print(actual, expected, actual == expected)
		self.assertNotEqual(actual, expected)
		
    # Unit test for US 08
class TestUserStoryEight(unittest.TestCase):

	def test_birth_before_marr(self):
		print()
		birth = date.today()
		marriage = birth + timedelta(days = 365)
		print("US08 - Birth before the marriage of parents")
		print("Birth :" ,birth," Marriage : ",marriage, birth_before_marriage(birth, marriage))
		self.assertTrue(birth_before_marriage(marriage, birth))

	def test_birth_after_marr(self):
		print()
		birth = date.today()
		marriage = birth - timedelta(days = 365)
		print("US08 - Birth before the marriage of parents")
		print("Birth :" ,birth," Marriage : ", marriage, birth_before_marriage(birth, marriage))
		self.assertFalse(birth_before_marriage(marriage, birth))
	
	def test_birth_div(self):
		print()
		birth = date.today()
		divorce = birth - timedelta(days = 270)
		print("US08 - Birth before the marriage of parents (no more than 9 months after their divorce)")

		print("Birth :" ,birth," Divorce : ", divorce, birth_before_divorce(birth, divorce))
		self.assertFalse(birth_before_divorce(birth, divorce + timedelta(days = 270)))
	
	def test_birth_div_after(self):
		print()
		birth = date.today()
		divorce = birth - timedelta(days = 365)
		print("US08 - Birth before the marriage of parents (no more than 9 months after their divorce)")
		print("Birth :" ,birth," Divorce : ", divorce, birth_before_divorce(birth, divorce))
		self.assertFalse(birth_before_divorce(birth, divorce + timedelta(days = 270)))
