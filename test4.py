import unittest

from tabulate import tabulate
from datetime import date, datetime, timedelta

#US 36
def list_recent_deaths(current_date, individuals):
    recent_deaths = []

    for individual in individuals:
        death_date = get_death_date(individual)
        if death_date:
            days_since_death = (current_date - death_date).days
            if 0 <= days_since_death <= 30:
                recent_deaths.append(individual)

    return recent_deaths

#US 38
def list_upcoming_birthdays(current_date, individuals):
    upcoming_birthdays = []

    for individual in individuals:
        birth_date = get_birth_date(individual)
        if birth_date:
            days_until_birthday = (birth_date - current_date).days
            if 0 <= days_until_birthday <= 30:
                upcoming_birthdays.append(individual)

    return upcoming_birthdays

#unit test for us 36
class TestListRecentDeaths(unittest.TestCase):
    def test_valid_recent_death(self):
        expected_recent_deaths = [
            IndividualElement(id="I1", name="Dev Naik", death_date="2023-11-10"),
            # Add more expected results as needed
        ]
        actual_recent_deaths = list_people_died_last_30_days(self.test_gedcom_file_path)

        self.assertEqual(len(actual_recent_deaths), len(expected_recent_deaths))

        for actual, expected in zip(actual_recent_deaths, expected_recent_deaths):
            self.assertEqual(actual.get_id(), expected.get_id())
            self.assertEqual(actual.get_name(), expected.get_name())
            self.assertEqual(get_death_date(actual), datetime.strptime(expected.death_date, "%Y-%m-%d").date())

#unit test for us 38
class TestListUpcomingBirthdays(unittest.TestCase):
    def test_upcoming_birthdays_exist(self):
        expected_upcoming_birthdays = [
            IndividualElement(id="I1", name="Dev Naik", birth_date="2023-11-05"),
            
        ]
        actual_upcoming_birthdays = list_living_people_upcoming_birthdays(self.test_gedcom_file_path)

        self.assertEqual(len(actual_upcoming_birthdays), len(expected_upcoming_birthdays))

        for actual, expected in zip(actual_upcoming_birthdays, expected_upcoming_birthdays):
            self.assertEqual(actual.get_id(), expected.get_id())
            self.assertEqual(actual.get_name(), expected.get_name())
            self.assertEqual(get_birth_date(actual), datetime.strptime(expected.birth_date, "%Y-%m-%d").date())

    def test_no_upcoming_birthdays(self):
        expected_upcoming_birthdays = []
        actual_upcoming_birthdays = list_living_people_upcoming_birthdays(self.test_gedcom_file_path)

        self.assertEqual(actual_upcoming_birthdays, expected_upcoming_birthdays)


        
if __name__ == '__main__':
    unittest.main()