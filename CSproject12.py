# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 16:22:26 2019

@author: admin

This is vandan.
"""

from tkinter import *
from tkinter.ttk import *
import mysql.connector as sql
import datetime

mydb=sql.connect(host="localhost",user="root",passwd="1609",db="Medstore")
cursor=mydb.cursor()
mydb.close()

def click_login(uid,passwd,caller,wrong_c):
    mydb.connect()
    cursor.execute(f"select passwd from staff where username='{uid}'")
    output=cursor.fetchall()
    if cursor.rowcount==1:
        epassw=output[0][0]
        if epassw==passwd:
            cursor.execute(f"select post from staff where username='{uid}'")
            post=(cursor.fetchall())[0][0]
            caller.destroy()
            MainMenu(post)   
        else:
            wrong_c.grid(row=0,column=2)
    else:
        wrong_c.grid(row=0,column=2)
    
#%% Login page        
def LoginPage():
    login=Tk()
    login.title("Login")
    fm1=Frame(login)
    fm1.grid(row=2,column=1,sticky=W)
    Label(login,text="Username: ").grid(row=0,column=0)
    Label(login,text="Password: ").grid(row=1,column=0)
    wrong_c=Label(fm1, text="Wrong credentials. Try again.")
    username,passwd=StringVar(),StringVar()
    Entry(login, textvariable=username,width=50).grid(row=0,column=1)
    Entry(login, textvariable=passwd,width=50,show='*').grid(row=1,column=1)
    Button(fm1, text="LOG IN", command=lambda: click_login(username.get(),passwd.get(),login,wrong_c)).grid(row=0,column=0,sticky=W)
    Button(fm1, text="SIGN UP", command=lambda: SignUp(login)).grid(row=0,column=1)
    login.mainloop()

#%%
def MainMenu(post):
    mnmnu=Tk()
    mnmnu.title("Main Menu")
    fr1=Frame(mnmnu)
    fr1.grid(row=0,column=0)
    Button(fr1,text="Billing",width=25).grid(row=0,column=0)
    Button(fr1,text="Stock",command=lambda: stock(mnmnu),width=25).grid(row=0,column=1)
    Button(fr1,text="Customers",width=25).grid(row=1,column=0)
    Button(fr1,text="History",width=25).grid(row=1,column=1)
    if post=="Manager":
        Button(fr1,text="Employees",width=50,command=lambda: employee(mnmnu)).grid(row=2,column=0,columnspan=2)
    mnmnu.mainloop()
    
#%%
def SignUp(caller):
    caller.destroy()
    newacc=Tk()
    newacc.title("Sign up")
    newacc.geometry("500x370")
    Label(newacc,text="Enter employee id*: ").grid(row=0,column=0,sticky=W)
    Label(newacc,text="Enter initial passcode*: ").grid(row=1,column=0,sticky=W)
    Label(newacc,text="Enter your name*: ").grid(row=2,column=0,sticky=W)
    Label(newacc,text="Enter username*: ").grid(row=3,column=0,sticky=W)
    Label(newacc,text="Enter password*: ").grid(row=4,column=0,sticky=W)
    Label(newacc,text="Re-enter password*: ").grid(row=5,column=0,sticky=W)
    Label(newacc,text="Enter mobile number: ").grid(row=6,column=0,sticky=W)
    Label(newacc,text="Enter date of birth: ").grid(row=7,column=0,sticky=W)
    Label(newacc,text="Select gender: ").grid(row=8,column=0,sticky=NW)
    Label(newacc,text="(Fields marked '*' are important)").grid(row=10,column=0,columnspan=2,sticky=W)
    Label(newacc,text="(Contact employer for the first 2 fields)").grid(row=9,column=0,columnspan=2,sticky=W)
    eid,ipass,name,uname,passwd,repass,mobno,dob,gender=StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
    gender.set(None)
    Entry(newacc, textvariable=eid, width=20).grid(row=0,column=1,sticky=W)
    Entry(newacc, textvariable=ipass, width=20,show='*').grid(row=1,column=1,sticky=W)
    Entry(newacc, textvariable=name, width=30).grid(row=2,column=1,sticky=W)
    Entry(newacc, textvariable=uname, width=30).grid(row=3,column=1,sticky=W)
    Entry(newacc, textvariable=passwd, width=30,show='*').grid(row=4,column=1,sticky=W)
    Entry(newacc, textvariable=repass, width=30,show='*').grid(row=5,column=1,sticky=W)
    Entry(newacc, textvariable=mobno, width=30).grid(row=6,column=1,sticky=W)
    Entry(newacc, textvariable=dob, width=25).grid(row=7,column=1,sticky=W)
    gen=Frame(newacc)
    gen.grid(row=8,column=1,sticky=W)  
    r1=Radiobutton(gen,text="Prefer not to specify",variable=gender,value="null")
    r1.grid(row=0,column=0,columnspan=2,sticky=W)
    Radiobutton(gen,text="Male",variable=gender,value="'M'").grid(row=1,column=0,sticky=W)
    Radiobutton(gen,text="Female",variable=gender,value="'F'").grid(row=1,column=1,sticky=W)
    Radiobutton(gen,text="Others",variable=gender,value="'O'").grid(row=1,column=2,sticky=W)
    Button(newacc, text="ADD ACCOUNT",command=lambda: click_createacc(eid.get(),
                                                                      name.get(),
                                                                      ipass.get(),
                                                                      uname.get(),
                                                                      passwd.get(),
                                                                      repass.get(),
                                                                      mobno.get(),
                                                                      dob.get(),
                                                                      gender.get(),
                                                                      newacc)).grid(row=11,column=0,sticky=W)
    newacc.mainloop()
    
def click_createacc(eid,name,ipass,uname,passwd,repass,mobno,dob,gender,caller):
    mydb.connect()
    cursor.execute(f"select ipass,name from staff where eid='{eid}'")
    check = cursor.fetchall()
    print(check) #remove later
    error=Frame(caller)
    error.grid(row=11,column=1,ipadx=83,sticky=W)
    if cursor.rowcount == 0:
        Label(error, text="Please contact your employer for a valid ID.", fg="red").pack(fill='x',side=LEFT)
    elif not check[0][1]==None:
        Label(error, text="You have already made an account.", fg="red").pack(fill='x',side=LEFT)
    elif not ipass==check[0][0]:
        Label(error, text="Please contact your employer for a valid initial passcode.", fg="red").pack(fill='x',side=LEFT)
    elif name=='':
        Label(error, text="Please enter your name.",fg="red").pack(fill='x',side=LEFT)
    elif len(uname)<8:
        Label(error, text="Username must be at least 8 chars long.",fg="red").pack(fill='x',side=LEFT)
    elif len(passwd)<8:
        Label(error, text="Password must be at least 8 chars long.", fg="red").pack(fill='x',side=LEFT)
    elif not repass==passwd:
        Label(error, text="Passwords do not match.", fg="red").pack(fill='x',side=LEFT)
    else:
        dob="'"+dob+"'" if not dob=='' else 'null'
        mobno='null' if mobno=='' else "'"+mobno+"'"
        cursor.execute(f"update staff set\
                       name='{name}',\
                       username='{uname}',\
                       passwd='{passwd}',\
                       mobile={mobno},\
                       gender={gender},\
                       dob={dob} \
                       where eid='{eid}'")
        mydb.commit()
        mydb.close()
        caller.destroy()
        LoginPage()
        
#%% 
def stock(caller):
    caller.destroy()
    inventory=Tk()
    additems=Frame(inventory)
    additems.grid(row=1,column=0,columnspan=3,sticky=W)
    Label(inventory,text="Add to stock:-\n").grid(row=0,column=0,sticky=W)
    Label(additems,text="Seriel no.*:").grid(row=0,column=0,sticky=W)
    Label(additems,text="Batch code*:").grid(row=0,column=2,sticky=W)
    Label(additems,text="Manufacturer:").grid(row=1,column=0,sticky=W)
    Label(additems,text=" Supplier:").grid(row=1,column=2,sticky=W)
    Label(additems,text="Product name*:").grid(row=2,column=0,sticky=W)
    Label(additems,text=" Quantity:").grid(row=2,column=2,sticky=W)
    Label(additems,text=" Rate*:").grid(row=2,column=4,sticky=W)
    Label(additems,text="Expiry:").grid(row=3,column=0,sticky=W)
    Label(inventory,text="Fields marked '*' are important.").grid(row=2,column=0,sticky=W)
    seriel,batchcode,manu,supp,pname,qty,rate,exp=StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
    e1=Entry(additems,textvariable=seriel,width=20)
    e1.grid(row=0,column=1,sticky=W)
    e2=Entry(additems,textvariable=batchcode,width=20)
    e2.grid(row=0,column=3,columnspan=3,sticky=W)
    e3=Entry(additems,textvariable=manu,width=30)
    e3.grid(row=1,column=1,sticky=W)
    e4=Entry(additems,textvariable=supp,width=30)
    e4.grid(row=1,column=3,columnspan=3,sticky=W)
    e5=Entry(additems,textvariable=pname,width=30)
    e5.grid(row=2,column=1,sticky=W)
    e6=Entry(additems,textvariable=qty,width=10)
    e6.grid(row=2,column=3,sticky=W)
    e7=Entry(additems,textvariable=rate,width=12)
    e7.grid(row=2,column=5,sticky=W)
    e8=Entry(additems,textvariable=exp,width=20)
    e8.grid(row=3,column=1,sticky=W)
    entries=[e1,e2,e3,e4,e5,e6,e7,e8]
    Button(inventory,text="Add entry",command=lambda: click_entry("new",inventory,entries,tree,
                                                                  seriel.get(),
                                                                  manu.get(),
                                                                  supp.get(),
                                                                  pname.get(),
                                                                  qty.get(),
                                                                  rate.get(),
                                                                  exp.get(),
                                                                  batchcode.get())).grid(row=3,column=0,sticky=W)
    
    tree=Treeview(inventory)
    tree["columns"]=(0,1,2,3,4,5,6,7)
    tree.column("#0",width=0)
    tree.column(0,width=100)
    tree.column(1,width=100)
    tree.column(2,width=100)
    tree.column(3,width=100)
    tree.column(4,width=50)
    tree.column(5,width=50)
    tree.column(6,width=100)
    tree.column(7,width=130)
    tree.heading(0,text="Seriel number")
    tree.heading(1,text="Supplier")
    tree.heading(2,text="Manufacturer")
    tree.heading(3,text="Product")
    tree.heading(4,text="Qty.")
    tree.heading(5,text="Rate")
    tree.heading(6,text="Expiry")
    tree.heading(7,text="batchcode")
    tree.grid(row=4,column=0)
    vsb=Scrollbar(inventory,orient="vertical",command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.grid(row=4,column=1,sticky=NS)
    mydb.connect()
    cursor.execute("select * from stock order by Itemname asc, expiry desc")
    for i in cursor.fetchall():
        tree.insert('',"end",values=(i))
    mydb.close()
    inventory.mainloop()
    
def click_entry(mode,caller,entries,tree,serielno,manufacturer,supplier,itemname,qty,rate,expiry,batchcode):
    error=Frame(caller)
    error.grid(row=3,column=1,sticky=W,ipadx=60)
    if serielno=='':
        Label(error,text="Seriel number is necessary.",fg='red').grid(row=0,column=0,sticky=W)
    elif itemname=='':
        Label(error,text="Product name is necessary.",fg='red').grid(row=0,column=0,sticky=W)
    elif rate=='':
        Label(error,text="Rate is necessary",fg='red').grid(row=0,column=0,sticky=W)
    elif batchcode=='':
        Label(error,text="Batch code is necessary",fg='red').grid(row=0,column=0,sticky=W)
    else: 
        manufacturer='null' if manufacturer=='' else "'"+manufacturer+"'"
        supplier='null' if supplier=='' else "'"+supplier+"'"
        qty=0 if qty=='' else qty
        expiry='null' if expiry=='' else "'"+expiry+"'"
        mydb.connect()
        cursor.execute(f"insert into stock values('{serielno}',{supplier},{manufacturer},\
                                                  '{itemname}',{qty},{rate},{expiry},'{batchcode}')")
        mydb.commit()
        for i in entries:
            i.delete(0,100)
        cursor.execute("select * from stock order by Itemname asc, expiry desc")
        for i in tree.get_children():
            tree.delete(i)
        for i in cursor.fetchall():
            tree.insert('',"end",values=(i))
        mydb.close()
#%%
def employee(caller):
    caller.destroy()
    emp=Tk()
    fr1=Frame(emp)
    fr1.grid(row=0,column=0,columnspan=2)
    tree=Treeview(emp)
    Button(fr1,text="Add new employee",width=48,command=lambda: add_emp(emp,tree)).grid(row=0,column=0)
    Button(fr1,text="Update an employee",width=48).grid(row=0,column=1)
    Button(fr1,text="Remove an employee",width=48).grid(row=0,column=2)
    tree["columns"]=(0,1,2,3,4,5,6,7,8,9)
    tree.column("#0",width=0)
    tree.column(0,width=50)
    tree.column(1,width=140)
    tree.column(2,width=100)
    tree.column(3,width=80)
    tree.column(4,width=80)
    tree.column(5,width=70)
    tree.column(6,width=50)
    tree.column(7,width=100)
    tree.column(8,width=100)
    tree.column(9,width=110)
    tree.heading(0,text="E.id")
    tree.heading(1,text="Name")
    tree.heading(2,text="Username")
    tree.heading(3,text="Post")
    tree.heading(4,text="Mobile")
    tree.heading(5,text="Salary")
    tree.heading(6,text="Gender")
    tree.heading(7,text="Date of Birth")
    tree.heading(8,text="Initial password")
    tree.heading(9,text="Date employeed")
    tree.grid(row=1,column=0)
    vsb=Scrollbar(emp,orient="vertical",command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.grid(row=1,column=1,sticky=NS)
    mydb.connect()
    cursor.execute("select eid,name,username,post,mobile,sal,gender,dob,ipass,date_employed from staff")
    for i in cursor.fetchall():
            tree.insert('',"end",values=(i))
    mydb.close()
    emp.mainloop()
    
def add_emp(emp,tree):
    mydb.connect()
    cursor.execute("select max(eid),max(date_employed),max(ipass) from staff")
    op=cursor.fetchall()
    today=str(datetime.date.today())
    date_employed=today
    if cursor.rowcount==0:
        eid='E001'
        ipass='#'+today[2:4]+today[5:7]+today[8:]+'01#'
    else:
        maxeid=op[0][0] #The last eid in the table
        maxde=str(op[0][1]) #The last date_employed in the table
        maxpass=op[0][2] #The last ipass in the table
        eid="E"+str(int(maxeid[1:])+1)
        while len(eid)<4:
            eid=eid[0]+'0'+eid[1:]
        if maxde==today:
            ipassnum=str(int(maxpass[7:9])+1) 
            ipassnum='0'+ipassnum if len(ipassnum)==1 else ipassnum
        else:
            ipassnum='01'
        ipass='#'+today[2:4]+today[5:7]+today[8:]+ipassnum+'#'
    cursor.execute(f"insert into staff(eid,ipass,date_employed) values('{eid}','{ipass}','{date_employed}')")
    mydb.commit()
    cursor.execute("select eid,name,username,post,mobile,sal,gender,dob,ipass,date_employed from staff")
    for i in tree.get_children():
        tree.delete(i)
    for i in cursor.fetchall():
        tree.insert('',"end",values=(i))
    mydb.close()    
        
#%%        
LoginPage()