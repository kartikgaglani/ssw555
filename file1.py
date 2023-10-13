
from datetime import date, datetime, timedelta
def family_output(names):
	first_names = []
	for name in names :
			names = name.split(" ")
			first_names.append(names[0])

	res = {x for x in first_names if first_names.count(x) > 1}
	return res

def compareDates(currDate, pastDate):
	return pastDate.year - currDate.year - ((pastDate.month, pastDate.day) < (currDate.month, currDate.day)) >= 0
