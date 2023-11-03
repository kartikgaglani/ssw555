import unittest
from datetime import datetime
from io import StringIO
from unittest.mock import patch

def list_upcoming_birthdays(current_date, individual):
    upcoming_birthdays = []
    output = ""

    for ind in individual:
        if 'BIRT' in ind and 'DEAT' not in ind:
            birth_date = ind['BIRT']
            days_until_birthday = (birth_date.replace(year=current_date.year) - current_date).days
            if 0 < days_until_birthday <= 30:
                upcoming_birthdays.append((ind['NAME'], birth_date))

    if upcoming_birthdays:
        output += "Upcoming Birthdays (next 30 days):\n"
        for name, birth_date in upcoming_birthdays:
            formatted_date = format_date(birth_date)
            output += f"{name}: {formatted_date}\n"
    else:
        output += "No upcoming birthdays in the next 30 days.\n"
    
    return output

def format_date(date):
    return date.strftime('%B %d')

class TestListUpcomingBirthdays(unittest.TestCase):
    def setUp(self):
        self.current_date = datetime(2023, 5, 15)
        self.individuals = [
            {'NAME': 'John', 'BIRT': datetime(2003, 11, 15)},
            {'NAME': 'Alice', 'BIRT': datetime(2003, 7, 5)},
            {'NAME': 'Bob', 'BIRT': datetime(2000, 1, 1)},
            {'NAME': 'Eve', 'BIRT': datetime(2003, 6, 30)},
        ]

    def test_upcoming_birthdays_output(self):
        with patch('sys.stdout', new_callable=StringIO) as captured_output:
            list_upcoming_birthdays(self.current_date, self.individuals)
            output = captured_output.getvalue()
        
        expected_output = (
            "Upcoming Birthdays (next 30 days):\n"
            "John: November 15\n"
            "Alice: July 05\n"
            "Eve: June 30\n"
        )
      

    def test_no_upcoming_birthdays_output(self):
        with patch('sys.stdout', new_callable=StringIO) as captured_output:
            list_upcoming_birthdays(self.current_date, [{'NAME': 'Bob', 'BIRT': datetime(2000, 1, 1)}])
            output = captured_output.getvalue()
        
        expected_output = "No upcoming birthdays in the next 30 days.\n"
        

    def test_age_calculation(self):
        age = self.current_date.year - self.individuals[0]['BIRT'].year
        self.assertEqual(age, 20)

    def test_age_calculation_past_birthday(self):
        age = self.current_date.year - self.individuals[2]['BIRT'].year
        self.assertEqual(age, 23)

    def test_empty_individuals_list(self):
        with patch('sys.stdout', new_callable=StringIO) as captured_output:
            list_upcoming_birthdays(self.current_date, [])
            output = captured_output.getvalue()
        
        expected_output = "No upcoming birthdays in the next 30 days.\n"
     

if __name__ == '__main__':
    unittest.main()
