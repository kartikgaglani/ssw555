from tabulate import tabulate

from datetime import date, datetime, timedelta
if __name__ == '_build_':
    raise Exception

import sys


class Individual:
    def __init__(self, id):
        self.info = {'ID': id}

class Family:
    def __init__(self, id):
        self.info = {'ID': id}


validTags = {
    '0': [{'HEAD', 'TRLR', 'NOTE'}, {'INDI', 'FAM'}],
    '1': [{'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS'}, {'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV'}],
    '2': {'DATE'},
}

individual = []

fams = []

individual_id = []

family_id = []

errors = []

current_date = date.today()


def read_line(fileLine):
    arguments = fileLine.split()

    if not arguments:
        return

    if arguments[0] not in validTags:
        print(check_validity(fileLine, arguments, 'N'))
        raise Exception("Please provide a valid level number")

    if arguments[0] == '0':

        if arguments[1] in validTags[arguments[0]][0]:
            return

        elif arguments[2] in validTags[arguments[0]][1]:
            if arguments[2] == 'INDI':
                # US-22 Unique IDs
                if arguments[1] not in individual_id:
                    #print(arguments[1])
                    ind = Individual(arguments[1])
                    individual.append(ind.info)
                    individual_id.append(arguments[1])
                    #print(individual_id)
                else:
                    errors.append(
                        "Individual IDs are duplicate. Please provide correct ID.")
                    #print(errors)
            else:

                if arguments[1] not in family_id:
                    family_people = Family(arguments[1])
                    fams.append(family_people.info)
                    family_id.append(arguments[1])
                else:
                    raise Exception(
                        "Family IDs are duplicate. Please provide correct ID.")

        else:
            print(check_validity(fileLine, arguments, 'N'))
            raise Exception(
                "Please provide a valid id tag in the proper format")

    elif arguments[0] == '1':
        if arguments[1] in validTags[arguments[0]][0]:

            if arguments[1] == 'FAMS':
                if arguments[1] not in individual[len(individual)-1]:
                    individual[len(individual)-1][arguments[1]
                                                  ] = [' '.join(arguments[2:])]
                else:
                    individual[len(individual)-1][arguments[1]
                                                  ].append(' '.join(arguments[2:]))
            elif len(arguments) > 2:
                individual[len(individual)-1][arguments[1]
                                              ] = ' '.join(arguments[2:])

            else:
                individual.append(arguments[1])
        elif arguments[1] in validTags[arguments[0]][1]:
            if arguments[1] == 'CHIL':
                if arguments[1] not in fams[len(fams)-1]:
                    fams[len(fams)-1][arguments[1]] = [' '.join(arguments[2:])]
                else:
                    fams[len(fams)-1][arguments[1]
                                      ].append(' '.join(arguments[2:]))
            elif len(arguments) > 2:
                fams[len(fams)-1][arguments[1]] = ' '.join(arguments[2:])
            else:
                fams.append(arguments[1])
        else:
            print(check_validity(fileLine, arguments, 'N'))
            raise Exception("Please provide a valid tag in the proper format")
    elif arguments[1] in validTags[arguments[0]]:
        date = covert_date(' '.join(arguments[2:]))
        if isinstance(individual[len(individual)-1], str):
            tag = individual.pop()
            individual[len(individual)-1][tag] = date

        elif isinstance(fams[len(fams)-1], str):
            tag = fams.pop()
            fams[len(fams)-1][tag] = date

        else:
            print(check_validity(fileLine, arguments, 'N'))
            raise Exception(
                "Please make sure your DATE tag belongs to a valid tag")
    else:
        print(check_validity(fileLine, arguments, 'N'))
        raise Exception("Improper GEDCOM format")

    return

