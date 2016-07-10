from Tkinter import *

#====WINDOW 1
win_1=Tk()
b1_1 = Button(win_1,text="One")
b1_2 = Button(win_1,text="Two")

b1_1.pack(side=LEFT,padx=10)
b1_2.pack(side=LEFT,padx=10)

#====WINDOW 2

win_2=Tk()

b2_1 = Button(win_2,text="One")
b2_2 = Button(win_2,text="Two")
b2_1.grid(row=0,column=0)
b2_2.grid(row=1,column=1)

l2 = Label(win_2, text="This is a label")
l2.grid(row=1,column=0)

#====WINDOW 3
win_3 = T
f = Frame(win_3)
b3_1 = Button(f,text ="One")
b3_2 = Button(f,text ="One")
b3_3 = Button(f,text ="One")

b3_1.pack(side = LEFT)
b3_2.pack(side = LEFT)
b3_3.pack(side = LEFT)

l3 = Label(win_3,text = "This label is over all buttons")
l3.pack()
f.pack()

b3_1.configure(text = "Uno")
def btn3_1() : print "Button one was pushed"
b3_1.configure(command = btn3_1)

#====WINDOW 4

win_4 = Tk()
v = StringVar()
e = Entry(win_4,textvariable = v)
e.pack()
v.get()
v.set("this is set from the program")

#====WINDOW 5

win_5 = Tk()
lb = Listbox(win_5, height=3)
lb.pack()
lb.insert(END,"first entry")
lb.insert(END,"second entry")
lb.insert(END,"third entry")
lb.insert(END,"fourth entry")
sb = Scrollbar(win_5,orient=VERTICAL)
sb.pack(side=RIGHT,fill=Y)
sb.configure(command=lb.yview)
lb.configure(yscrollcommand=sb.set)
lb.curselection()


#=============
win_1.mainloop()
