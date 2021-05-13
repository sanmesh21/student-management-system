from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import requests
import bs4
import os
import tempfile
from tkinter.scrolledtext import *
from sqlite3 import *
import pandas  as pd
import matplotlib.pyplot as plt
import numpy as np
#========= All Functions =============
def F1():
	add_win.deiconify()
	main_win.withdraw()
def F2():
	main_win.deiconify()
	add_win.withdraw()
def F3():
	up_win.deiconify()
	main_win.withdraw()
def F4():
	main_win.deiconify()
	up_win.withdraw()
def F5():
	view_win_st_data.delete(1.0,END)
	view_win.deiconify()
	main_win.withdraw()
def F6():
	main_win.deiconify()
	view_win.withdraw()
def F7():
	del_win.deiconify()
	main_win.withdraw()
def F8():
	main_win.deiconify()
	del_win.withdraw()
def F9():
	ad_win.deiconify()
	main_win.withdraw()
def F10():
	main_win.deiconify()
	ad_win.withdraw()
def add_clear():
	add_win_ent_rno.delete(0,END)
	add_win_ent_name.delete(0,END)
	add_win_ent_marks.delete(0,END)
def up_clear():
	up_win_ent_rno.delete(0,END)
	up_win_ent_name.delete(0,END)
	up_win_ent_marks.delete(0,END)
def del_clear():
	del_win_ent_rno.delete(0,END)
def search():
	con = None
	rno = (up_win_ent_rno.get())
	name = (up_win_ent_name.get())
	marks = (up_win_ent_marks.get())

	if rno.isnumeric() :
		rno = int(rno)
		name = str(name)
		try:
			con = connect("SMS.db")
			cursor = con.cursor()
			sql = "select * from student where rno = '%d'"
			cursor.execute(sql % (rno))
			row = cursor.fetchone()
			if  row == None:
				messagebox.showwarning("Warning",("Record of RNO "+ up_win_ent_rno.get() + " Does Not Exist"))
			else:
				up_win_ent_name.insert(INSERT,row[1])
				up_win_ent_marks.insert(INSERT,row[2])
		except Exception as e:
			messagebox.showerror("issue",e)
			con.rollback()	
		finally:
			if con is not None:
					con.close()
	else:
		if up_win_ent_rno.get() == "":
			messagebox.showerror("RNO VAL","Please Enter the Roll No")
		elif rno.isnumeric() != True:
			messagebox.showerror("RNO VAL 1","Please Enter the +VE integers only In RNO Field")
		elif int(rno) < 0 and rno.isnumeric() != True:
			messagebox.showerror("RNO VAL 2","Please Enter Only + VE Integers in Rno field")
		else:
			messagebox.showerror("ERROR","Invalid reason")