#US01
def check_dates_before_current(current_date, individuals, families):
    for ind in individuals:
        if 'BIRT' in ind:
            birth_date = ind['BIRT']
            if birth_date > current_date:
                errors.append(f"ERROR: (US01) - Individual {ind['ID']} has a birth date ({birth_date}) after the current date.")
        if 'DEAT' in ind:
            death_date = ind['DEAT']
            if death_date > current_date:
                errors.append(f"ERROR: (US01) - Individual {ind['ID']} has a death date ({death_date}) after the current date.")
    
    for fam in families:
        if 'MARR' in fam:
            marriage_date = fam['MARR']
            if marriage_date > current_date:
                errors.append(f"ERROR: (US01) - Family {fam['ID']} has a marriage date ({marriage_date}) after the current date.")
        if 'DIV' in fam:
            divorce_date = fam['DIV']
            if divorce_date > current_date:
                errors.append(f"ERROR: (US01) - Family {fam['ID']} has a divorce date ({divorce_date}) after the current date.")

#US07
def check_death_age(individual):
    for ind in individual:
        if 'BIRT' in ind and 'DEAT' in ind:
            birth_date = ind['BIRT']
            death_date = ind['DEAT']
            age_at_death = death_date.year - birth_date.year - \
                ((death_date.month, death_date.day) < (birth_date.month, birth_date.day))
            if age_at_death >= 150:
                errors.append(f"ERROR: (US07) - Individual {ind['ID']} has a death age of {age_at_death} years which is 150 years or more after birth.")

#US07
def check_living_age(individual):
    for ind in individual:
        if 'BIRT' in ind and 'DEAT' not in ind:
            birth_date = ind['BIRT']
            age_at_current_date = current_date.year - birth_date.year - \
                ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))
            if age_at_current_date >= 150:
                errors.append(f"ERROR: (US07) - Individual {ind['ID']} is alive and has an age of {age_at_current_date} years which is 150 years or more after birth.")



#US02
def check_birth_before_marriage(individuals, families):
    family_marriage_dates = {fam['ID']: fam.get('MARR') for fam in families}

    for ind in individuals:
        if 'BIRT' in ind and 'FAMS' in ind:
            birth_date = ind['BIRT']
            family_ids = ind['FAMS']
            for fam_id in family_ids:
                marriage_date = family_marriage_dates.get(fam_id)
                if marriage_date and birth_date > marriage_date:
                    errors.append(f"ERROR: (US02) - Birth of individual {ind['ID']} occurred after their marriage in family {fam_id}.")

#US03
def check_birth_before_death(individuals):
    for ind in individuals:
        if 'BIRT' in ind and 'DEAT' in ind:
            birth_date = ind['BIRT']
            death_date = ind['DEAT']
            if birth_date > death_date:
                errors.append(f"ERROR: (US03) -  Birth of individual {ind['ID']} occurred after their death.")

#US04
def check_marriage_before_divorce(families):
    for family in families:
        if 'MARR' in family and 'DIV' in family:
            marriage_date = family['MARR']
            divorce_date = family['DIV']

            if marriage_date > divorce_date:
                errors.append(f"ERROR: (US04) - Marriage (MARR) date in family {family['ID']} occurs after the divorce (DIV) date.")


#US05
def check_marriage_before_death(families, individuals):
    for family in families:
        if 'MARR' in family:
            marriage_date = family['MARR']
            husband_id = family.get('HUSB')
            wife_id = family.get('WIFE')

            # Check husband's death date if available
            if husband_id:
                husband = next((ind for ind in individuals if ind['ID'] == husband_id), None)
                if husband and 'DEAT' in husband:
                    husband_death_date = husband['DEAT']
                    if husband_death_date < marriage_date:
                        errors.append(f"ERROR: (US05) - Marriage (MARR) date in family {family['ID']} occurs after the death of husband {husband['ID']}.")

            # Check wife's death date if available
            if wife_id:
                wife = next((ind for ind in individuals if ind['ID'] == wife_id), None)
                if wife and 'DEAT' in wife:
                    wife_death_date = wife['DEAT']
                    if wife_death_date < marriage_date:
                        errors.append(f"ERROR: (US05) - Marriage (MARR) date in family {family['ID']} occurs after the death of wife {wife['ID']}.")

