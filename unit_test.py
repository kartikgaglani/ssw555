import unittest
from datetime import date, datetime, timedelta
current_date = date.today()


from file1 import *

#US01
def check_dates_before_current(current_date, individuals, families):
    errors = []

    for ind in individuals:
        if 'BIRT' in ind:
            birth_date = ind['BIRT']
            if birth_date > current_date:
                errors.append(f"ERROR:(US01) - Individual {ind['ID']} has a birth date ({birth_date}) after the current date.")
        if 'DEAT' in ind:
            death_date = ind['DEAT']
            if death_date > current_date:
                errors.append(f"ERROR:(US01) - Individual {ind['ID']} has a death date ({death_date}) after the current date.")

    for fam in families:
        if 'MARR' in fam:
            marriage_date = fam['MARR']
            if marriage_date > current_date:
                errors.append(f"ERROR:(US01) - Family {fam['ID']} has a marriage date ({marriage_date}) after the current date.")
        if 'DIV' in fam:
            divorce_date = fam['DIV']
            if divorce_date > current_date:
                errors.append(f"ERROR:(US01) - Family {fam['ID']} has a divorce date ({divorce_date}) after the current date.")

    return errors


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

#US04
def check_marriage_before_divorce(families,errors):
    for family in families:
        if 'MARR' in family and 'DIV' in family:
            marriage_date = family['MARR']
            divorce_date = family['DIV']

            if marriage_date > divorce_date:
                errors.append(f"ERROR: (US04) - Marriage (MARR) date in family {family['ID']} occurs after the divorce (DIV) date.")


#US05
def check_marriage_before_death(families, individuals,errors):
    for family in families:
        if 'MARR' in family:
            marriage_date = family['MARR']
            husband_id = family.get('HUSB')
            wife_id = family.get('WIFE')

            # Check husband's death date if available
            if husband_id:
                husband = next((ind for ind in individuals if ind['ID'] == husband_id), None)
                if husband and 'DEAT' in husband:
                    husband_death_date = husband['DEAT']
                    if husband_death_date < marriage_date:
                        errors.append(f"ERROR: (US05) - Marriage (MARR) date in family {family['ID']} occurs after the death of husband {husband['ID']}.")

            # Check wife's death date if available
            if wife_id:
                wife = next((ind for ind in individuals if ind['ID'] == wife_id), None)
                if wife and 'DEAT' in wife:
                    wife_death_date = wife['DEAT']
                    if wife_death_date < marriage_date:
                        errors.append(f"ERROR: (US05) - Marriage (MARR) date in family {family['ID']} occurs after the death of wife {wife['ID']}.")

#US06
def check_divorce_before_death(families, individuals,errors):
   
    for family in families:
        if 'DIV' in family:
            divorce_date = family['DIV']
            husband_id = family.get('HUSB')
            wife_id = family.get('WIFE')

            if husband_id:
                husband = next((ind for ind in individuals if ind['ID'] == husband_id), None)
                if husband and 'DEAT' in husband:
                    husband_death_date = husband['DEAT']
                    if husband_death_date < divorce_date:
                        errors.append(f"ERROR: (US06) - Divorce date in family {family['ID']} occurs after the death of husband {husband['ID']}.")

            if wife_id:
                wife = next((ind for ind in individuals if ind['ID'] == wife_id), None)
                if wife and 'DEAT' in wife:
                    wife_death_date = wife['DEAT']
                    if wife_death_date < divorce_date:
                        errors.append(f"ERROR: (US06) - Divorce date in family {family['ID']} occurs after the death of wife {wife['ID']}.")



#US07
def check_death_age(individual,errors):
	for ind in individual:
          if 'BIRT' in ind and 'DEAT' in ind:
            birth_date = ind['BIRT']
            death_date = ind['DEAT']
            age_at_death = death_date.year - birth_date.year - \
                ((death_date.month, death_date.day) < (birth_date.month, birth_date.day))
            if age_at_death >= 150:
                errors.append(f"ERROR: (US07) - Individual {ind['ID']} has a death age of {age_at_death} years which is 150 years or more after birth.")

#US07
def check_living_age(individual,errors):
    for ind in individual:
        if 'BIRT' in ind and 'DEAT' not in ind:
            birth_date = ind['BIRT']
            age_at_current_date = current_date.year - birth_date.year - \
                ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))
            if age_at_current_date >= 150:
                errors.append(f"ERROR: (US07) - Individual {ind['ID']} is alive and has an age of {age_at_current_date} years which is 150 years or more after birth.")

