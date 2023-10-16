import unittest

from file1 import *

#US02
def check_birth_before_marriage(individuals, families, errors):
    family_marriage_dates = {fam['ID']: fam.get('MARR') for fam in families}

    for ind in individuals:
        if 'BIRT' in ind and 'FAMS' in ind:
            birth_date = ind['BIRT']
            family_ids = ind['FAMS']
            for fam_id in family_ids:
                marriage_date = family_marriage_dates.get(fam_id)
                if marriage_date and birth_date > marriage_date:
                    errors.append(f"ERROR: (US02) - Birth of individual {ind['ID']} occurred after their marriage in family {fam_id}.")

#US03
def check_birth_before_death(individuals,errors):
    for ind in individuals:
        if 'BIRT' in ind and 'DEAT' in ind:
            birth_date = ind['BIRT']
            death_date = ind['DEAT']
            if birth_date > death_date:
                errors.append(f"ERROR: (US03) -  Birth of individual {ind['ID']} occurred after their death.")

class TestUserStory02(unittest.TestCase):
    def test_us02_birth_before_marriage(self):
        individuals = [
            {
                'ID': 'I1',
                'BIRT': '2000-01-01',
                'FAMS': ['F1'],
            },
        ]

        families = [
            {
                'ID': 'F1',
                'MARR': '2015-01-01',
            },
        ]

        errors = []
        check_birth_before_marriage(individuals, families, errors)
        actual = len(errors)
        expected = 0
        print()
        print("US02: Birth Before Marriage.")
        self.assertEqual(actual, expected)

class TestUserStory03(unittest.TestCase):
    def test_us03_birth_before_death(self):
        individuals = [
            {
                'ID': 'I1',
                'BIRT': '2000-01-01',
                'DEAT': '2020-01-01',
            },
        ]

        errors = []
        check_birth_before_death(individuals, errors)
        actual = len(errors)
        expected = 0
        print()
        print("US03: Birth before death")
        self.assertEqual(actual, expected)

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

if __name__ == '__main__':
    unittest.main()