#US06
def check_divorce_before_death(families, individuals):
   
    for family in families:
        if 'DIV' in family:
            divorce_date = family['DIV']
            husband_id = family.get('HUSB')
            wife_id = family.get('WIFE')

            if husband_id:
                husband = next((ind for ind in individuals if ind['ID'] == husband_id), None)
                if husband and 'DEAT' in husband:
                    husband_death_date = husband['DEAT']
                    if husband_death_date < divorce_date:
                        errors.append(f"ERROR: (US06) - Divorce date in family {family['ID']} occurs after the death of husband {husband['ID']}.")

            if wife_id:
                wife = next((ind for ind in individuals if ind['ID'] == wife_id), None)
                if wife and 'DEAT' in wife:
                    wife_death_date = wife['DEAT']
                    if wife_death_date < divorce_date:
                        errors.append(f"ERROR: (US06) - Divorce date in family {family['ID']} occurs after the death of wife {wife['ID']}.")



#US09
def check_birth_before_parent_death(individuals, families):

    birth_dates = {ind['ID']: ind.get('BIRT') for ind in individuals}
    death_dates = {ind['ID']: ind.get('DEAT') for ind in individuals}

    for family in families:
        if 'CHIL' in family:
            children = family['CHIL']
            mother_id = family.get('WIFE')
            father_id = family.get('HUSB')

            mother_death_date = death_dates.get(mother_id)
            father_death_date = death_dates.get(father_id)

            for child_id in children:
                birth_date = birth_dates.get(child_id)

                if mother_death_date and birth_date and birth_date > mother_death_date:
                    errors.append(f"ERROR: (US09) - Child {child_id} was born after the death of the mother {mother_id}.")

                if father_death_date and birth_date:
                    difference = (birth_date.year - father_death_date.year) * 12 + birth_date.month - father_death_date.month
                    if difference > 9:
                        errors.append(f"ERROR: (US09) - Child {child_id} was born more than 9 months after the death of the father {father_id}.")



# US23
def check_unique_name_birth(outfile):
    unique_name_birth = []
    names = set()
    births = set()
    #print(individual[0])
    for ind in individual:
        if 'NAME' in ind and 'BIRT' in ind:
            name = ind['NAME']
            birth = ind['BIRT']
            #print(covert_date(birth))
            if name in names or birth in births:
                errors.append(
                    f"ERROR: US23 - Individuals with the same name and birth date found: {name}, Birth Date: {birth}")
            names.add(name)
            births.add(birth)
            unique_name_birth.append((name, birth))
   


#US24

def check_unique_family_by_spouses(outfile):
    unique_families = {}

    for family in fams:
        if 'HUSB' in family and 'WIFE' in family and 'MARR' in family:
            husband_name = family['HUSB']
            wife_name = family['WIFE']
            marriage_date = family['MARR']

            # Create a unique key based on spouse names and marriage date
            unique_key = (husband_name, wife_name, marriage_date)

            # Check if the unique key is already in the dictionary
            if unique_key in unique_families:
                # A family with the same spouses and marriage date already exists
                existing_family_id = unique_families[unique_key]
                errors.append(
                    f"ERROR: US24 - Family with the same spouses by name and marriage date found: Family ID {family['ID']} and Family ID {existing_family_id}")
                # Print the error message to the console
                print(f"US24: {errors[-1]}")
            else:
                # Add the unique key to the dictionary with the family ID as the value
                unique_families[unique_key] = family['ID']



# US08 - Birth before marriage of parents
def birth_before_marriage(marr,birth_child):
 	return marr.year - birth_child.year - ((marr.month, marr.day) < (birth_child.month , birth_child.day)) >=  0

def birth_before_divorce(birth_child, div):
    div -= timedelta(weeks = 40)
    return div.year - birth_child.year - ((div.month, div.day) < (birth_child.month, birth_child.day)) >= 0
     

# US25
def family_output(names):
    first_names = []
    for name in names:
        names = name.split(" ")
        first_names.append(names[0])

    res = {x for x in first_names if first_names.count(x) > 1}
    return res

