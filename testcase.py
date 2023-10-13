from datetime import date

def list_upcoming_anniversaries(current_date, families, individuals):
    upcoming_anniversaries = []

    for fam in families:
        if 'MARR' in fam:
            marriage_date = fam['MARR']
            anniversary_date = marriage_date.replace(year=current_date.year)
            if anniversary_date >= current_date:
                days_until_anniversary = (anniversary_date - current_date).days
                if 0 <= days_until_anniversary <= 30:
                    husband_id = fam['HUSB']
                    wife_id = fam['WIFE']

                    husband = next((ind for ind in individuals if ind['ID'] == husband_id), None)
                    wife = next((ind for ind in individuals if ind['ID'] == wife_id), None)

                    if husband and wife and 'DEAT' not in husband and 'DEAT' not in wife:
                        upcoming_anniversaries.append((husband['NAME'], wife['NAME'], anniversary_date))

    if upcoming_anniversaries:
        output = "Upcoming Anniversaries (next 30 days) for living couples:\n"
        for husband, wife, anniversary_date in upcoming_anniversaries:
            output += f"{husband} and {wife}: {anniversary_date.strftime('%B %d')}\n"
        return output.strip()
    else:
        return "No upcoming anniversaries in the next 30 days for living couples."

# Unit tests

import unittest

class TestListUpcomingAnniversaries(unittest.TestCase):

    def test_no_upcoming_anniversaries(self):
        current_date = date(2023, 10, 1)
        families = []
        individuals = []
        result = list_upcoming_anniversaries(current_date, families, individuals)
        self.assertEqual(result, "No upcoming anniversaries in the next 30 days for living couples.")

    def test_one_upcoming_anniversary(self):
        current_date = date(2023, 10, 15)
        families = [
            {
                "ID": "F1",
                "HUSB": "I1",
                "WIFE": "I2",
                "MARR": date(2023, 10, 30),
            }
        ]
        individuals = [
            {"ID": "I1", "NAME": "John Doe"},
            {"ID": "I2", "NAME": "Jane Smith"},
        ]
        expected_output = "Upcoming Anniversaries (next 30 days) for living couples:\n"
        expected_output += "John Doe and Jane Smith: October 30"
        result = list_upcoming_anniversaries(current_date, families, individuals)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
