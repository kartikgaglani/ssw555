
from datetime import date, datetime, timedelta
def family_output(names):
	first_names = []
	for name in names :
			names = name.split(" ")
			first_names.append(names[0])

	res = {x for x in first_names if first_names.count(x) > 1}
	return res

def birth_before_marriage(marr,birth_child):
 	return marr.year - birth_child.year - ((marr.month, marr.day) < (birth_child.month , birth_child.day)) >=  0

def birth_before_divorce(birth_child, div):
    div -= timedelta(weeks = 40)
    return div.year - birth_child.year - ((div.month, div.day) < (birth_child.month, birth_child.day)) >= 0

#US12 parents are too old
def compareDates(earlierDate, laterDate):
	return laterDate.year - earlierDate.year - ((laterDate.month, laterDate.day) < (earlierDate.month, earlierDate.day)) >= 0
def Parentstooold(childBirthdate, parentBirthdate, years):
    return compareDates(childBirthdate, parentBirthdate + timedelta(days = years * 365.25))