def save():
	con = None
	rno = add_win_ent_rno.get()
	name = add_win_ent_name.get()
	marks = add_win_ent_marks.get()
	if rno.isnumeric() and name.isalpha() and marks.isnumeric() and len(name) > 1 and int(marks)>= 0 and int(marks) <= 100 :
		rno = int(rno)
		name = str(name)
		marks = int(marks)
		try:
			con = connect("SMS.db")
			cursor = con.cursor()
			sql = "insert into student values('%d','%s','%d')"
			cursor.execute(sql % (rno ,name ,marks))
			con.commit()
			messagebox.showinfo("Sucess","Record Added Successfully")	
			query ="select * from student"
			cursor.execute(query)
			result = pd.read_sql_query(query, con)
			result.to_csv("Student Data"+".csv", index=False)	
			add_win_ent_rno.delete(0,END)
			add_win_ent_name.delete(0,END)
			add_win_ent_marks.delete(0,END)
			add_win_ent_rno.focus()
		except Exception as e:
			messagebox.showerror("issue",e)
			con.rollback()
		finally:
			if con is not None:
				con.close()
	else:
		if add_win_ent_rno.get() == "":
			messagebox.showerror("RNO VAL","Please Enter the Roll No")
		elif add_win_ent_name.get() == "":
			messagebox.showerror("Name VAL","Please Enter the Name")
		elif add_win_ent_marks.get() == "":
			messagebox.showerror("Marks VAL","Please Enter the Marks")
		elif rno.isnumeric() != True:
			messagebox.showerror("RNO VAL 1","Please Enter the +VE integers only In RNO Field")
		elif int(rno) < 0 and rno.isnumeric() != True:
			messagebox.showerror("RNO VAL 2","Please Enter Only + VE Integers in Rno field")
		elif name.isalpha() != True:
			messagebox.showerror("Name VAL 1","Please Enter Only Alphabets in Name field")
		elif int(len(name)) <= 1 :
			messagebox.showerror("Name VAL 2","Please Enter the name having 2 or more than 2 alphabets")
		elif marks.isalpha() == True:
			messagebox.showerror("Marks VAL 1","Please Enter + ve Integers in MArks field")
		elif int(marks) < 0 != True :
			messagebox.showerror("Marks VAL 2","Please Enter the Marks in range of 0-100 only")
		elif int(marks) > 100 != True :
			messagebox.showerror("Marks VAL 3","Please Enter the Marks in range of 0-100 only")
		else:
			messagebox.showerror("Error","Invalid Reason")
def view():
	info = ""
	con = None
	try:
		con = connect("SMS.db")
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			info = info + "rno : " + str(d[0]) + " \t " +  "name : " + str(d[1]) + 2*" \t " +  "marks : " + str(d[2]) + "\n"
		view_win_st_data.insert(INSERT ,info)
	except Exception as e:
		messagebox.showerror("issue",e)
	finally:
		if con is not None:
			con.close()
def delete():
	con = None
	rno = del_win_ent_rno.get()
	if rno.isnumeric() :
		rno = int(rno)
		try:
			con = connect("SMS.db")
			cursor = con.cursor()
			sql = "delete from student where rno = '%s'"
			cursor.execute(sql % (rno))
			if cursor.rowcount == 1:
				con.commit()
				messagebox.showinfo("INFO",("Record of RNO " + del_win_ent_rno.get() + " successfully Deleted"))
				query ="select * from student"
				cursor.execute(query)
				result = pd.read_sql_query(query, con)
				result.to_csv("Student Data"+".csv", index=False)	
				del_win_ent_rno.delete(0,END)
				del_win_ent_rno.focus()
			else:
				messagebox.showwarning("Warning",("Record of RNO "+ del_win_ent_rno.get() + " Does Not Exist"))
				con.rollback()
		except Exception as e:
				messagebox.showerror("issue",e)
		finally:
			if con is not None:
				con.close()
	else:
		if del_win_ent_rno.get() == "":
			messagebox.showerror("RNO VAL","Please Enter the Roll No")
		elif rno.isnumeric() != True:
			messagebox.showerror("RNO VAL 1","Please Enter the +VE integers only In RNO Field")
		elif int(rno) < 0 and rno.isnumeric() != True:
			messagebox.showerror("RNO VAL 2","Please Enter Only + VE Integers in Rno field")
		else:
			messagebox.showerror("ERROR","Invalid reason")
