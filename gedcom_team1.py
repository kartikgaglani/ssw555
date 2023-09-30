
from tabulate import tabulate

from datetime import date, datetime


if __name__ == '_build_':
	raise Exception;

import sys;

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
};

individual = []

fams = []

individual_id = []

family_id = []

errors = []

current_date = date.today()

def read_line(fileLine):
	arguments = fileLine.split();

	if not arguments: 
		return;

	if arguments[0] not in validTags:
		print(check_validity(fileLine, arguments, 'N'))
		raise Exception("Please provide a valid level number") 

	if arguments[0] == '0':

		if arguments[1] in validTags[arguments[0]][0]:
			return 

		elif arguments[2] in validTags[arguments[0]][1]:
			if arguments[2] == 'INDI':
				#US-22 Unique IDs
				if arguments[1] not in individual_id: 
					print(arguments[1])
					ind = Individual(arguments[1]) 
					individual.append(ind.info) 
					individual_id.append(arguments[1])
				else:
					errors.append("Individual IDs are duplicate. Please provide correct ID.")
			else:
			
				if arguments[1] not in family_id:
					family_people = Family(arguments[1]) 
					fams.append(family_people.info) 
					family_id.append(arguments[1])
				else:
					raise Exception("Family IDs are duplicate. Please provide correct ID.")

	
		else:
			print(check_validity(fileLine, arguments, 'N'))
			raise Exception("Please provide a valid id tag in the proper format") 

	elif arguments[0] == '1':
		if arguments[1] in validTags[arguments[0]][0]: 
			
			if arguments[1] == 'FAMS':
				if arguments[1] not in individual[len(individual)-1]:
					individual[len(individual)-1][arguments[1]] = [' '.join(arguments[2:])]
				else:
					individual[len(individual)-1][arguments[1]].append(' '.join(arguments[2:]))
			elif len(arguments) > 2:
				individual[len(individual)-1][arguments[1]] = ' '.join(arguments[2:]) 

			else:
				individual.append(arguments[1])		
		elif arguments[1] in validTags[arguments[0]][1]: 
			if arguments[1] == 'CHIL':
				if arguments[1] not in fams[len(fams)-1]:
					fams[len(fams)-1][arguments[1]] = [' '.join(arguments[2:])]
				else:
					fams[len(fams)-1][arguments[1]].append(' '.join(arguments[2:]))
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
			raise Exception("Please make sure your DATE tag belongs to a valid tag") 
	else:
		print(check_validity(fileLine, arguments, 'N'))
		raise Exception("Improper GEDCOM format") 	

	return



#US25
def family_output(names):
	first_names = []
	for name in names :
			names = name.split(" ")
			first_names.append(names[0])

	res = {x for x in first_names if first_names.count(x) > 1}
	if res :
		raise Exception("First names of individuals cannot be same.")
	

def check_validity(fileLine, args, is_valid):
	returnOutput = "--> {0}\n".format(fileLine.rstrip('\r\n'));
	returnOutput += "<-- ";
	for i in range(len(args)):
		returnOutput += args[i];
		if i == 0:
			returnOutput += "|";
		elif i == 1:
			returnOutput += "|{}|".format(is_valid)
			if len(args) == 2:
				returnOutput += "\n";
		elif i < len(args)-1:
			returnOutput += " ";
		else:
			returnOutput += "\n";
			
	return returnOutput;

def covert_date(date):
	try:
		return datetime.strptime(date, '%d %b %Y').date()
	except:
		raise Exception("Date should be in the format 'Day Month Year'")


def age(today_date, person_information):
	birth = person_information["BIRT"]
	if 'DEAT' in person_information:
		death = person_information["DEAT"]
		person_information["AGE"] = death.year - birth.year - ((death.month, death.day) < (birth.month, birth.day))
		person_information["ALIVE"] = False
	else:
		person_information["AGE"] = today_date.year - birth.year - ((today_date.month, today_date.day) < (birth.month, birth.day))
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
		filename = input("Please enter the name of the file (defaults to test3.ged if no file given): ")
		if(filename==""):
			filename="test.ged"
		with open(filename, 'r', encoding='utf-8-sig') as infile:
			for line in infile:
				#print(line)
				read_line(line);
	except FileNotFoundError:
		print ('''
		ERROR: GEDCOM file does not exist.
		''');
		sys.exit();

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

		family["HUSB NAME"] = husband["NAME"]
		family["WIFE NAME"] = wife["NAME"]
        
		
		if "CHIL" in family:
			for chil_str in family["CHIL"]:
				child_id = int(''.join(filter(str.isdigit, chil_str)))
				child = search_id(individual, len(individual), 0, child_id)
				if not child:
					raise Exception("Wife ID must exist.")
				else:
					family_names.append(child['NAME'])
	
				childBirthdate = child["BIRT"]


			
		family_output(family_names)

	outfile = open(filename + ".txt", "w")

	outfile.write(tabulate(individual, headers = "keys", tablefmt="github"))
	outfile.write('\n\n')
	outfile.write(tabulate(fams, headers = "keys", tablefmt="github"))
	outfile.write('\n\n')

	
	outfile.write('ERRORS\n')	
	for err in errors:
		outfile.write(err)
		outfile.write('\n')	

	outfile.close()


init()
sys.exit();