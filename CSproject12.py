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
    Button(fr1,text="Billing",width=25,command=lambda: billing(mnmnu)).grid(row=0,column=0)
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
    Radiobutton(gen,text="Prefer not to specify",variable=gender,value="null").grid(row=0,column=0,columnspan=2,sticky=W)
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
    options=Frame(emp)
    options.grid(row=2,column=0,sticky=W)
    tree=Treeview(emp)
    Button(fr1,text="Add new employee",width=48,command=lambda: add_emp(tree,options)).grid(row=0,column=0)
    Button(fr1,text="Update an employee",width=48,command=lambda: update_employee(tree,options)).grid(row=0,column=1)
    Button(fr1,text="Remove an employee",width=48, command=lambda: remove(tree,options)).grid(row=0,column=2)
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
    
def add_emp(tree,fr1):
    for widget in fr1.winfo_children():
        widget.destroy()
    post,sal=StringVar(),StringVar()
    Label(fr1,text="Add post: ").grid(row=0,column=0)
    Entry(fr1,textvariable=post).grid(row=0,column=1)
    Label(fr1,text="Add salary: ").grid(row=0,column=2)
    Entry(fr1,textvariable=sal).grid(row=0,column=4)
    Button(fr1,text="ADD",command=lambda: click_add_emp(tree,post.get(),sal.get())).grid(row=0,column=5)

def click_add_emp(tree,post,sal):
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
    post='null' if post=='' else "'"+post+"'"
    sal='null' if sal=='' else sal
    cursor.execute(f"insert into staff(eid,ipass,date_employed,post,sal) values('{eid}','{ipass}','{date_employed}',{post},{sal})")
    mydb.commit()
    cursor.execute("select eid,name,username,post,mobile,sal,gender,dob,ipass,date_employed from staff")
    for i in tree.get_children():
        tree.delete(i)
    for i in cursor.fetchall():
        tree.insert('',"end",values=(i))
    mydb.close()    
    
def remove(tree,fr1):
    for widget in fr1.winfo_children():
        widget.destroy()
    Label(fr1,text="Enter ID of employee to remove: ").grid(row=0,column=0)
    eid=StringVar()
    Entry(fr1,textvariable=eid).grid(row=0,column=1)
    error=Label(fr1,text="Please enter a valid ID.")
    Button(fr1,text="REMOVE",command=lambda: click_remove(tree,eid.get(),error)).grid(row=0,column=2)
    
def click_remove(tree,eid,error):
    mydb.connect()
    cursor.execute(f"delete from staff where eid='{eid}'")
    mydb.commit()
    if cursor.rowcount==0:
        error.grid(row=0,column=4)
    else:
        error.grid_forget()
        cursor.execute("select eid,name,username,post,mobile,sal,gender,dob,ipass,date_employed from staff")
        for i in tree.get_children():
            tree.delete(i)
        for i in cursor.fetchall():
            tree.insert('',"end",values=(i))
    mydb.close()
    
def update_employee(tree,fr1):
    for widget in fr1.winfo_children():
        widget.destroy()
    eid,new_post,new_sal=StringVar(),StringVar(),StringVar()
    error=Label(fr1,text="Enter a valid ID.")
    Label(fr1,text="Add Employee ID: ").grid(row=0,column=0)
    Entry(fr1,textvariable=eid).grid(row=0,column=1)
    Label(fr1,text="Add new post: ").grid(row=0,column=2)
    Entry(fr1,textvariable=new_post).grid(row=0,column=3)
    Label(fr1,text="Add new salary: ").grid(row=0,column=4)
    Entry(fr1,textvariable=new_sal).grid(row=0,column=5)
    Button(fr1,text="UPDATE",command=lambda: click_upd_emp(tree,error,eid.get(),new_post.get(),new_sal.get())).grid(row=0,column=6)

def click_upd_emp(tree,error,eid,new_post,new_sal):
    mydb.connect()
    cursor.execute(f"select post,sal from staff where eid='{eid}'")
    op=list(cursor.fetchall()[0])
    if cursor.rowcount==0:
        error.grid(row=0,column=7)
    else:
        for i in range(2):
            if op[i]==None:
                op[i]='null'
            elif i==0:
                op[i]=f"'{op[i]}'"
                
        error.grid_forget()
        new_post=op[0] if new_post=='' else "'"+new_post+"'"
        new_sal=op[1] if new_sal=='' else new_sal
        cursor.execute(f"update staff set post={new_post},sal={new_sal} where eid='{eid}'")
        mydb.commit()
        cursor.execute("select eid,name,username,post,mobile,sal,gender,dob,ipass,date_employed from staff")
        for i in tree.get_children():
            tree.delete(i)
        for i in cursor.fetchall():
            tree.insert('',"end",values=(i))
        mydb.close()
#%%
def billing():
    #caller.destroy()
    billpage=Tk()
    billpage.title("Billing")
    customer=Frame(billpage)
    customer.grid(row=1,column=0,sticky=W)
    Label(billpage,text="Customer details:\n").grid(row=0,column=0,sticky=W)
    Label(customer,text="Name: ").grid(row=0,column=0,sticky=W)
    Label(customer,text="Phone Number: ").grid(row=1,column=0,sticky=W)
    Label(customer,text="Gender ").grid(row=2,column=0,sticky=NW)
    Label(customer,text="  Date of Birth: ").grid(row=1,column=2,sticky=W)
    name1,ph1,gender,dob1=StringVar(),StringVar(),StringVar(),StringVar()
    Entry(customer, textvariable=name1,width=40).grid(row=0,column=1,sticky=W,columnspan=3)
    Entry(customer, textvariable=ph1,width=20).grid(row=1,column=1,sticky=W)
    Entry(customer, textvariable=dob1,width=20).grid(row=1,column=3,sticky=W)
    gen=Frame(customer)
    gen.grid(row=2,column=1,sticky=W,columnspan=2)  
    Radiobutton(gen,text="Prefer not to specify",variable=gender,value="null").grid(row=0,column=0,columnspan=2,sticky=W)
    Radiobutton(gen,text="Male",variable=gender,value="'M'").grid(row=1,column=0,sticky=W)
    Radiobutton(gen,text="Female",variable=gender,value="'F'").grid(row=1,column=1,sticky=W)
    Radiobutton(gen,text="Others",variable=gender,value="'O'").grid(row=1,column=2,sticky=W)
    #Button(customer, text="Proceed",command=push).grid(row=4,column=0,sticky=W)
    Label(billpage,text="Invoice:\n").grid(row=2,column=0,sticky=W)
    Bill=Frame(billpage)
    Bill.grid(row=3,column=0,sticky=W)
    Label(Bill, text="Batch Code: ").grid(row=0,column=0,sticky=W)
    Label(Bill, text="    Item Name: ").grid(row=0,column=2,sticky=W)
    Label(Bill, text="Quantity:").grid(row=1,column=0,sticky=W)
    batch,iname,qty=StringVar(),StringVar(),StringVar()
    Entry(Bill,textvariable=batch).grid(row=0,column=1)
    Entry(Bill,textvariable=iname,width=30).grid(row=0,column=3)
    Entry(Bill,textvariable=qty,width=10).grid(row=1,column=1,sticky=W)
    
    billpage.mainloop()
    
def push(name,mob,gender):
    mydb.connect()
    name=name1.get()
    phone=ph1.get()
    gender=g1.get()
    DOB=dob1.get()
    print(gender)
    qs="insert into customer values('{}','{}','{}','{}')".format(phone,name,gender,DOB)
    cursor.execute(qs)
    mydb.commit()
    mydb.close()
    
billing()
#%%        
LoginPage()