def update():
	con = None
	rno = up_win_ent_rno.get()
	name = up_win_ent_name.get()
	marks = up_win_ent_marks.get()
	if rno.isnumeric() and name.isalpha() and marks.isnumeric() and len(name) > 1 and int(marks)>= 0 and int(marks) <= 100 :
		rno = int(rno)
		name = str(name)
		marks = int(marks)
		try:
			con = connect("SMS.db")
			cursor = con.cursor()
			sql="update student set name ='%s',marks = '%d' where rno = '%d' "
			cursor.execute(sql % (name,marks,rno))
			if cursor.rowcount==1:
				con.commit()
				messagebox.showinfo("INFO",("Record of RNO " + up_win_ent_rno.get() + " successfully Updated"))
				query ="select * from student"
				cursor.execute(query)
				result = pd.read_sql_query(query, con)
				result.to_csv("Student Data"+".csv", index=False)
				up_win_ent_rno.delete(0,END)
				up_win_ent_name.delete(0,END)
				up_win_ent_marks.delete(0,END)
				up_win_ent_rno.focus()
			else:
				messagebox.showwarning("Warning",("Record of RNO "+ up_win_ent_rno.get() + " Does Not Exist"))
				up_win_ent_rno.focus()
		except Exception as e:
			messagebox.showerror("issue",e)
			con.rollback()
		finally:
			if con is not None:
				con.close()
	else:
		if up_win_ent_rno.get() == "":
			messagebox.showerror("RNO VAL","Please Enter the Roll No")
		elif up_win_ent_name.get() == "":
			messagebox.showerror("Name VAL","Please Enter the Name")
		elif up_win_ent_marks.get() == "":
			messagebox.showerror("Marks VAL","Please Enter the Marks")
		elif rno.isnumeric() != True:
			messagebox.showerror("RNO VAL 1","Please Enter the + VE integers only in RNO Field")
		elif int(rno) < 0 and rno.isnumeric() != True:
			messagebox.showerror("RNO VAL 2","Please Enter Only + VE integers in Rno field")
		elif name.isalpha() != True:
			messagebox.showerror("Name VAL 1","Please Enter Only Alphabets in Name field")
		elif int(len(name)) <= 1 :
			messagebox.showerror("Name VAL 2","Please Enter the name having 2 or more than 2 alphabets")
		elif marks.isalpha() == True:
			messagebox.showerror("Marks VAL 1","Please Enter + VE Integers in Marks field")
		elif int(marks) < 0 != True :
			messagebox.showerror("Marks VAL 2","Please Enter the Marks in range of 0-100 only")
		elif int(marks) > 100 != True :
			messagebox.showerror("Marks VAL 3","Please Enter the Marks in range of 0-100 only")
		else:
			messagebox.showerror("ERROR","Invalid reason")
def DSF():
	data = pd.read_csv("Student Data.csv")
	while True:
		op = int(input("press 1 to find data of particular Roll No:\n press 2 to find data of Particular student :\npress 3 to find the group or single data of student using marks :"))
		if op ==1:
			n = int(input("Enter the Roll Number of student: "))
			d = data[data.rno == n]
			print(d)
		elif op == 2:
			n = str(input("Enter the student name : "))
			d = data[data.name == n]
			print(d)
		elif op == 3:
			op = int(input("press 1 if you want to find student having same marks : \n or \n press 2 if you want to find student records using marks range :"))
			if op == 1:
				n = int(input("Enter the marks :"))
				d = data[data.marks == n ]
				print(d)
			elif op == 2:
				print("Enter the Marks limits: ")
				n1 = int(input("Enter the start limit of marks :"))
				n2 = int(input("Enter the end limit of marks :"))

				d =  data[(data.marks >= n1) & (data.marks <=n2) ]
				print(d)
		else:
			print("Invalid Choice")
			break
def PLOT():
	data = pd.read_csv("Student Data.csv")
	name = data['name'].tolist()
	marks = data['marks'].tolist()

	plt.bar(name,marks,width=0.25,color=['red','orange', 'blue', 'cyan', 'yellow'])

	plt.xlabel("NAME")
	plt.ylabel("MARKS")
	plt.title("Basic Information !")

	plt.legend()
	plt.grid()
	plt.show()
#code for Quote
wa = "https://www.brainyquote.com/quote_of_the_day"
res = requests.get(wa)
data = bs4.BeautifulSoup(res.text,"html.parser")	
info = data.find("img",{"class":"p-qotd"})	
qotd = info['alt']
q = ("Daily Quote" + " : \n")
quote = (q + qotd)


#code for Location
wl = "https://ipinfo.io/"
res1 = requests.get(wl)
data1 = res1.json()
city = data1['city']
state = data1['region']
location = city +','+ state
loc = ("Location")

