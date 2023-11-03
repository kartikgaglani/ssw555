import unittest


def male_last_names(individuals, families):
    last_name_errors = []

    for family in families:
        if 'HUSB' in family:
            husband_id = family['HUSB']
            husband = [ind for ind in individuals if ind['ID'] == husband_id][0]
            husband_gender = husband.get('SEX')
            husband_last_name = husband.get('NAME').split()[-1]

            if husband_gender == 'M':
                for child_id in family.get('CHIL', []):
                    child = [ind for ind in individuals if ind['ID'] == child_id][0]
                    if child.get('SEX') == 'M':
                        child_last_name = child.get('NAME').split()[-1]
                        if husband_last_name != child_last_name:
                            error = f"ERROR: US16 - All male members in the family (e.g., {husband['NAME']} and {child['NAME']}) should have the same last name."
                            last_name_errors.append(error)

    return last_name_errors

# Unit tests
class TestMaleLastNames(unittest.TestCase):
    def test_all_male_members_same_last_name(self):
        individuals = [
            {'ID': 'I01', 'NAME': 'Adam Wills', 'SEX': 'M'},
            {'ID': 'I02', 'NAME': 'Mike Wills', 'SEX': 'M'},
        ]
        families = [
            {'HUSB': 'I01', 'CHIL': ['I02']},
        ]
        errors = male_last_names(individuals, families)
        self.assertEqual(errors, [])

    def test_all_male_members_different_last_names(self):
        individuals = [
            {'ID': 'I01', 'NAME': 'Adam Wills', 'SEX': 'M'},
            {'ID': 'I02', 'NAME': 'Mike Johnson', 'SEX': 'M'},
        ]
        families = [
            {'HUSB': 'I01', 'CHIL': ['I02']},
        ]
        errors = male_last_names(individuals, families)
        self.assertEqual(len(errors), 1)
        self.assertIn('Mike Johnson', errors[0])
        self.assertIn('Adam Wills', errors[0])

    def test_male_and_female_members(self):
        individuals = [
            {'ID': 'I01', 'NAME': 'Adam Wills', 'SEX': 'M'},
            {'ID': 'I02', 'NAME': 'Athena Wills', 'SEX': 'F'},
        ]
        families = [
            {'HUSB': 'I01', 'WIFE': 'I02'},
            {'CHIL': ['I01', 'I02']},
        ]
        errors = male_last_names(individuals, families)
        self.assertEqual(errors, [])

 

if __name__ == '__main__':
    unittest.main()
