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
#US 14
# Create a dictionary to store individuals' information
individuals = {}

# Function to add individual data to the dictionary
def add_individual(indi_id, name, sex, birth_date, death_date=None, famc=None, fams=None):
    individuals[indi_id] = {
        "name": name,
        "sex": sex,
        "birth_date": birth_date,
        "death_date": death_date,
        "famc": famc,
        "fams": fams
    }

# # Read data from the GEDCOM file
# gedcom_file_path = "C:\Users\Anna\Desktop\sprint\ssw555-1\Kte.ged"  
# with open(gedcom_file_path, "r") as gedcom_file:
#     lines = gedcom_file.readlines()

# # Process the GEDCOM data
# current_individual_id = None
# for line in lines:
#     parts = line.strip().split()
#     if len(parts) >= 2:
#         level = int(parts[0])
#         tag = parts[1]

#         if level == 0:
#             if tag == "@I" and parts[2].isdigit():
#                 current_individual_id = parts[2]
#             else:
#                 current_individual_id = None
#         elif level == 1 and current_individual_id:
#             if tag == "NAME":
#                 name = " ".join(parts[2:])
#             elif tag == "SEX":
#                 sex = parts[2]
#             elif tag == "BIRT":
#                 birth_date = None
#             elif tag == "DEAT":
#                 death_date = None
#             elif tag == "FAMC":
#                 famc = parts[2]
#             elif tag == "FAMS":
#                 fams = parts[2]

#     elif current_individual_id:
#         if tag == "DATE":
#             date = " ".join(parts[2:])
#             if "BIRT" in line:
#                 birth_date = date
#             elif "DEAT" in line:
#                 death_date = date

#         elif tag == "MARR":
#             fams = parts[2]

#     if current_individual_id and "BIRT" not in line and "DEAT" not in line:
#         add_individual(current_individual_id, name, sex, birth_date, death_date, famc, fams)

# # Print individuals' information
# for indi_id, data in individuals.items():
#     print(f"Individual ID: {indi_id}")
#     print(f"Name: {data['name']}")
#     print(f"Sex: {data['sex']}")
#     print(f"Birth Date: {data['birth_date']}")
#     if data['death_date']:
#         print(f"Death Date: {data['death_date']}")
#     if data['famc']:
#         print(f"Child of Family: {data['famc']}")
#     if data['fams']:
#         print(f"Spouse in Family: {data['fams']}")
#     print()

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
def init():
    try:
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
            check_birth_before_parent_death(individual,fams)

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
    #US29
    outfile.write('US 29: List of people deceased\n')
    outfile.write(tabulate(list_deceased, headers="keys", tablefmt="github"))
    outfile.write('\n\n')

    outfile.write('ERRORS\n')
    for err in errors:
        outfile.write(err)
        outfile.write('\n')

    outfile.close()

init()

sys.exit()