#code for Temperature
a = "http://api.openweathermap.org/data/2.5/weather?units=metric"
b = "&q=" + city
c = "&appid=" + "c6e315d09197cec231495138183954bd"
webadd = a+b+c

res2 = requests.get(webadd)
data2 = res2.json()	
tp = data2['main']['temp']
t = str(tp)
temp = ('Temperature'+' : '+ t + '\u2103')


#============ code for Main Window ==============
main_win = Tk()
main_win.title("S.M.S")
main_win.geometry("600x600+450+130")
main_win.resizable(False,False)
#code for Background image
bg  = ImageTk.PhotoImage(file = "bg2.jpg")
bg_image = Label(main_win,image = bg).place(x=0,y=0,relwidth=1,relheight=1)

f  = ("Times New Roman",25,)
f1  = ("Roboto",16)
f2  = ("Helvetica",15)
fn = ("Helvetica",11)
f3 = ("Helvetica",20)

# code for buttons 
main_win_btn_add = Button(main_win,text = "Add",command=F1,font = f,fg = "#C0C0C0",bg = "#000033",border=2,cursor = "hand2")
main_win_btn_add.place(width = 160,height = 50 , x = 220 , y = 140)

main_win_btn_view= Button(main_win,text = "View",command=lambda:[F5(),view()],font = f,fg = "#C0C0C0",bg = "#000033",border=2,cursor = "hand2")
main_win_btn_view.place(width = 160,height = 50 , x = 220 , y = 205)

main_win_btn_update = Button(main_win,text = "Update",command=F3,font = f,fg = "#C0C0C0",bg = "#000033",border=2,cursor = "hand2")
main_win_btn_update.place(width = 160,height = 50 , x = 220 , y = 270)

main_win_btn_delete = Button(main_win,text = "Delete",command=F7,font = f,fg = "#C0C0C0",bg = "#000033",border=2,cursor = "hand2")
main_win_btn_delete.place(width = 160,height = 50 , x = 220 , y = 335)

main_win_btn_charts = Button(main_win,text = "Ad.Task",command=F9 ,font = f,fg = "#C0C0C0",bg = "#000033",border=2,cursor = "hand2")
main_win_btn_charts.place(width = 160,height = 50 , x = 220 , y =400)


#code for labels 
main_win_lbl_quote = Label(main_win,text = quote,font = fn,fg = "#C0C0C0",bg = "#000033",anchor =W)
main_win_lbl_quote.place(x = 0 ,y = 20, height = 50 ,width = 600 )

main_win_lbl_loc = Label(main_win,text = (loc,":",location),font = f1,fg = "#C0C0C0",bg = "#000033",anchor =W)
main_win_lbl_loc.place(x = 0 ,y = 510 ,height = 45 ,width = 310)

main_win_lbl_temp = Label(main_win,text = temp,font = f1,fg = "#C0C0C0",bg = "#000033",anchor =W)
main_win_lbl_temp.place(x = 370 ,y = 510 ,height = 45 ,width = 200)
 

#============== code for add window ================

add_win = Toplevel(main_win)
add_win.title("Add Students")
add_win.geometry("600x600+450+130")
add_win.resizable(False,False)

bg1  = ImageTk.PhotoImage(file = "add.jpg")
bg1_image = Label(add_win,image = bg1).place(x=0,y=0,relwidth=1,relheight=1)


add_win_lbl_rno = Label(add_win,text = "Enter Roll Number" ,font = f2,fg = "Black",bg = "Aquamarine") 
add_win_lbl_rno.place(x = 200  ,y = 30 ,height = 45 ,width = 200)

add_win_ent_rno = Entry(add_win,font = f2,fg = "black",bg = "LightCyan",justify = CENTER) 
add_win_ent_rno.place(x = 150  ,y = 90 ,height = 45 ,width = 300)

