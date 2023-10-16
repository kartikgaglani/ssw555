import unittest

from tabulate import tabulate
from datetime import date, datetime, timedelta

#US09
def check_birth_before_parent_death(individuals, families):

    birth_dates = {ind['ID']: ind.get('BIRT') for ind in individuals}
    death_dates = {ind['ID']: ind.get('DEAT') for ind in individuals}

    for family in families:
        if 'CHIL' in family:
            children = family['CHIL']
            mother_id = family.get('WIFE')
            father_id = family.get('HUSB')

            mother_death_date = death_dates.get(mother_id)
            father_death_date = death_dates.get(father_id)

            for child_id in children:
                birth_date = birth_dates.get(child_id)

                if mother_death_date and birth_date and birth_date > mother_death_date:
                    errors.append(f"ERROR: (US09) - Child {child_id} was born after the death of the mother {mother_id}.")

                if father_death_date and birth_date:
                    difference = (birth_date.year - father_death_date.year) * 12 + birth_date.month - father_death_date.month
                    if difference > 9:
                        errors.append(f"ERROR: (US09) - Child {child_id} was born more than 9 months after the death of the father {father_id}.")

#US15
def fewer_than_15_siblings(families):
    invalid = False
    for family_id, family_data in families.items():
        siblings = get_all_individual_data_by_key(families, family_id, 'CHIL')
        if len(siblings) > 15:
            invalid = True
            print(f"ERROR: US15: Family has more than 15 siblings")
    return invalid


# Unit tests
#unit test for US09

class TestCheckBirthBeforeParentDeath(unittest.TestCase):

    def test_birth_before_parent_death(self):
        individuals = [
                        {'ID': 'I1', 'NAME': 'Dev /Naik/', 'SEX': 'M', 'BIRT': '1995-04-19', 'FAMC': '@F1@', 'AGE': 28, 'ALIVE': True, 'FAMS': [], 'DEAT': ''},
            {'ID': 'I2', 'NAME': 'Sandhya /Naik/', 'SEX': 'F', 'BIRT': '1968-12-08', 'FAMC': '@F2@', 'AGE': 54, 'ALIVE': True, 'FAMS': ['@F1@'], 'DEAT': ''},
            {'ID': 'I3', 'NAME': 'Sandip /Naik/', 'SEX': 'M', 'BIRT': '1964-04-05', 'FAMC': '@F3@', 'AGE': 59, 'ALIVE': True, 'FAMS': ['@F1@'], 'DEAT': ''},
            
        ]

        families_data = [
            {'ID': '@F1@', 'WIFE': 'I2', 'HUSB': 'I3', 'CHIL': ['I1', 'I4'], 'MARR': '1995-05-30', 'DIV': '2005-02-06'},
            
        ]

        #Function check_birth_before_parent_death returns a list of errors or an empty list
        errors = check_birth_before_parent_death(individuals_data, families_data)

        # Assert that there are no errors in the list
        self.assertEqual(errors, [], "No errors should be found in birth before parent death validation.")
    
    def test_birth_after_mother_death(selfb):
        individuals_data = [
            {'ID': 'I1', 'NAME': 'Dev /Naik/', 'SEX': 'M', 'BIRT': '1995-04-19', 'FAMC': '@F1@', 'AGE': 28, 'ALIVE': True, 'FAMS': [], 'DEAT': ''},
            {'ID': 'I2', 'NAME': 'Sandhya /Naik/', 'SEX': 'F', 'BIRT': '1968-12-08', 'FAMC': '@F2@', 'AGE': 54, 'ALIVE': False, 'FAMS': ['@F1@'], 'DEAT': '2020-02-15'},
        ]

        families_data = [
            {'ID': '@F1@', 'WIFE': 'I2', 'HUSB': 'I3', 'CHIL': ['I1'], 'MARR': '1995-05-30', 'DIV': '2005-02-06'},
        ]

        # Assuming your function check_birth_before_parent_death returns a list of errors or an empty list
        errors = check_birth_before_parent_death(individuals_data, families_data)

        # Assert that there are no errors in the list
        selfb.assertEqual(errors, [], "No errors should be found in birth after mother's death validation.")


#unit test for US15
class TestFewerThan15Siblings(unittest.TestCase):
    def test_valid_case(self):
        
        families = {
            '@F1@': {
                'CHIL': ['@I1@', '@I4@']
            }
        }
        result = fewer_than_15_siblings(families)
        self.assertFalse(result)  # Expecting False

    def test_invalid_case(self):
       
        families = {
            '@F2@': {
                'CHIL': ['@I1@', '@I2@', '@I3@', '@I4@', '@I5@', '@I6@', '@I7@', '@I8@', '@I9@', '@I10@', '@I11@', '@I12@', '@I13@', '@I14@', '@I15@', '@I16@']
            }
        }
        result = fewer_than_15_siblings(families)
        self.assertTrue(result)  # Expecting True

if __name__ == '__main__':
    unittest.main()