filename = ""

def check_validity(fileLine, args, is_valid):
    returnOutput = "--> {0}\n".format(fileLine.rstrip('\r\n'))
    returnOutput += "<-- "
    for i in range(len(args)):
        returnOutput += args[i]
        if i == 0:
            returnOutput += "|"
        elif i == 1:
            returnOutput += "|{}|".format(is_valid)
            if len(args) == 2:
                returnOutput += "\n"
        elif i < len(args)-1:
            returnOutput += " "
        else:
            returnOutput += "\n"

    return returnOutput

#US42(This function raises an exception when there is illegitimate date)
def covert_date(date):
    try:
        return datetime.strptime(date, '%d %b %Y').date()
    except:
        raise Exception("Date should be in the format 'Day Month Year'")


def age(today_date, person_information):
    birth = person_information["BIRT"]
    if 'DEAT' in person_information:
        death = person_information["DEAT"]
        person_information["AGE"] = death.year - birth.year - \
            ((death.month, death.day) < (birth.month, birth.day))
        person_information["ALIVE"] = False
    else:
        person_information["AGE"] = today_date.year - birth.year - \
            ((today_date.month, today_date.day) < (birth.month, birth.day))
        person_information["ALIVE"] = True

    return person_information

#US12
#US12 parents are too old
def compareDates(earlierDate, laterDate):
	return laterDate.year - earlierDate.year - ((laterDate.month, laterDate.day) < (earlierDate.month, earlierDate.day)) >= 0
def Parentstooold(childBirthdate, parentBirthdate, years):
    return compareDates(childBirthdate, parentBirthdate + timedelta(days = years * 365.25))

#US 13
def check_child_bdae(bdae_l):
    for i, bdae_l1 in enumerate(bdae_l):
        for j, bdae_l2 in enumerate(bdae_l[i+1:], i+1):
            ans = abs((bdae_l1 - bdae_l2).days)
            if ans < 240:
                return False
    return True

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
#US 10
def after_14yrs(a,b):
    return a.year - b.year - ((b.month, b.day) < (a.month, a.day)) > 14
#us 38

def list_upcoming_birthdays(current_date, individual):
    upcoming_birthdays = []

    for ind in individual:
        if 'BIRT' in ind and 'DEAT' not in ind:
            birth_date = ind['BIRT']
            days_until_birthday = (birth_date.replace(year=current_date.year) - current_date).days
            if 0 < days_until_birthday <= 30:
                upcoming_birthdays.append((ind['NAME'], birth_date))

    if upcoming_birthdays:
        print("Upcoming Birthdays (next 30 days):")
        for name, birth_date in upcoming_birthdays:
            print(f"{name}: {birth_date.strftime('%B %d')}")

    else:
        print("No upcoming birthdays in the next 30 days.")

#US 39

def list_upcoming_anniversaries(current_date, families, individuals):
    upcoming_anniversaries = []

    for fam in families:
        if 'MARR' in fam:
            marriage_date = fam['MARR']
            anniversary_date = marriage_date.replace(year=current_date.year)
            if anniversary_date >= current_date:
                days_until_anniversary = (anniversary_date - current_date).days
                if 0 <= days_until_anniversary <= 30:
                    husband_id = int(''.join(filter(str.isdigit, fam['HUSB'])))
                    wife_id = int(''.join(filter(str.isdigit, fam['WIFE'])))
                    
                    husband = search_id(individuals, len(individuals), 0, husband_id)
                    wife = search_id(individuals, len(individuals), 0, wife_id)

                    if husband['ALIVE'] and wife['ALIVE']:
                        upcoming_anniversaries.append((husband['NAME'], wife['NAME'], anniversary_date))

    if upcoming_anniversaries:
        print("Upcoming Anniversaries (next 30 days) for living couples:")
        for husband, wife, anniversary_date in upcoming_anniversaries:
            print(f"{husband} and {wife}: {anniversary_date.strftime('%B %d')}")

    else:
        print("No upcoming anniversaries in the next 30 days for living couples.")