add_win_lbl_name = Label(add_win,text = "Enter Student Name" ,font = f2,fg = "Black",bg = "Aquamarine") 
add_win_lbl_name.place(x = 200  ,y = 160 ,height = 45 ,width = 200)

add_win_ent_name = Entry(add_win,font = f2,fg = "black",bg = "LightCyan",justify = CENTER) 
add_win_ent_name.place(x = 150  ,y = 220 ,height = 45 ,width = 300)

add_win_lbl_marks = Label(add_win,text = "Enter Student Marks" ,font = f2,fg = "Black",bg = "Aquamarine") 
add_win_lbl_marks.place(x = 200  ,y = 290 ,height = 45 ,width = 200)

add_win_ent_marks = Entry(add_win,font = f2,fg = "black",bg = "LightCyan",justify = CENTER) 
add_win_ent_marks.place(x = 150  ,y = 350 ,height = 45 ,width = 300)

add_win_btn_clear = Button(add_win,text = "Clear",font = f,command = add_clear,fg = "black",bg = "MediumTurquoise",border=2,cursor = "hand2")
add_win_btn_clear.place(width = 160,height = 50 , x = 30 , y = 470)

add_win_btn_save = Button(add_win,text = "Save",font = f,command = save,fg = "black",bg = "OrangeRed",border=2,cursor = "hand2")
add_win_btn_save.place(width = 160,height = 50 , x = 220 , y = 470)

add_win_btn_back = Button(add_win,text = "Back",command=F2,font = f,fg = "black",bg = "SpringGreen",border=2,cursor = "hand2")
add_win_btn_back.place(width = 160,height = 50 , x = 410 , y = 470)

add_win.withdraw()

#============== code for Update window ================

up_win = Toplevel(main_win)
up_win.title("Update Students")
up_win.geometry("600x600+450+130")
up_win.resizable(False,False)

bg2  = ImageTk.PhotoImage(file = "update.jpg")
bg2_image = Label(up_win,image = bg2).place(x=0,y=0,relwidth=1,relheight=1)


up_win_lbl_rno = Label(up_win,text = "Enter Roll Number" ,font = f2,fg = "Black",bg = "Aquamarine") 
up_win_lbl_rno.place(x = 200  ,y = 30 ,height = 45 ,width = 200)

up_win_ent_rno = Entry(up_win,font = f2,fg = "black",bg = "LightCyan",justify = CENTER) 
up_win_ent_rno.place(x = 150  ,y = 90 ,height = 45 ,width = 300)

up_win_lbl_name = Label(up_win,text = "Enter Student Name" ,font = f2,fg = "Black",bg = "Aquamarine") 
up_win_lbl_name.place(x = 200  ,y = 160 ,height = 45 ,width = 200)

up_win_ent_name = Entry(up_win,font = f2,fg = "black",bg = "LightCyan",justify = CENTER) 
up_win_ent_name.place(x = 150  ,y = 220 ,height = 45 ,width = 300)

up_win_lbl_marks = Label(up_win,text = "Enter Student Marks" ,font = f2,fg = "Black",bg = "Aquamarine") 
up_win_lbl_marks.place(x = 200  ,y = 290 ,height = 45 ,width = 200)

up_win_ent_marks = Entry(up_win,font = f2,fg = "black",bg = "LightCyan",justify = CENTER) 
up_win_ent_marks.place(x = 150  ,y = 350 ,height = 45 ,width = 300)

up_win_btn_clear = Button(up_win,text = "Clear",font = f,command = up_clear,fg = "black",bg = "MediumTurquoise",border=2,cursor = "hand2")
up_win_btn_clear.place(width = 120,height = 50 , x = 30 , y = 470)

up_win_btn_search = Button(up_win,text = "Search",font = f,command = search,fg = "black",bg = "Aquamarine",border=2,cursor = "hand2")
up_win_btn_search.place(width = 120,height = 50 , x = 170 , y = 470)

up_win_btn_update = Button(up_win,text = "Update",font = f,command=update,fg = "black",bg = "OrangeRed",border=2,cursor = "hand2")
up_win_btn_update.place(width = 120,height = 50 , x = 310 , y = 470)

