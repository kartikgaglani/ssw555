import unittest

# Your code for list_living_single function
def list_living_single(individual):
    living_singles = []
    for ind in individual:
        if 'AGE' in ind and 'DEAT' not in ind:
            age = ind['AGE']
            if age > 30 and 'FAMS' not in ind:
                living_singles.append(ind)
    return living_singles

# Test case for list_living_single function
class TestListLivingSingle(unittest.TestCase):

    def setUp(self):
        # Sample individual data with Marvel characters
        self.individual = [
            {
                'NAME': 'Tony Stark',
                'AGE': 40,
            },
            {
                'NAME': 'Natasha Romanoff',
                'AGE': 35,
                'FAMS': 'F1',
            },
            {
                'NAME': 'Steve Rogers',
                'AGE': 100,
            },
            {
                'NAME': 'Thor Odinson',
                'AGE': 1500,
                'DEAT': '2022-04-05',
            },
        ]

    def test_living_singles_found(self):
        result = list_living_single(self.individual)
        expected_output = [
            {
                'NAME': 'Tony Stark',
                'AGE': 40,
            },
            {
                'NAME': 'Steve Rogers',
                'AGE': 100,
            },
        ]
        self.assertEqual(result, expected_output)

    def test_no_living_singles(self):
        no_living_singles = [
            {
                'NAME': 'Natasha Romanoff',
                'AGE': 35,
                'FAMS': 'F1',
            },
            {
                'NAME': 'Thor Odinson',
                'AGE': 1500,
                'DEAT': '2022-04-05',
            },
        ]
        result = list_living_single(no_living_singles)
        self.assertEqual(result, [])

    def test_empty_input(self):
        result = list_living_single([])
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
