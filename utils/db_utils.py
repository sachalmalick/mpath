import sqlite3

db_name = "mpath.db"

'''
accounts:

account_num primary_key (int),full name(text), bio(blob)
'''
ACCOUNTS_TABLE = '''
	CREATE TABLE `accounts` (
		`account_num` INTEGER NOT NULL PRIMARY KEY,
		`full_name` TEXT,
		`bio` BLOB
	);'''

ORDERS_TABLE = '''
	CREATE TABLE `orders` (
		`account_num` INTEGER NOT NULL,
		`order_id` TEXT NOT NULL,
		`status` VARCHAR(20),
		`net_amount` DOUBLE
	);'''




def execute_select(command):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	results = c.execute(command)
	l = []
	for row in results:
		l.append(row)
	conn.close()
	return l

def execute_update(command):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	if(isinstance(command, list)):
		for cmd in command:
			try:
				c.execute(cmd)
			except Exception as e:
				print(str(e))
				print(cmd)
	else:
		c.execute(command)
	conn.commit()
	conn.close()
	
#0 = successful, 1 = repeat account num, 2 = all other errors.
def create_account(account_num, name, bio):
	statement = "INSERT INTO accounts (account_num, full_name, bio) VALUES (?, ?, ?)"
	statement = statement.format(account_num, name, bio)
	print(statement)
	try:
		conn = sqlite3.connect(db_name)
		c = conn.cursor()
		c.execute(statement, (account_num, name, bio))
		conn.commit()
		conn.close()
		return 0
	except Exception as sqlexep:
		conn.close()
		if(isinstance(sqlexep, sqlite3.IntegrityError)):
			if("accounts.account_num" in str(sqlexep)):
				return 1
		return 2
	
def get_organization(email=None,org_id=None,username=None):
	if(email != None):
		cmd = "SELECT * from organizations WHERE admin_email = '{}'"
		cmd = cmd.format(email)
		print(cmd)
		return execute_select(cmd)
	elif(org_id != None):
		cmd = "SELECT * from organizations WHERE org_id = {}"
		cmd = cmd.format(org_id)
		return execute_select(cmd)
	elif(username != None):
		cmd = "SELECT * from organizations WHERE username = '{}'"
		cmd = cmd.format(username)
		return execute_select(cmd)
	
def get_key(dic, key):
	val = dic.get(key)
	if(val == None):
		return ""
	return val
	
def insert_order(account_num, order_id, status, net_amount):
	stmt = "INSERT INTO orders (account_num, order_id, status, net_amount) VALUES ('{}', '{}', '{}', {})"
	stmt = stmt.format(account_num, order_id, status, net_amount)
	execute_update([stmt])
	
def insert_students(students, org_id):
	cmds = []
	for student in students:
		email = get_key(student, "Email")
		fname = get_key(student, "Firstname")
		lname = get_key(student, "Lastname")
		person_id = get_key(student, "id")
		room_id = get_key(student, "staff_room")
		stmt = "INSERT INTO students (org_id, firstname, lastname, email, person_id, room_id) VALUES ({}, '{}', '{}', '{}', '{}', '{}')"
		stmt = stmt.format(org_id, fname, lname, email, person_id, room_id)
		cmds.append(stmt)
	execute_update(cmds)
	
def update_students(students, key, key_name):
	cmds = []
	for student in students:
		key_val = get_key(student, key)
		email = get_key(student, "Email")
		stmt = "UPDATE students SET {} = '{}' WHERE email = '{}'"
		stmt = stmt.format(key_name, key_val, email)
		print(stmt)
		cmds.append(stmt)
	execute_update(cmds)
	
def update_staff(students, key, key_name):
	cmds = []
	for student in students:
		key_val = get_key(student, key)
		email = get_key(student, "Email")
		stmt = "UPDATE staff SET {} = '{}' WHERE email = '{}'"
		stmt = stmt.format(key_name, key_val, email)
		print(stmt)
		cmds.append(stmt)
	execute_update(cmds)

	
	
