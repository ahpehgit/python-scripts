import time
from datetime import datetime as dt

hosts_path = r"./hosts"
redirect = "127.0.0.1"
website_lists = ["www.facebook.com", "facebook.com", "hotmail.com"]

while True:
	if dt(dt.now().year, dt.now().month, dt.now().day, 8, 0, 0) < dt.now() < dt(dt.now().year, dt.now().month, dt.now().day, 16, 0, 0):
		print("Slogging work hours...")

		with open(hosts_path, "r+") as file:
			content = file.read()
			print(content)
			for website in website_lists:
				if website in content:
					pass #do nothing
				else:
					file.write("127.0.0.1 %s\n" %(website))

	else:
		print("It's play time!")
		with open(hosts_path, "r+") as file:
			content = file.readlines()
			file.seek(0)
			
			for line in content:
				if not any(website in line for website in website_lists):
					file.write(line)
				else:
					pass #do nothing
			file.truncate();
	time.sleep(5) #sleep for 5 seconds