import unittest

from tabulate import tabulate
from datetime import date, datetime, timedelta

# US17
def parents_should_not_marry_descendants(individuals, families):
    invalid = False
    for ind_id in individuals:
        children_ids = get_all_data_of_a_person(families, ind_id, 'CHIL')
        for child_id in children_ids:
            for family_id in families:
                husb_id = get_family_data_by_key(families, family_id, 'HUSB')
                wife_id = get_family_data_by_key(families, family_id, 'WIFE')

                if ((ind_id == husb_id) and (child_id == wife_id) or (ind_id == wife_id) and (child_id == husb_id)):
                    invalid = True
                    print(f"ERROR: US17: Parent is married to their descendant")
    return invalid

# US18
def sibling_should_not_marry(families):
    invalid = False
    husb_wives = get_all_husband_and_wives(families)
    for family_id, family_data in families.items():
        sibling_ids = get_all_individual_data_by_key(families, family_id, 'CHIL')
        for hub_id, wife_id in husb_wives:
            if (hub_id in sibling_ids) and (wife_id in sibling_ids):
                invalid = True
                print(f"ERROR: US18: Siblings {hub_id} and {wife_id} should not marry.")
    return invalid

# unit test for us 17
class TestNoMarriage(unittest.TestCase):
    
    def test_valid_marriage(self):
        # Test a valid marriage between non-descendants
        self.assertTrue(self.validator.is_marriage_valid("I2", "I3"))

    def test_invalid_marriage(self):
        # Test an invalid marriage between a parent and a descendant
        self.assertFalse(self.validator.is_marriage_valid("I2", "I1"))

    def test_valid_marriage_same_person(self):
        # Test a valid marriage when the husband and wife are the same person
        self.assertTrue(self.validator.is_marriage_valid("I1", "I1"))

# unit test for us 18
class TestSiblingsshouldnotMarry(unittest.TestCase):
    
    def test_valid_marriage(self):
        # Test a valid marriage between non-descendant individuals
        self.assertTrue(self.validator.is_marriage_valid("I2", "I3"))

    def test_invalid_marriage(self):
        # Test an invalid marriage between a parent and a descendant
        self.assertFalse(self.validator.is_marriage_valid("I2", "I1"))

    def test_valid_marriage_same_person(self):
        # Test a valid marriage when the husband and wife are the same person
        self.assertTrue(self.validator.is_marriage_valid("I1", "I1"))

   
if __name__ == '__main__':
    unittest.main()
