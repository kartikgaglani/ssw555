from tabulate import tabulate

from datetime import date, datetime


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
                    # print(arguments[1])
                    ind = Individual(arguments[1])
                    individual.append(ind.info)
                    individual_id.append(arguments[1])
                else:
                    errors.append(
                        "Individual IDs are duplicate. Please provide correct ID.")
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
                errors.append(f"ERROR:(US01) - Individual {ind['ID']} has a birth date ({birth_date}) after the current date.")
        if 'DEAT' in ind:
            death_date = ind['DEAT']
            if death_date > current_date:
                errors.append(f"ERROR:(US01) - Individual {ind['ID']} has a death date ({death_date}) after the current date.")
    
    for fam in families:
        if 'MARR' in fam:
            marriage_date = fam['MARR']
            if marriage_date > current_date:
                errors.append(f"ERROR:(US01) - Family {fam['ID']} has a marriage date ({marriage_date}) after the current date.")
        if 'DIV' in fam:
            divorce_date = fam['DIV']
            if divorce_date > current_date:
                errors.append(f"ERROR:(US01) - Family {fam['ID']} has a divorce date ({divorce_date}) after the current date.")

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

    for per in individual:
        per = age(current_date, per)

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

        if "CHIL" in family:
            for chil_str in family["CHIL"]:
                child_id = int(''.join(filter(str.isdigit, chil_str)))
                child = search_id(individual, len(individual), 0, child_id)
                if not child:
                    raise Exception("Wife ID must exist.")
                else:
                    family_names.append(child['NAME'])

                childBirthdate = child["BIRT"]
        #US 25
        result = family_output(family_names)
        if result:
            errors.append("ERROR US25: " + family["ID"] + ": First names of individuals in the family cannot be same.")

    outfile = open(filename + ".txt", "w")

    outfile.write(tabulate(individual, headers="keys", tablefmt="github"))
    outfile.write('\n\n')
    outfile.write(tabulate(fams, headers="keys", tablefmt="github"))
    outfile.write('\n\n')

    outfile.write('ERRORS\n')
    for err in errors:
        outfile.write(err)
        outfile.write('\n')

    outfile.close()

init()

sys.exit()
