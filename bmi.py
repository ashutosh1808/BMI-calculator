from tkinter import *
from math import *
from tkinter.messagebox import *
from mysql.connector import *
import mysql.connector.errorcode
import pandas.io.sql as sql
from tkinter.scrolledtext import *
from datetime import *
import xlwt
def f1():
	bmi_window.deiconify()
	main_window.withdraw()
def f2():
	main_window.deiconify()
	bmi_window.withdraw()	
def f3():
	convert_window.deiconify()
	bmi_window.withdraw()
def f4():
	try:
		hf=float(cw_ent_hf.get())	
		hi=float(cw_ent_hi.get())
		if hf in range(1,8) and hi in range(0,12):
			hm=round(hf*0.3048+hi*0.0254,3)
			showinfo("Height converted in metres",str(hm))
		else:
			showerror("Input issue","Height in ft shud be between 1 and 7"+"\n"+"Height in inch shud be between 0 and 11")
	except (ValueError,TypeError):
		showerror("Issue","Enter numbers only")
	except Exception as e:
		showerror("Failure",str(e))
	cw_ent_hf.delete(0,END);cw_ent_hi.delete(0,END)
def f5():
	bmi_window.deiconify()
	convert_window.withdraw()
def f7():
	main_window.deiconify()
	history_window.withdraw()
def f8():
	res=""
	con=None
	try:
		con=connect(host='localhost',user='root',password='abc456',database='bmi_25dec21')
		cursor=con.cursor()
		sql="insert into person values('%s','%s','%f','%d','%d','%d','%f')"
		name=bw_ent_name.get().capitalize()
		gender=""
		if op.get()==1:
			gender="Male"
		elif op.get()==2:	
			gender="Female"
		height=float(bw_ent_ht.get())
		weight=float(bw_ent_wt.get())
		phone=int(bw_ent_phone.get())
		age=int(bw_ent_age.get())
		bmi=weight/pow(height,2)
		cursor.execute(sql%(name,gender,height,weight,phone,age,bmi))
		if bmi<18.5:
			res="Aap patley ho"
		elif bmi<24.9:
			res='Aap normal ho'
		elif bmi<29.9:
			res="Aap motey ho"
		else:
			res="Aap bahut motey ho"
		showinfo("Success","Your name is "+str(name).capitalize()+"\n"+"Your age is "+str(age)+"\n"+"Your gender is "+gender+"\n"+"Your BMI is: "+str(bmi)+"\n"+res)
		con.commit()
	except ValueError:
		showerror("Failure","Invalid height/phone no/weight/age entered"+"\n"+"Enter numeric values in the specified columns")
		con.rollback()
	except ZeroDivisionError:
		showerror("Issue","Height cannot be zero");	con.rollback()
	except TypeError:
		con.rollback()
	except UnboundLocalError:
		con.rollback()
	except mysql.connector.Error as e:
		showerror("Failure",str(e.msg))
		con.rollback()
	finally:
		if con is not None:
			con.close()
	bw_ent_name.delete(0,END)
	bw_ent_ht.delete(0,END)
	bw_ent_wt.delete(0,END)
	bw_ent_phone.delete(0,END)
	bw_ent_age.delete(0,END)
	bw_ent_name.focus()
def f9():
	co=0;con=None
	try:
		con=connect(host='localhost',user='root',password='abc456',database='bmi_25dec21')
		cursor=con.cursor()
		sql="select * from person"
		cursor.execute(sql)
		data=cursor.fetchall()
		for d in data:
			co=co+1
		return co
	except Exception as e:
		showerror("Issue",str(e))
	finally:
		if con is not None:
			con.close()
def f10():
	history_window.deiconify()
	main_window.withdraw()
	con=None
	try:
		con=connect(host='localhost',user='root',password='abc456',database='bmi_25dec21')
		cursor=con.cursor()
		sql="select * from person"
		cursor.execute(sql)
		data=cursor.fetchall()
		info=""
		for d in data:
			info=info+"Name- "+str(d[0])+"\n"+"Gender- "+str(d[1])+"\n"+"Age- "+str(d[5])+"\n"+"BMI- "+str(d[6])+"\n"+"*"*79+"\n"
		hw_st_data.insert(INSERT,info)
	except Exception as e:
		showerror("Issue",str(e.msg))
	finally:
		if con is not None:
			con.close()
def f11():
	con=None
	try:
		con=connect(host='localhost',user='root',password='abc456',database='bmi_25dec21')
		df=sql.read_sql('select * from person',con)
		df.to_excel("bkp9.xls")
		showinfo("Success","Data export successful")
		con.commit()	
	except Exception as e:
		showerror("Issue: ",str(e))
		con.rollback()
	finally:
		if con is not None:
			con.close()
def on_close():
	response=askyesno('Exit','Are you sure you want to exit?')
	if response:
		main_window.destroy()
main_window=Tk()
main_window.title("BMI Calculator")
main_window.geometry("1000x800+40+30")
main_window.config(bg="yellow")
main_window.iconbitmap("health_heart.ico")
main_window.protocol('WM_DELETE_WINDOW',on_close)

