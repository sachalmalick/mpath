import random

from .db_utils import create_account
from .qr_utils import generate_pay_code

START_RANGE = 1000000000
END_RANGE = 9999999999

people = [("meredith palmer", "hi im mer"), ("michael scott", "thats what she said"), ("jim halpert", "haah little comment"), ("dwight schrute", "hahhh little comment")]

def generate_account_num():
	return random.randint(START_RANGE, END_RANGE)

def create_account_entry(name, bio, max_steps = 100):
	for i in range(0, max_steps):
		num = generate_account_num()
		res = create_account(num, name, bio)
		if(res == 0):
			return num
		elif(res == 2):
			return False
	print("max steps exceeded")
	return False

def setup_account(name, bio):
	res = create_account_entry(name, bio)
	if(res == False):
		print("could not create account")
		return False
	generate_pay_code(res)
	return res

def run_tests():
	for person in people:
		setup_account(person[0], person[1])
