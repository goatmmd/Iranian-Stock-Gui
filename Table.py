from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import sqlite3




# =========================================convert=============================================


# =========================================database===========================================
def init():
    conn = sqlite3.connect('calcTab.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS bbs(
                darai text,
                naghd int,
                ghardesh int,
                meghias int,
                tabdil int,
                tose int,
                shomare PRIMARY KEY)
                ''')
    conn.commit()
    conn.close()


init()




# ============================================Tree============================================
global icon
root = Tk()
root.title('Table')
root.configure(bg="silver")
root.resizable(0,0)
styl = ttk.Style()

styl.theme_use('clam')
styl.configure("Treeview",background="silver")
styl.map('Treeview',
    background=[('selected','#455264')])
styl.configure("Treeview", fieldbackground="#FAFCFF")    

tree_frame = Frame(root)
tree_frame.pack(pady=10)

tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

tree = ttk.Treeview(tree_frame, column=("c1", "c2", "c3","c4","c5","c6","c7"), show='headings',yscrollcommand=tree_scroll.set)
tree.pack()


tree_scroll.configure(command=tree.yview)


tree.column("#1", anchor=CENTER, width=80)
tree.column("#2", anchor=CENTER, width=180)
tree.column("#3", anchor=CENTER, width=180)
tree.column("#4", anchor=CENTER, width=180)
tree.column("#5", anchor=CENTER, width=180)
tree.column("#6", anchor=CENTER, width=180)
tree.column("#7", anchor=CENTER, width=80)

tree.heading("#1", text="نوع دارایی")
tree.heading("#2", text=u"نقدشوندگی")
tree.heading("#3", text="گردش پذیری")
tree.heading("#4", text="مقیاس پذیری")
tree.heading("#5", text="تبدیل پذیری")
tree.heading("#6", text="توسعه پذیری")
tree.heading("#7", text="شماره ")




tree.tag_configure('evenrow', background='#9FA3AA')
tree.tag_configure('oddrow', background='gray')

# =========================================Frame=======================================
my_frame1 = ttk.Labelframe(root)
my_frame1.pack(side=LEFT, pady=20, fill=Y)

my_frame2 = ttk.Labelframe(root)
my_frame2.pack(padx=15 ,side=RIGHT,)
# ========================================Label========================================
darai = Label(my_frame1, text="نوع دارایی")
darai.grid(row=0, column=0)

naghd = Label(my_frame1, text="نقدشوندگی")
naghd.grid(row=0, column=1)

ghardesh = Label(my_frame1, text="گردش پذیری")
ghardesh.grid(row=0, column=2)

meghias = Label(my_frame1, text="مقیاس پذیری")
meghias.grid(row=2, column=0)

tabdil = Label(my_frame1, text="تبدیل پذیری")
tabdil.grid(row=2, column=1)


shomare = Label(my_frame1, text="شماره")
shomare.grid(row=2, column=3)

warn = Label(my_frame1, text="لطفا چیزی درشماره وارد نکنید")
warn.grid(row=0, column=3)


tose = Label(my_frame1, text="نمره ی توسعه پذیری ")
tose.grid(row=2, column=2)

# ===========================================Entry=======================================

darai_box = Entry(my_frame1, bd=3)
darai_box.grid(row=1, column=0)

naghd_box = Entry(my_frame1, bd=3)
naghd_box.grid(row=1, column=1)

ghardesh_box = Entry(my_frame1, bd=3)
ghardesh_box.grid(row=1, column=2)

meghias_box = Entry(my_frame1, bd=3)
meghias_box.grid(row=3, column=0)

tabdil_box = Entry(my_frame1, bd=3)
tabdil_box.grid(row=3, column=1)

shomare_box = Entry(my_frame1, bd=3)
shomare_box.grid(row=3, column=3)

tose_box = Entry(my_frame1, bd=3)
tose_box.grid(row=3, column=2)

# =========================================func============================================



def selected_record(e):
    clear_enteries()


    selected = tree.focus()

    values = tree.item(selected, 'values')

    darai_box.insert(0 ,values[0])
    naghd_box.insert(0 ,values[1])
    ghardesh_box.insert(0 ,values[2])
    meghias_box.insert(0 ,values[3])
    tabdil_box.insert(0 ,values[4])
    tose_box.insert(0, values[5])
    shomare_box.insert(0, values[6])






def add_record1():
    conn = sqlite3.connect('calcTab.db')
    
    cur = conn.cursor()
    
    cur.execute("INSERT INTO bbs VALUES(?,?,?,?,?,?,NULL)",(darai_box.get(), naghd_box.get(), ghardesh_box.get(), meghias_box.get(), tabdil_box.get(), tose_box.get()))

    conn.commit()
    
    conn.close()

    clear_enteries()

    tree.delete(*tree.get_children())

    query_database()
    



def removall_record():
    response = messagebox.askyesno('WARNING','آیا میخواهید همه ی اطلاعات خود را پاک کنید ؟')
    if response == 1:
        for record in tree.get_children():
            tree.delete(record)
        
        conn = sqlite3.connect('calcTab.db')
        
        cur = conn.cursor()

        cur.execute("DROP TABLE bbs")

        conn.commit()
        
        conn.close()

        clear_enteries()
        
        init()
    
    else:
        pass
    



def removeone_record():
    try:
        x = tree.selection()[0]
        tree.delete(x)

        conn = sqlite3.connect('calcTab.db')
        cur = conn.cursor()

        cur.execute('DELETE FROM bbs WHERE oid='+ shomare_box.get())

        conn.commit()
        
        conn.close()

        clear_enteries()

    except:
        messagebox.showerror('Error','!لطفا یک ردیف را انتخاب کنید')



def updates_record():
    
    conn = sqlite3.connect('calcTab.db')
    cur = conn.cursor()
    selected = tree.focus()
    tree.item(selected, text="", values=(darai_box.get(), naghd_box.get(), ghardesh_box.get(), meghias_box.get(), tabdil_box.get(), tose_box.get(), shomare_box.get()))
    
    cur.execute('''UPDATE bbs SET
        darai = :darai,
        naghd = :naghd,
        ghardesh = :ghardesh,
        meghias = :meghias,
        tabdil = :tabdil,
        tose = :tose

        WHERE oid = :shomare''',
        
        {
            'darai' : darai_box.get(),
            'naghd': naghd_box.get(),
            'ghardesh' : ghardesh_box.get(),
            'meghias' : meghias_box.get(),
            'tabdil' : tabdil_box.get(),
            'tose' : tose_box.get(),
            'shomare' : shomare_box.get()
        })


    conn.commit()
    conn.close()

    clear_enteries()





def clear_enteries():
    darai_box.delete(0, END)
    naghd_box.delete(0, END)
    ghardesh_box.delete(0, END)
    meghias_box.delete(0, END)
    tabdil_box.delete(0, END)
    tose_box.delete(0, END)
    shomare_box.delete(0 ,END)



def hesab():
    try:
        s1 = int(naghd_box.get())
        s2 = int(ghardesh_box.get())
        s3 = int(meghias_box.get())
        s4 = int(tabdil_box.get())
        s5 = int(tose_box.get())
        resault = s1+s2+s3+s4
        result = s5*(s1+s2+s3+s4)
        respowns = messagebox.showinfo('Warning',f'توسعه پذیری : {resault} \n نمره ی کلی : {result}')
        respowns
    except:
        messagebox.showerror('Error','!لطفا یک ردیف را انتخاب کنید')
def avarege():
    conn = sqlite3.connect('calcTab.db')
    cur = conn.cursor()


    cur.execute("SELECT avg(round(naghd)),round((ghardesh)),round((meghias)),round((tabdil)) FROM bbs")
    result = cur.fetchone()
    root1 = Tk()
    root1.geometry('300x200')
    root1.title('!میانگین ')
    my_frame3 = LabelFrame(root1,width=15,text="میانگین")
    my_frame3.pack()
    Label15 = Label(my_frame3,text=f"نقد شوندگی : {result[0]} \n گردش پذیری : {result[1]} \n مقیاس پذیری : {result[2]} \n تبدیل پذیری : {result[3]}",font=('Helvetica',20))
    Label15.grid(sticky=W)
    root1.mainloop()
  
    
    conn.commit()
    conn.close()


# ============================================buttons==================================================
add_record = Button(my_frame2, text="اضافه کردن اطلاعات ",command=add_record1,bd=4)
add_record.grid(row=0,column=0,sticky=S)

remove_all_record = Button(my_frame2, text="حذف همه ی لیست ها", command=removall_record, width=15,bd=4)
remove_all_record.grid(row=0,column=1)

remove_one_record = Button(my_frame2, text="حذف", command=removeone_record,width=12,height=0,bd=4)
remove_one_record.grid(row=0,column=2)



avarege_record = Button(my_frame2, text="میانگین", command=avarege, width=15,bd=4)
avarege_record.grid(row=3, column=0,sticky=E) 



update_record = Button(my_frame2, text="آپدیت کردن", command=updates_record, width=15,bd=4)
update_record.grid(row=3, column=1,sticky=E)


calculate_record = Button(my_frame2, text="توسعه پذیری", command=hesab, width=12,bd=4)
calculate_record.grid(row=3, column=2)


# ==============================================DATABASE==============================================
num_of_add = 0
def query_database():
    conn = sqlite3.connect('calcTab.db')
    cur = conn.cursor()
   
    cur.execute("SELECT rowid, * FROM bbs")
    records = cur.fetchall()
    global num_of_add
    for record in records:
        if num_of_add %2 == 0:
            tree.insert(parent='', index='end', iid=num_of_add, text="", values=(
                record[1], record[2], record[3], record[4], record[5],record[6], record[0]), tags='evenrow')
        else:
            tree.insert(parent='', index='end', iid=num_of_add, text="", values=(
                record[1], record[2], record[3], record[4], record[5],record[6], record[0]), tags='oddrow')
        num_of_add +=1


    conn.close()










tree.bind("<ButtonRelease-1>", selected_record)

query_database()

root.mainloop()
 