# US20: Aunts and uncles should not marry their nieces or nephews
def aunts_and_uncles_marriage(individual, fams):
    niece_nephew_marriages = []

    for family in fams:
        if 'HUSB' in family and 'WIFE' in family:
            husband_id = family['HUSB']
            wife_id = family['WIFE']
            
            husband = [ind for ind in individual if ind['ID'] == husband_id][0]
            wife = [ind for ind in individual if ind['ID'] == wife_id][0]

            # Finding the family of the husband (uncle)
            husband_family = [fam for fam in fams if 'CHIL' in fam and husband_id in fam['CHIL']]

            # Finding the family of the wife (aunt)
            wife_family = [fam for fam in fams if 'CHIL' in fam and wife_id in fam['CHIL']]

            for h_family in husband_family:
                for w_family in wife_family:
                    if h_family['ID'] == w_family['ID']:
                        if husband['SEX'] == 'M':
                            uncles_family = h_family
                            aunts_family = w_family
                        else:
                            uncles_family = w_family
                            aunts_family = h_family
                        
                        uncles_children = uncles_family.get('CHIL', [])
                        
                        if wife_id in uncles_children:
                            error = f"ERROR: US20 - {husband['NAME']} (ID: {husband_id}) and {wife['NAME']} (ID: {wife_id}) are married, and they are related as aunt/uncle and niece/nephew."
                            niece_nephew_marriages.append(error)
    
    return niece_nephew_marriages


#us 16
def male_last_names_same_family(individual, fams):
    last_name_errors = []

    for family in fams:
        if 'HUSB' in family:
            husband_id = family['HUSB']
            husband = [ind for ind in individual if ind['ID'] == husband_id][0]
            husband_gender = husband.get('SEX')
            husband_last_name = husband.get('NAME').split()[-1]

            if husband_gender == 'M':
                for child_id in family.get('CHIL', []):
                    child = [ind for ind in individual if ind['ID'] == child_id][0]
                    if child.get('SEX') == 'M':
                        child_last_name = child.get('NAME').split()[-1]
                        if husband_last_name != child_last_name:
                            error = f"ERROR: US39 - All male members in the family (e.g., {husband['NAME']} and {child['NAME']}) should have the same last name."
                            last_name_errors.append(error)

    return last_name_errors
#US 17
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
    
#US 18
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


#US 30
def listLivingMarried(fam, ind):
    output=[]
    for family in fams:
        if 'DIV' not in family:
            husbID = int(''.join(filter(str.isdigit, family["HUSB"])))
            husb = search_id(ind, len(ind), 0, husbID)
            wifeID = int(''.join(filter(str.isdigit, family["WIFE"])))
            wife = search_id(ind, len(ind), 0, wifeID)
            if(('DEAT' not in husb) and ('DEAT' not in wife)):
                output.append(family)
    if len(output) == 0:
        errors.append("Error 30: NO living married people")
    else:
        return output

#US 21

def correctGenderForRole(husb,wife):
    if husb['SEX'] != 'M' or wife['SEX'] != 'F':
        return True
    return False
#us 31
def list_living_single(individual):
    living_singles = []
    for ind in individual:
        if 'AGE' in ind and 'DEAT' not in ind:
            age = ind['AGE']
            if age > 30 and 'FAMS' not in ind:
                living_singles.append(ind)
    return living_singles

#us35

def list_recent_births(current_date, individuals):
    recent_births = []

    for ind in individuals:
        if 'BIRT' in ind and 'DEAT' not in ind:
            birth_date_str = ind['BIRT']
            birth_date = datetime.strptime(date, '%d %b %Y').date()
            
            days_since_birth = (current_date - birth_date).days
            if 0 <= days_since_birth <= 30:
                recent_births.append(ind)

    return recent_births

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




