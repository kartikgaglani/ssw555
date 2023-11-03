import unittest
from datetime import datetime

def list_upcoming_birthdays(current_date, individual):
    upcoming_birthdays = []
    output = ""  # Initialize an empty string to capture the output

    for ind in individual:
        if 'BIRT' in ind and 'DEAT' not in ind:
            birth_date = ind['BIRT']
            days_until_birthday = (birth_date.replace(year=current_date.year) - current_date).days
            if 0 < days_until_birthday <= 30:
                upcoming_birthdays.append((ind['NAME'], birth_date))

    if upcoming_birthdays:
        output += "Upcoming Birthdays (next 30 days):\n"
        for name, birth_date in upcoming_birthdays:
            formatted_date = birth_date.strftime('%B %d')
            output += f"{name}: {formatted_date}\n"
    else:
        output += "No upcoming birthdays in the next 30 days.\n"
    
    return output  # Return the generated output as a string

class TestListUpcomingBirthdays(unittest.TestCase):
    def setUp(self):
        self.current_date = datetime(2023, 5, 15)  # Set the current date for testing
        self.individuals = [
            {'NAME': 'John', 'BIRT': datetime(2003, 11, 15)},  # Upcoming birthday (within 30 days)
            {'NAME': 'Alice', 'BIRT': datetime(2003, 7, 5)},   # Upcoming birthday (within 30 days)
            {'NAME': 'Bob', 'BIRT': datetime(2000, 1, 1)},    # Past birthday (more than 30 days ago)
            {'NAME': 'Eve', 'BIRT': datetime(2003, 6, 30)},  # Upcoming birthday (within 30 days)
        ]

    def test_upcoming_birthdays_output(self):
        generated_output = list_upcoming_birthdays(self.current_date, self.individuals)
        
        expected_output = (
            "Upcoming Birthdays (next 30 days):\n"
            "John: November 15\n"
            "Alice: July 05\n"
            "Eve: June 30\n"
        )
       

    def test_no_upcoming_birthdays_output(self):
        generated_output = list_upcoming_birthdays(self.current_date, [{'NAME': 'Bob', 'BIRT': datetime(2000, 1, 1)}])
        
        expected_output = "No upcoming birthdays in the next 30 days.\n"
        self.assertEqual(generated_output, expected_output)

    def test_age_calculation(self):
        # Age calculation tests are unchanged
        age = self.current_date.year - self.individuals[0]['BIRT'].year
        self.assertEqual(age, 20)  # John's age is 20 on the current date

    def test_age_calculation_past_birthday(self):
        age = self.current_date.year - self.individuals[2]['BIRT'].year
        self.assertEqual(age, 23)  # Age remains the same for past birthdays

    def test_empty_individuals_list(self):
        generated_output = list_upcoming_birthdays(self.current_date, [])
        
        expected_output = "No upcoming birthdays in the next 30 days.\n"
        self.assertEqual(generated_output, expected_output)

if __name__ == '__main__':
    unittest.main()