up_win_btn_back = Button(up_win,text = "Back",command=F4,font = f,fg = "black",bg = "SpringGreen",border=2,cursor = "hand2")
up_win_btn_back.place(width = 120,height = 50 , x = 450 , y = 470)

up_win.withdraw()

#============== code for view window ================

view_win = Toplevel(main_win)
view_win.title("View Students")
view_win.geometry("600x600+450+130")
view_win.resizable(False,False)

bg3  = ImageTk.PhotoImage(file = "view.jpg")
bg3_image = Label(view_win,image = bg3).place(x=0,y=0,relwidth=1,relheight=1)

view_win_st_data = ScrolledText(view_win,width=40,height=10,font=("Times New Roman",17),bg="PowderBlue",fg="black")
view_win_btn_back = Button(view_win,text="Back",command=F6,font=f,fg = "black",bg = "MediumTurquoise",border=2,cursor = "hand2")

view_win_st_data.place(x = 70 , y = 90)
view_win_btn_back.place(x = 220 , y = 470,width=160,height=50)

view_win.withdraw()

#============ code for delete window ==================

del_win = Toplevel(main_win)
del_win.title("Delete Students")
del_win.geometry("600x600+450+130")
del_win.resizable(False,False)

bg4  = ImageTk.PhotoImage(file ="del.jpg")
bg4_image = Label(del_win,image = bg4).place(x=0,y=0,relwidth=1,relheight=1)

del_win_lbl_rno = Label(del_win,text = "Enter Roll Number" ,font = f3,fg = "Black",bg = "Aquamarine") 
del_win_lbl_rno.place(x = 170  ,y = 40 ,height = 45 ,width = 280)

del_win_ent_rno = Entry(del_win,font = f2,fg = "black",bg = "LightCyan",justify = CENTER) 
del_win_ent_rno.place(x = 110  ,y = 110 ,height = 45 ,width = 400)

del_win_btn_clear = Button(del_win,text = "Clear",font = f,fg = "black",command = del_clear,bg = "MediumTurquoise",border=2,cursor = "hand2")
del_win_btn_clear.place(width = 160,height = 50 , x = 30 , y = 250)

del_win_btn_save = Button(del_win,text = "Delete",font = f,command=delete,fg = "black",bg = "OrangeRed",border=2,cursor = "hand2")
del_win_btn_save.place(width = 160,height = 50 , x = 220 , y = 250)

del_win_btn_back = Button(del_win,text = "Back",command=F8,font = f,fg = "black",bg = "SpringGreen",border=2,cursor = "hand2")
del_win_btn_back.place(width = 160,height = 50 , x = 410 , y = 250)

del_win.withdraw()

#============== code for Administrative Task ==================
ad_win = Toplevel(main_win)
ad_win.title("Administrative Task")
ad_win.geometry("600x600+450+130")
ad_win.resizable(False,False)

bg5 = ImageTk.PhotoImage(file ="admin.jpg")
bg5_image = Label(ad_win,image = bg5).place(x=0,y=0,relwidth=1,relheight=1)

ad_win_btn_charts = Button(ad_win,text = "Charts",command=PLOT,font = f,fg = "black",bg = "MediumTurquoise",border=2,cursor = "hand2")
ad_win_btn_charts.place(width = 160,height = 50 , x = 220 , y = 210)

ad_win_btn_cli= Button(ad_win,text = "CLI",command=DSF,font = f,fg = "black",bg = "OrangeRed",border=2,cursor = "hand2")
ad_win_btn_cli.place(width = 160,height = 50 , x = 220 , y = 275)

ad_win_btn_back = Button(ad_win,text = "Back",command=F10,font = f,fg = "black",bg = "SpringGreen",border=2,cursor = "hand2")
ad_win_btn_back.place(width = 160,height = 50 , x = 220 , y = 340)

ad_win.withdraw()
		
main_win.mainloop()