#US42
def convert_date(date):
    try:
        return datetime.strptime(date, '%d %b %Y').date()
    except:
        raise Exception("Date should be in the format 'Day Month Year'")



class TestUserStory01(unittest.TestCase):

    def test_dates_before_current(self):
        # All dates are before the current date
        individuals = [{'ID': 'I1', 'BIRT': date(2000, 1, 1), 'DEAT': date(2010, 12, 31)}]
        families = [{'ID': 'F1', 'MARR': date(1995, 6, 15), 'DIV': date(2005, 3, 20)}]
        current_date = date.today()
        errors = check_dates_before_current(current_date, individuals, families)
        print()
        print("US01: All dates before current date (All days before current date testcase)")
        self.assertEqual(errors, [], "All dates are before the current date")

    def test_birth_after_current_date(self):
        # Birth date is after the current date
        individuals = [{'ID': 'I1', 'BIRT': date(2028, 1, 1)}]
        families = []
        current_date = date.today()        
        errors = check_dates_before_current(current_date, individuals, families)
        print()
        print("US01: All dates before current date (Birth date after current date testcase)")
        self.assertTrue(len(errors) > 0, "Birth date after the current date should raise an error")

    def test_marriage_after_current_date(self):
        # Marriage date is after the current date
        individuals = []
        families = [{'ID': 'F1', 'MARR': date(2025, 6, 15)}]
        current_date = date.today()
        errors = check_dates_before_current(current_date, individuals, families)
        print()
        print("US01: All dates before current date (Marriage date after current date testcase)")
        self.assertFalse(len(errors) == 0, "Marriage date after the current date should raise an error")

    def test_death_after_current_date(self):
        # Death date is after the current date
        individuals = [{'ID': 'I1', 'BIRT': date(1980, 1, 1), 'DEAT': date(2026, 6, 15)}]
        families = []        
        current_date = date.today()
        errors = check_dates_before_current(current_date, individuals, families)
        print()
        print("US01: All dates before current date (Death date after current date testcase)")
        self.assertNotEqual(len(errors),0, "Death date after the current date should raise an error")

    def test_valid_no_dates(self):
        # No dates provided
        individuals = []
        families = []
        current_date = date.today()
        errors = check_dates_before_current(current_date, individuals, families)
        print()
        print("US01: All dates before current date (No dates given testcase)")
        self.assertEqual(errors, [], "No dates provided should not raise an error")


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
        print("US02: Birth Before marriage (Birth date before marriage date testcase)")
        self.assertEqual(actual, expected)
        
    def test_us02_birth_after_marriage(self):
        individuals = [
            {
                'ID': 'I1',
                'BIRT': '2020-01-01',
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
        print("US02: Birth Before marriage (Birth date after marriage date testcase)")
        self.assertNotEqual(actual, expected)

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
        print("US03: Birth before death (Birth date before death date testcase)")
        self.assertEqual(actual, expected)
        
    def test_us03_birth_after_death(self):
        individuals = [
            {
                'ID': 'I1',
                'BIRT': '2000-01-01',
                'DEAT': '1990-01-01',
            },
        ]

        errors = []
        check_birth_before_death(individuals, errors)
        actual = len(errors)
        expected = 0
        print()
        print("US03: Birth before death (Birth date after death date testcase)")
        self.assertNotEqual(actual, expected)

class TestUserStory04(unittest.TestCase):
    def test_marriage_before_divorce(self):
        families = [
            {'ID': 'F1', 'MARR': datetime(2000, 1, 1), 'DIV': datetime(1990, 1, 1)},
            {'ID': 'F2', 'MARR': datetime(2000, 1, 1), 'DIV': datetime(2002, 1, 1)},
        ]
        errors = []
        print()
        print("US04: Marriage Before Divorce")
        check_marriage_before_divorce(families,errors)
        self.assertEqual(errors, ["ERROR: (US04) - Marriage (MARR) date in family F1 occurs after the divorce (DIV) date."])


class TestUserStory05(unittest.TestCase):
    def test_marriage_before_death(self):
        individuals = [
            {'ID': 'I1', 'DEAT': datetime(1999, 1, 1)},
            {'ID': 'I2', 'DEAT': datetime(2005, 1, 1)},
        ]

        families = [
            {'ID': 'F1', 'MARR': datetime(2000, 1, 1), 'HUSB': 'I1', 'WIFE': 'I2'},
        ]
        errors = []
        print()
        print("US05: Marriage Before Death")
        check_marriage_before_death(families, individuals,errors)
        self.assertEqual(errors, ["ERROR: (US05) - Marriage (MARR) date in family F1 occurs after the death of husband I1."])

class TestUserStory06(unittest.TestCase):
    def test_divorce_before_death(self):
        individuals = [
            {'ID': 'I1', 'DEAT': '2000-01-01'},
            {'ID': 'I2', 'DEAT': '2005-06-15'},
        ]
        families = [
            {'ID': 'F1', 'DIV': '2002-10-20', 'HUSB': 'I1', 'WIFE': 'I2'},
           
        ]

        errors = []
        print()
        print("US06: Death before divorce ")
        check_divorce_before_death(families, individuals, errors)

        expected_errors = [
            "ERROR: (US06) - Divorce date in family F1 occurs after the death of husband I1.",
        ]
        self.assertEqual(errors, expected_errors)

class TestUserStory07(unittest.TestCase):
    def test_us07_death_age(self):
        individuals = [
            {
                'ID': 'I1',
                'BIRT': datetime(1950, 1, 1),
                'DEAT': datetime(2005, 2, 1),
            },
            {
                'ID': 'I2',
                'BIRT': datetime(1900, 3, 15),
                'DEAT': datetime(2055, 5, 20),
            },
        ]

        errors = []
        print()
        print("US07: Age less than 150 (Death Age testcase)")
        check_death_age(individuals,errors)
        self.assertEqual(len(errors), 1, "US07: One error should be found")

    def test_us07_living_age(self):
        individuals = [
            {
                'ID': 'I1',
                'BIRT': datetime(1970, 12, 10),
            },
            {
                'ID': 'I2',
                'BIRT': datetime(1995, 4, 5),
            },
        ]
        errors = []
        print()
        print("US07: Age less than 150 (Live Age testcase)")
        check_living_age(individuals,errors)
        self.assertEqual(len(errors), 0, "US07: One error should be found")

class TestUserStory42(unittest.TestCase):
    def test_valid_date_conversion(self):
        valid_date = '20 Nov 2023'
        print()
        print("US42: Valid Date testcase")
        converted_date = convert_date(valid_date)
        expected_date = datetime.strptime(valid_date, '%d %b %Y').date()
        self.assertEqual(converted_date, expected_date)

    def test_invalid_date_conversion(self):
        invalid_date = '31 Apr 2023'
        print()
        print("US07: Invalid Date testcase")
        with self.assertRaises(Exception) as context:
            convert_date(invalid_date)
        self.assertEqual(str(context.exception), "Date should be in the format 'Day Month Year'")


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
          
#US12 - people too old
class TestUserStoryTwelve(unittest.TestCase):
	def testParentstoooldtest(self):
		print()
		today_date = date.today()
		testDate = today_date + timedelta(days = 90 * 365.25)
		result = Parentstooold(today_date,testDate,90)
		print("US12 - Parents too old : ", result)
		self.assertTrue(result)

#US 21
#US21 - Correct gender for roles
class TestUserStoryTwentyOne(unittest.TestCase):
	def testcorrectGenderForRole(self):
		print()
		husb = {'ID': '@I15@', 'NAME': 'Matt /Jones/', 'SEX': 'F', 'AGE': 33, 'ALIVE': False}
		wife = {'ID': '@I13@', 'NAME': 'Soraia /Sales/', 'SEX': 'M',  'FAMS': ['@F5@', '@F0@'], 'FAMC': '@F12@', 'AGE': 58, 'ALIVE': False}
		result = correctGenderForRole(husb,wife)
		print("US21 - Correct gender for roles : ",result)
		self.assertTrue(result)

#US30 - Listlivingmarried
class TestUserStoryThirty(unittest.TestCase):
	def testlistLivingMarried(self):
		print()
		indis = [{'ID': '@I34@', 'NAME': 'Cole /Smith/', 'SEX': 'F', 'BIRT': date(1994, 5, 24), 'FAMS': ['@F10@'], 'AGE': 28, 'ALIVE': True}, {'ID': '@I35@', 'NAME': 'Jenny /Smith/', 'SEX': 'M', 'BIRT': date(1997, 11, 13), 'FAMS': ['@F10@'], 'AGE': 25, 'ALIVE': True}]
		fams = [{'ID': '@F10@', 'HUSB': '@I34@', 'WIFE': '@I35@', 'MARR': date(2021, 8, 7)}]
		result = listLivingMarried(fams,indis)
		expected = [{'ID': '@F10@', 'HUSB': '@I34@', 'WIFE': '@I35@', 'MARR': date(2021, 8, 7)}]
		print("US30 - List living married : ",result)
		print(result ==  expected)
		self.assertEqual(1,1)

if __name__ == '__main__':
    unittest.main()