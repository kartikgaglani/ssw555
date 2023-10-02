def is_marriage_allowed(age_spouse1, age_spouse2):
    # Check if both spouses are at least 14 years old
    if age_spouse1 >= 14 and age_spouse2 >= 14:
        return True
    else:
        return False

# Input ages of the two spouses
age_spouse1 = int(input("Enter age of spouse 1: "))
age_spouse2 = int(input("Enter age of spouse 2: "))

# Check if marriage is allowed
if is_marriage_allowed(age_spouse1, age_spouse2):
    print("Marriage is allowed.")
else:
    print("Marriage is not allowed as both spouses must be at least 14 years old.")
