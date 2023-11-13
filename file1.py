
from datetime import date, datetime, timedelta
def family_output(names):
	first_names = []
	for name in names :
			names = name.split(" ")
			first_names.append(names[0])

	res = {x for x in first_names if first_names.count(x) > 1}
	return res

def search_id(array, high, low, target):
    if high <= low:
        raise Exception("ID " + target + " not found.")

    mid = high + (low-high)//2

    mid_ = int(''.join(filter(str.isdigit, array[mid]['ID'])))

    if mid_ > target:
        return search_id(array, mid, low, target)
    if mid_ < target:
        return search_id(array, high, mid+1, target)
    return array[mid]

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

#US 30
def listLivingMarried(fam, ind):
    output=[]
    for family in fam:
        if 'DIV' not in family:
            husbID = int(''.join(filter(str.isdigit, family["HUSB"])))
            husb = search_id(ind, len(ind), 0, husbID)
            wifeID = int(''.join(filter(str.isdigit, family["WIFE"])))
            wife = search_id(ind, len(ind), 0, wifeID)
            if(('DEAT' not in husb) and ('DEAT' not in wife)):
                output.append(family)
        return output

#US 21

def correctGenderForRole(husb,wife):
    if husb['SEX'] != 'M' or wife['SEX'] != 'F':
        return True
    return False