f=("Cambria",20,"bold")
bmi_window=Toplevel(main_window)
bmi_window.title("BMI Calculator")
bmi_window.geometry("1000x800+40+30")
bmi_window.iconbitmap("running_man.ico")
bmi_window.protocol('WM_DELETE_WINDOW',on_close)
bmi_window.config(bg="red")
bw_lbl_welcome=Label(bmi_window,text="PLEASE FILL IN YOUR DETAILS !",font=f,bg='red',fg='yellow')
bw_lbl_welcome.place(x=370,y=10)
bw_lbl_name=Label(bmi_window,text="enter your name",font=f,bg="red",fg='yellow')
bw_ent_name=Entry(bmi_window,font=f,bd=3)
bw_lbl_name.place(x=20,y=90)
bw_ent_name.place(x=400,y=90)
bw_lbl_gender=Label(bmi_window,text="select ur gender",font=f,bg="red",fg='yellow')
bw_lbl_gender.place(x=20,y=160)
op=IntVar()
op.set(1)
bw_rbMale=Radiobutton(bmi_window,text="Male",font=f,variable=op,value=1)
bw_rbFemale=Radiobutton(bmi_window,text="Female",font=f,variable=op,value=2)
bw_rbMale.place(x=400,y=160);bw_rbFemale.place(x=550,y=160)
bw_ent_phone=Entry(bmi_window,font=f,bd=3);bw_ent_phone.place(x=400,y=220)
bw_lbl_phone=Label(bmi_window,text="enter phone no",font=f,bg="red",fg='yellow')
bw_lbl_phone.place(x=20,y=220)
bw_lbl_ht=Label(bmi_window,text="enter height(in metres)",font=f,bg="red",fg='yellow')
bw_ent_ht=Entry(bmi_window,font=f,bd=3)
bw_lbl_ht.place(x=20,y=300);bw_ent_ht.place(x=400,y=300)
bw_btn_conv=Button(bmi_window,text="convert to metres",font=f,bd=3,command=f3)
bw_btn_conv.place(x=730,y=300)
bw_lbl_wt=Label(bmi_window,font=f,text="enter ur weight(in kgs)",bg="red",fg='yellow')
bw_lbl_wt.place(x=20,y=420)
bw_ent_wt=Entry(bmi_window,font=f,bd=3)
bw_ent_wt.place(x=400,y=420)
bw_lbl_age=Label(bmi_window,font=f,text="enter ur age",bg="red",fg='yellow')
bw_lbl_age.place(x=20,y=500)
bw_ent_age=Entry(bmi_window,font=f,bd=3)
bw_ent_age.place(x=400,y=500)
bw_btn_submit=Button(bmi_window,font=f,text="Submit here",bd=4,command=f8)
bw_btn_submit.place(x=30,y=600)
bw_btn_back=Button(bmi_window,font=f,text="Back",bd=4,command=f2)
bw_btn_back.place(x=700,y=600)
bmi_window.withdraw()

convert_window=Toplevel(bmi_window)
convert_window.geometry("500x400+40+30")
convert_window.title("Convert ur height")
convert_window.config(bg="green")
convert_window.iconbitmap("height_measure.ico")
convert_window.protocol('WM_DELETE_WINDOW',on_close)
cw_lbl_hf=Label(convert_window,font=f,text="enter height (ft)",bg='green',fg='yellow')
cw_lbl_hf.pack(pady=10)
cw_ent_hf=Entry(convert_window,font=f,bd=4)
cw_ent_hf.pack(pady=10)
cw_lbl_hi=Label(convert_window,font=f,text="enter height (inch)",bg='green',fg='yellow')
cw_lbl_hi.pack(pady=10)
cw_ent_hi=Entry(convert_window,font=f,bd=4)
cw_ent_hi.pack(pady=10)
cw_btn_find=Button(convert_window,text="Convert",font=f,command=f4)
cw_btn_find.pack(pady=10)
cw_btn_back=Button(convert_window,text="Back",font=f,command=f5)
cw_btn_back.pack(pady=10)
convert_window.withdraw()

history_window=Toplevel(main_window)
history_window.geometry("1000x800+40+30")
history_window.title("History")
history_window.iconbitmap("history_clock.ico")
history_window.protocol('WM_DELETE_WINDOW',on_close)
history_window.config(bg="magenta")
hw_st_data=ScrolledText(history_window,width=60,height=18,font=f)
hw_st_data.place(x=10,y=10)
hw_btn_back=Button(history_window,text="Back",font=f,bd=3,command=f7)
hw_btn_back.place(x=500,y=600)
history_window.withdraw()

d=datetime.now();	d1=str(d)
res=""
hr=d.hour
if hr<12:
	res="Good morning"
elif hr<16:
	res="Good afternoon"
else:
	res="Good evening"
lbl_dt=Label(main_window,font=f,text=d1+str(hr)+"\n"+res)
lbl_dt.pack(pady=10)
btn_bmi=Button(main_window,font=f,text="Calculate BMI",bd=3,command=f1)
btn_bmi.pack(pady=10)
btn_hist=Button(main_window,font=f,text="View History",bd=3,command=f10)
btn_hist.pack(pady=10)
btn_exp=Button(main_window,font=f,text="Export data",bd=3,command=f11)
btn_exp.pack(pady=10)
ans=f9()
lbl_co=Label(main_window,font=f,text="Count = "+str(ans))
lbl_co.pack(pady=10)
main_window.mainloop()