def get_student(email=None, org_id=None):
	stmt = "SELECT * FROM students WHERE email = '{}'".format(email)
	if((ord_id != None) and (email != None)):
		stmt = "SELECT * FROM students WHERE email = '{}' AND org_id = {}".format(email, org_id)
	students = execute_select(stmt)
	results = []
	for student in students:
		updatedv = {}
		updatedv["org_id"] = student[0]
		updatedv["Firstname"] = student[1]
		updatedv["Lastname"] = student[2]
		updatedv["Email"] = student[3]
		updatedv["id"] = student[4]
		updatedv["staff_room"] = student[5]
		results.append(updatedv)
	if(len(results) == 0):
		return False
	return results[0]

def get_account(account_id=None):
	if(account_id == None):
		return
	stmt = "SELECT * FROM accounts WHERE account_num = '{}'".format(account_id)
	accounts = execute_select(stmt)
	results = []
	for acct in accounts:
		updatedv = {}
		updatedv["account_num"] = acct[0]
		updatedv["full_name"] = acct[1]
		updatedv["bio"] = acct[2]
		results.append(updatedv)
	if(len(results) == 0):
		return False
	return results[0]

def get_account_transactions(account_id):
	stmt = "SELECT * FROM orders WHERE account_num = '{}'".format(account_id)
	orders = execute_select(stmt)
	pending,donated,withdrawn,other = 0,0,0,0
	transactions = []
	for order in orders:
		transaction = {}
		transaction["account_num"] = order[0]
		transaction["id"] = order[1]
		transaction["status"] = order[2]
		transaction["amount"] = float(order[3])
		if(transaction["status"] == "COMPLETED"):
			donated+=transaction["amount"]
		elif(transaction["status"] == "PENDING"):
			pending+=transaction["amount"]
		elif(transaction["status"] == "WITHDRAW"):
			withdrawn+=transaction["amount"]
		else:
			other+=transaction["amount"]
		transactions.append(transaction)
	transactions.reverse()
	return {"transactions" : transactions, "pending" : pending, "donated" : donated, "withdrawn" : withdrawn, "other" : other, "balance" : donated - withdrawn}

def get_all_accounts():
	stmt = "SELECT * FROM accounts"
	accounts = execute_select(stmt)
	results = []
	for acct in accounts:
		updatedv = {}
		updatedv["account_num"] = acct[0]
		updatedv["full_name"] = acct[1]
		updatedv["bio"] = acct[2]
		results.append(updatedv)
	return results


def get_all_staff(orgid):
	stmt = "SELECT * FROM staff WHERE org_id = {}".format(orgid)
	results = []
	staffmems = execute_select(stmt)
	for staff in staffmems:
		updatedv = {}
		updatedv["org_id"] = staff[0]
		updatedv["Firstname"] = staff[1]
		updatedv["Lastname"] = staff[2]
		updatedv["Email"] = staff[3]
		updatedv["id"] = staff[4]
		results.append(updatedv)
	return results

def update_org_teamid(orgid, teamid):
	stmt = "UPDATE organizations SET staff_team_id = '{}' WHERE org_id = {}"
	stmt = stmt.format(teamid, orgid)
	print(stmt)
	execute_update([stmt])

	
def create_tables():
	commands = []
	commands.append("DROP TABLE IF EXISTS accounts")
	commands.append("DROP TABLE IF EXISTS orders")
	commands.append(ACCOUNTS_TABLE)
	commands.append(ORDERS_TABLE)
	execute_update(commands)
	
if __name__ == "__main__":
	execute_update([ORDERS_TABLE])
	insert_order(2483929, "testest", "COMPLETED", 30.23)
#	create_tables()
#	print(create_account(57, "sachal malick", "this is a test"))
#	print(create_account(33, "sachal malick", "this is a test"))
#	print(create_account(33, "hello malick", "this is a test"))