from tkinter import *

window = Tk()

def km_miles():
	miles = float(e1_var.get()) * 1.6
	t1.delete(1.0, END)
	t1.insert(END, miles)


b1 = Button(window, text="Execute", command=km_miles)
b1.grid(row=0, column=0)

e1_var = StringVar()
e1 = Entry(window, textvaraible=e1_var)
e1.grid(row=0, column=1)

t1 = Text(window, height=1, width=20)
t1.grid(row=0, column=2)

window.mainloop()