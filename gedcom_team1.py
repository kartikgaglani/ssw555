
from tabulate import tabulate
from datetime import date, datetime

# This is statement is required by the build system to query build infos
if __name__ == '__build__':
	raise Exception;

import sys;

# creates a new "person" object
class Individual:
	def __init__(self, id):
		self.info = {'ID': id} # dict to save individual information


# creates a new "family" object
class Family:
	def __init__(self, id):
		self.info = {'ID': id} # dict to save family information
	   

# all the valid tags for the project, along with their corresponding levels
validTags = {
	'0': [{'HEAD', 'TRLR', 'NOTE'}, {'INDI', 'FAM'}],
	'1': [{'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS'}, {'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV'}],
	'2': {'DATE'},
};

# list of all individuals
indis = []
# list of all families
fams = []

# read and evalute if each new line is in valid GEDCOM format
def readLine(fileLine):
	args = fileLine.split();
	

	# end of file check
	if not args: 
		return;

	# valid level check (cannot go past level 2)
	if args[0] not in validTags:
		print(validOutput(fileLine, args, 'N'))
		raise Exception("Please provide a valid level number") 

	if args[0] == '0':

		if args[1] in validTags[args[0]][0]:
			return # these tags aren''t needed
		
		# individual and family id tags have a different format
		elif args[2] in validTags[args[0]][1]:
			if args[2] == 'INDI':
				indi = Individual(args[1]) # creates new individual object with id specified by args[1]
				indis.append(indi.info) # add object dict to list of individuals
			else:
				fam = Family(args[1]) # creates new family object with id specified by args[1]
				fams.append(fam.info) # add object dict to list of families

		# valid tag check (must be a tag specified in valid tags)
		else:
			print(validOutput(fileLine, args, 'N'))
			raise Exception("Please provide a valid id tag in the proper format") 

	elif args[0] == '1':

		if args[1] in validTags[args[0]][0]: # these tags specify certain information for the individual it describes 
			# edge case - FAMS information should be a list of strings since you can have multiple spouces
			if args[1] == 'FAMS':
				if args[1] not in indis[len(indis)-1]:
					indis[len(indis)-1][args[1]] = [' '.join(args[2:])]
				else:
					indis[len(indis)-1][args[1]].append(' '.join(args[2:]))
			elif len(args) > 2:
				indis[len(indis)-1][args[1]] = ' '.join(args[2:]) # store the infomation for the most recent person added to the "indis" list
			
			else:
				# edge case - information is within a nested date tag and not on the same line, save the tag for later
				indis.append(args[1])
				
		elif args[1] in validTags[args[0]][1]: # these tags specify certain information for the family it describes 
			
			# edge case - FAMS information should be a list of strings since you can have multiple spouces
			if args[1] == 'CHIL':
				if args[1] not in fams[len(fams)-1]:
					fams[len(fams)-1][args[1]] = [' '.join(args[2:])]
				else:
					fams[len(fams)-1][args[1]].append(' '.join(args[2:]))
			elif len(args) > 2:
				fams[len(fams)-1][args[1]] = ' '.join(args[2:]) # store the infomation for the most recent family added to the "fams" list
			else:
				# edge case - information is within a nested date tag and not on the same line, save the tag for later
				fams.append(args[1]) 
		
		# valid tag check (must be a tag specified in valid tags)
		else:
			print(validOutput(fileLine, args, 'N'))
			raise Exception("Please provide a valid tag in the proper format") 

	elif args[1] in validTags[args[0]]:
		# date tag - take the previous saved tag and add date information to the previously saved object in array
		if isinstance(indis[len(indis)-1], str):
			tag = indis.pop()
			indis[len(indis)-1][tag] = ' '.join(args[2:])
		elif isinstance(fams[len(fams)-1], str):
			tag = fams.pop()
			fams[len(fams)-1][tag] = ' '.join(args[2:])
		# valid format check (date must proceed a level 1 tag)
		else:
			print(validOutput(fileLine, args, 'N'))
			raise Exception("Please make sure your DATE tag belongs to a valid tag") 
	else:
		print(validOutput(fileLine, args, 'N'))
		raise Exception("Improper GEDCOM format") 	

	#print(validOutput(fileLine, args, 'Y'))
	return


# print the input and output of each new line 
def validOutput(fileLine, args, isValid):
	returnOutput = "--> {0}\n".format(fileLine.rstrip('\r\n'));
	returnOutput += "<-- ";

	# print output in the format "<-- <level>|<tag>|<valid?> : Y or N|<arguments>"
	for i in range(len(args)):
		returnOutput += args[i];
		if i == 0:
			returnOutput += "|";
		elif i == 1:
			returnOutput += "|{}|".format(isValid)
			if len(args) == 2:
				returnOutput += "\n";
		elif i < len(args)-1:
			returnOutput += " ";
		else:
			returnOutput += "\n";
			
	return returnOutput;

# calculates an individual's age and whether they are alive, adds this to their dictionary
def getAge(today, personInfo):
	# print(personInfo)
	birth = datetime.strptime(personInfo["BIRT"], '%d %b %Y').date()
	if 'DEAT' in personInfo:
		death = datetime.strptime(personInfo["DEAT"], '%d %b %Y').date()
		personInfo["AGE"] = death.year - birth.year - ((death.month, death.day) < (birth.month, birth.day))
		personInfo["ALIVE"] = False
	else:
		personInfo["AGE"] = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
		personInfo["ALIVE"] = True
		
	return personInfo

# binary search through the list of individuals to find the matching ID
def searchID (high, low, target):
	if high <= low:
		return False

	mid = (high+low)//2

	# turn midpoint string ID into a number
	midNum = int(''.join(filter(str.isdigit, indis[mid]['ID'])))

	if midNum > target:
		return searchID(mid, low, target)
	if midNum < target:
		return searchID(high, mid+1, target)
	return indis[mid]["NAME"]


# main method
def init():
	try:
		filename = input("Please enter the name of the file: ")
		if(filename==""):
			filename="test3.ged"
		with open(filename, 'r',encoding='utf-8-sig') as infile:
			for line in infile:
				readLine(line);
	except FileNotFoundError:
		print ('''
		ERROR: GEDCOM file does not exist.
		''');
		sys.exit();

	# sort each list by their ID nums
	indis.sort(key=lambda info: int(''.join(filter(str.isdigit, info["ID"])))) 
	fams.sort(key=lambda info: int(''.join(filter(str.isdigit, info["ID"])))) 

	currDate = date.today()
	for person in indis:
		person = getAge(currDate, person)

	for family in fams:
		# turn husband string ID into a number
		husbID = int(''.join(filter(str.isdigit, family["HUSB"])))
		husbName = searchID(len(indis), 0, husbID)

		# turn wife string ID into a number
		wifeID = int(''.join(filter(str.isdigit, family["WIFE"])))
		wifeName = searchID(len(indis), 0, wifeID)

		if not husbName or not wifeName: # ID not found in list
			print(wifeID, husbID)
			raise Exception("Family Husband and Wife IDs must exist.")

		family["HUSB NAME"] = husbName
		family["WIFE NAME"] = wifeName

	print(tabulate(indis, headers = "keys"))
	print()
	print(tabulate(fams, headers = "keys"))

init()
sys.exit();
