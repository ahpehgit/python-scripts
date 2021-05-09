from datetime import datetime

f1 = f2 = f3 = ''

with open("file1.txt", "r") as myfile:
	f1 = myfile.read()

with open("file2.txt", "r") as myfile:
	f2 = myfile.read()

with open("file3.txt", "r") as myfile:
	f3 = myfile.read()

now = datetime.now()
filename = now.strftime("%Y-%m-%d-%H-%M-%S-%s") + ".txt"
with open(filename, "w") as myfile:
	myfile.write(f1 + "\n" + f2 + "\n" + f3)