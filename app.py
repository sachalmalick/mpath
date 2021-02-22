from flask import Flask, render_template, request,redirect,url_for,session
import utils.admin_utils as au
import utils.db_utils as du
import json

app = Flask(__name__)
app.secret_key = "sachal"


@app.route('/pay', methods=['GET'])
def pay_route():
	acctnum = request.args.get("acctnum")
	if(acctnum == None):
		return "please specify an account"
	account = du.get_account(acctnum)
	if(account == False):
		return "invalid account number"
	return render_template("pay2.html", account = account, acctnum=account["account_num"])

def return_admin(neworgmsg="", account_num=None):
	accounts = du.get_all_accounts()
	def func(e):
		return e["full_name"]
	accounts.sort(key=func)
	return render_template("admin2.html", accounts=accounts,neworgmsg=neworgmsg, account_num=account_num)

@app.route('/admin', methods=['GET'])
def admin_route():
	return return_admin()

@app.route('/logorder', methods=['POST'])
def logorder_route():
	accountnum = request.form.get("account_num")
	orderid = request.form.get("order_id")
	status = request.form.get("status")
	amt = request.form.get("net_amt")
	du.insert_order(accountnum, orderid, status, amt)
	return "success"

@app.route('/newacct', methods=['GET', 'POST'])
def new_account_route():
	fullname = request.form.get("fullname")
	bio = request.form.get("bio")
	if('file' not in request.files):
		return return_admin(neworgmsg = "please upload a profile pic")
	file = request.files['file']
	if(len(file.filename.strip()) == 0):
		return return_admin(neworgmsg="no file specifed")
	if (not ((".png" in file.filename) or (".jpg" in file.filename))):
		return return_admin(neworgmsg="only png or jpg files supported")
	account_number = au.setup_account(fullname, bio)
	if(account_number == False):
		return return_admin(neworgmsg="unable to create an account")
	file.save("static/img/pfp/" + str(account_number))
	return return_admin(neworgmsg = "successfully created", account_num=account_number)

@app.route('/viewaccount', methods=['POST'])
def viewaccount_route():
	acctid = request.form.get("id")
	acct = du.get_account(acctid)
	if(acct == False):
		return "NOT FOUND"
	return json.dumps(acct)

def return_mng_acct_view(account_id, withdraw_msg=""):
	if(account_id == None):
		return "please enter a valid account ID"
	account = du.get_account(account_id)
	transactions = du.get_account_transactions(account_id)
	return render_template("account2.html", orders=transactions, withdraw_message=withdraw_msg, acctnum = account_id, account=account)
@app.route('/manageaccount', methods=['GET', 'POST'])
def manageaccount_route():
	return return_mng_acct_view(request.args.get("id"))

@app.route('/logwithdrawl', methods=['GET', 'POST'])
def logwithdrawl_route():
	account_id = request.form.get("account_id")
	amount = request.form.get("amount")
	try:
		amount = float(amount)
	except:
		return "invalid withdrawl amount"
	transactions = du.get_account_transactions(account_id)
	print(amount)
	print(transactions["balance"])
	if(amount > transactions["balance"]):
		return "amount exceeds balance"
	du.insert_order(account_id, "N/A", "WITHDRAW", amount)
	return "success"

def return_mng_acct_view_two(account_id, withdraw_msg=""):
	if(account_id == None):
		return "please enter a valid account ID"
	transactions = du.get_account_transactions(account_id)
	acct = du.get_account(account_id)
	return render_template("account2.html", orders=transactions, withdraw_message=withdraw_msg, account_id = account_id, account=acct)


@app.route('/', methods=['GET'])
def main_page():
	acctnum = request.args.get("acctnum")
	if(acctnum == None):
		return "please specify an account"
	account = du.get_account(acctnum)
	if(account == False):
		return "invalid account number"
	return render_template("pay2.html", account = account, acctnum=account["account_num"])


if __name__=="__main__":
    app.run("localhost", 8080, debug = True)