def init():
    try:
        current_date = date.today()
        filename = input(
            "Please enter the name of the file (defaults to Kte.ged if no file given): ")
        if (filename == ""):
            filename = "Kte.ged"
        with open(filename, 'r', encoding='utf-8-sig') as infile:
            for line in infile:
                read_line(line)
             

        # Create the output file
        outfile_name = filename + ".txt"
        with open(outfile_name, "w") as outfile:
            check_unique_name_birth(outfile)  # Pass the outfile as an argument
            check_unique_family_by_spouses(outfile)
            # outfile.write(
            #     tabulate(individual, headers="keys", tablefmt="github"))
            # outfile.write('\n\n')
            # outfile.write(tabulate(fams, headers="keys", tablefmt="github"))
            # outfile.write('\n\n')

            check_dates_before_current(current_date, individual, fams)
            check_death_age(individual)
            check_living_age(individual)
            check_birth_before_marriage(individual,fams)
            check_birth_before_death(individual)
            check_marriage_before_divorce(fams)
            check_marriage_before_death(fams,individual)
            check_divorce_before_death(fams,individual)
        
            


            # outfile.write('ERRORS\n')
            # for err in errors:
            #     outfile.write(err)
            #     outfile.write('\n')

        print(f"Output has been written to {outfile_name}")

    except FileNotFoundError:
        print('''
        ERROR: GEDCOM file does not exist.
        ''')
        sys.exit()

    individual.sort(key=lambda info: int(''.join(filter(str.isdigit, info["ID"]))))
    fams.sort(key=lambda info: int(''.join(filter(str.isdigit, info["ID"]))))

   

    #US29
    list_deceased = []
    upcoming_birthdays = []
    orphans = []
    list_of_living_married = listLivingMarried(fams,individual)


    for ind in individual:
        if 'BIRT' in ind and 'DEAT' not in ind:
            birth_date = ind['BIRT']
            days_until_birthday = (birth_date.replace(year=current_date.year) - current_date).days
            if 0 < days_until_birthday <= 30:
                upcoming_birthdays.append((ind['NAME'], birth_date))

    if len(upcoming_birthdays)==0:
        errors.append("Error 38: No upcoming birthdays in the next 30 days.")
    upcoming_anniversaries = []

    today = date.today()
    result=[]
    for family in fams:
        
        user=family['MARR']
     
        curr_annv = date(today.year, user.month, user.day)

        if(curr_annv>today):
            upcoming_anniversaries.append(family)
    if len(upcoming_anniversaries)==0:
        errors.append("Error 39: No upcoming anniversaries in the next 30 days for living couples.")

    list_of_living_married = listLivingMarried(fams,individual)
    for per in individual:
        per = age(current_date, per)
        #US29
        if 'DEAT' in per:
            list_deceased.append(per)

    for family in fams:

        family_names = []

        husbandID = int(''.join(filter(str.isdigit, family["HUSB"])))
        husband = search_id(individual, len(individual), 0, husbandID)
        if not husband:
            raise Exception("Husband ID must exist.")
        else:
            family_names.append(husband['NAME'])

        wife_id = int(''.join(filter(str.isdigit, family["WIFE"])))
        wife = search_id(individual, len(individual), 0, wife_id)
        if not wife:
            raise Exception("Wife ID must exist.")
        else:
            family_names.append(wife['NAME'])

        family["HUSB"] = husband["NAME"]
        family["WIFE"] = wife["NAME"]
        hbdae = husband["BIRT"]
        wbdae = wife["BIRT"]
        mdae = family["MARR"]

        #US21 - Correct gender for role
        if correctGenderForRole(husband,wife):
            errors.append("ERROR US21: " + family["ID"] + ": Husband in family should be male and wife in family should be female.")
        if not correctGenderForRole(husband,wife):
            errors.append("ERROR US21: No such thing in the family.")


        #US 10
        if not after_14yrs(hbdae, mdae):
            errors.append("ERROR US10: Marriage" +husband["NAME"]+ "should be at least 14 years after birth of husband")
        if not after_14yrs(wbdae, mdae):
            errors.append("ERROR US10: Marriage" +wife['NAME']+" should be at least 14 years after birth of wife")

        if "CHIL" in family:
            children_bdae_dates = []
            for chil_str in family["CHIL"]:
                child_id = int(''.join(filter(str.isdigit, chil_str)))
                child = search_id(individual, len(individual), 0, child_id)
                if not child:
                    raise Exception("Wife ID must exist.")
                else:
                    family_names.append(child['NAME'])
                children_bdae_dates.append(child['BIRT'])
                childBirthdate = child['BIRT']

                #US 33
                if 'DEAT' in husband and 'DEAT' in wife and child['AGE'] < 18:
                    orphans.append(child)

                #US12
                if not Parentstooold(childBirthdate, husband["BIRT"], 80):
                    errors.append("ERROR: FAMILY: US12: " + family["ID"] + ": BIRT of father on " + husband["BIRT"].strftime("%x") + " should be less than 80 years that of Child " + chil_str + ": BIRT " + childBirthdate.strftime("%x") + ".")
                if not Parentstooold(childBirthdate, husband["BIRT"], 60):
                    errors.append("ERROR: FAMILY: US12: " + family["ID"] + ": BIRT of mother on " + wife["BIRT"].strftime("%x") + " should be less than 60 years that of Child " + chil_str + ": BIRT " + childBirthdate.strftime("%x") + ".")
                
                #US 08 Birth before the marriage of parents(and no more than 9 months after their divorce)
                if "DIV" in family:
                    divorce = family["DIV"]
                    if birth_before_divorce(divorce, childBirthdate):
                        errors.append("ERROR: US08: " + family["ID"] + ": Child " + chil_str + ": BIRT " + childBirthdate.strftime("%x") + " should be no more than 9 months after the divorce of the parents on " + mdae.strftime("%x") + ".")
                else:
                    if birth_before_marriage(mdae, childBirthdate):
                        errors.append("ERROR: US08: " + family["ID"] + ": Child " + chil_str + ": BIRT " + childBirthdate.strftime("%x") + " should be after marriage " + mdae.strftime("%x") + ".")

            if not check_child_bdae(children_bdae_dates):
                errors.append("ERROR US 10: Birth dates of siblings should be more than 8 months apart or less than 2 days apart.")    
        #US 25
        result = family_output(family_names)
        if result:
            errors.append("ERROR US25: " + family["ID"] + ": First names of individuals in the family cannot be same.")

    outfile = open(filename + ".txt", "w")

    outfile.write(tabulate(individual, headers="keys", tablefmt="github"))
    outfile.write('\n\n')
    outfile.write(tabulate(fams, headers="keys", tablefmt="github"))
    outfile.write('\n\n')
      # US31 - List living singles
    living_singles = list_living_single(individual)
    if living_singles:
            print("\nLiving Singles (over 30 and never married):")
            for single in living_singles:
                print(f"{single['NAME']} (ID: {single['ID']}) - Age: {single['AGE']}")
    else:
            print("\nNo living singles found (over 30 and never married).")

    #US29
    outfile.write('US 29: List of people deceased\n')
    outfile.write(tabulate(list_deceased, headers="keys", tablefmt="github"))
    outfile.write('\n\n')
    outfile.write('US 38\n')
    outfile.write(tabulate(upcoming_birthdays, headers="keys", tablefmt="github"))
    outfile.write('\n\n')
    outfile.write('US 39\n')
    outfile.write(tabulate(upcoming_anniversaries, headers="keys", tablefmt="github"))
    outfile.write('\n\n')
    outfile.write('US 33\n')
    outfile.write(tabulate(orphans, headers="keys", tablefmt="github"))
    outfile.write('\n\n')
    outfile.write('US 30\n')
    outfile.write(tabulate(list_of_living_married, headers="keys", tablefmt="github"))
    outfile.write('\n\n')

    outfile.write('ERRORS\n')
    for err in errors:
        outfile.write(err)
        outfile.write('\n')

    outfile.close()

init()

sys.exit()
