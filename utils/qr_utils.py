import qrcode
BASE_URL = "http://localhost/pay"


def generate_pay_code(account_num, argname="acctnum", path="static/img/codes/"):
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=10,
		border=4,
	)
	url = BASE_URL + "?" + argname + "=" + str(account_num)
	qr.add_data(url)
	qr.make(fit=True)
	imgpath = path + str(account_num) + ".jpg"
	img = qr.make_image(fill_color="black", back_color="white")
	img.save(imgpath)
	
	
