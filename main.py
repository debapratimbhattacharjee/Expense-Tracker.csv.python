from tkinter import *
from tkinter import ttk
import datetime as dt
from mydb import *
from tkinter import messagebox

# object for database
data = Database(db='test.db')

# global variables
count = 0
selected_rowid = 0

# functions
def saveRecord():
    global data
    data.insertRecord(item_name=item_name.get(), item_price=item_amt.get(), purchase_date=transaction_date.get())

def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')

def clearEntries():
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    transaction_date.delete(0, 'end')

def fetch_records():
    f = data.fetchRecord('select rowid, * from expense_record')
    global count
    for rec in f:
        tv.insert(parent='', index='0', iid=count, values=(rec[0], rec[1], rec[2], rec[3]))
        count += 1
    tv.after(400, refreshData)

def select_record(event):
    global selected_rowid
    selected = tv.focus()
    val = tv.item(selected, 'values')
    try:
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
    except Exception as ep:
        pass

def update_record():
    global selected_rowid
    selected = tv.focus()  # Update record
    try:
        data.updateRecord(namevar.get(), amtvar.get(), dopvar.get(), selected_rowid)
        tv.item(selected, text="", values=(namevar.get(), amtvar.get(), dopvar.get()))
    except Exception as ep:
        messagebox.showerror('Error', ep)
    
    # Clear entry boxes
    item_name.delete(0, END)
    item_amt.delete(0, END)
    transaction_date.delete(0, END)
    tv.after(400, refreshData)

def totalBalance():
    f = data.fetchRecord(query="Select sum(item_price) from expense_record")
    for i in f:
        for j in i:
            messagebox.showinfo('Current Balance: ', f"Total Expense: {j} \nBalance Remaining: {5000 - j}")

def refreshData():
    for item in tv.get_children():
        tv.delete(item)
    fetch_records()

def deleteRow():
    global selected_rowid
    data.removeRecord(selected_rowid)
    refreshData()

# create tkinter object
ws = Tk()
ws.title('Daily Expenses')
ws.geometry('900x600')  # Adjust window size

# variables
f = ('Times new roman', 14)
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()

# Frame for input fields
f1 = Frame(ws, padx=10, pady=10, bg='#2B2B2B')  # Dark background
f1.pack(expand=True, fill=BOTH)

# Input Labels
Label(f1, text='ITEM NAME', font=f, bg='#2B2B2B', fg='#FFFFFF').grid(row=0, column=0, sticky=W)
Label(f1, text='ITEM PRICE', font=f, bg='#2B2B2B', fg='#FFFFFF').grid(row=1, column=0, sticky=W)
Label(f1, text='PURCHASE DATE', font=f, bg='#2B2B2B', fg='#FFFFFF').grid(row=2, column=0, sticky=W)

# Entry widgets
item_name = Entry(f1, font=f, textvariable=namevar, bg='#333333', fg='#FFFFFF', relief='flat')
item_amt = Entry(f1, font=f, textvariable=amtvar, bg='#333333', fg='#FFFFFF', relief='flat')
transaction_date = Entry(f1, font=f, textvariable=dopvar, bg='#333333', fg='#FFFFFF', relief='flat')

# Place entry widgets
item_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_amt.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))

# Action buttons with modern color scheme
btn_style = {'bg': '#007BFF', 'fg': 'white', 'font': f, 'relief': 'flat'}

cur_date = Button(f1, text='Current Date', command=setDate, **btn_style)
submit_btn = Button(f1, text='Save Record', command=saveRecord, **btn_style)
clr_btn = Button(f1, text='Clear Entry', command=clearEntries, **btn_style)
quit_btn = Button(f1, text='Exit', command=lambda: ws.destroy(), bg='#DC3545', fg='white', font=f, relief='flat')
total_bal = Button(f1, text='Total Balance', command=totalBalance, **btn_style)
update_btn = Button(f1, text='Update', command=update_record, bg='#FFC107', fg='black', font=f, relief='flat')
del_btn = Button(f1, text='Delete', command=deleteRow, bg='#DC3545', fg='white', font=f, relief='flat')

# Grid placement of buttons
cur_date.grid(row=3, column=1, sticky=EW, padx=(10, 0))
submit_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0))
clr_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
quit_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
total_bal.grid(row=0, column=3, sticky=EW, padx=(10, 0))
update_btn.grid(row=1, column=3, sticky=EW, padx=(10, 0))
del_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0))

# Frame for Treeview widget
f2 = Frame(ws)
f2.pack()

# Treeview widget
tv = ttk.Treeview(f2, columns=(1, 2, 3, 4), show='headings', height=8)
tv.pack(side="left")

# Treeview column configuration
tv.column(1, anchor=CENTER, stretch=NO, width=70)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.heading(1, text="Serial no")
tv.heading(2, text="Item Name")
tv.heading(3, text="Item Price")
tv.heading(4, text="Purchase Date")

# Binding treeview selection
tv.bind("<ButtonRelease-1>", select_record)

# Style for Treeview
style = ttk.Style()
style.configure("Treeview.Heading", font=('Helvetica', 12, 'bold'))
style.configure("Treeview", background="#333333", foreground="white", rowheight=25, fieldbackground="#333333")
style.map("Treeview", background=[('selected', '#007BFF')], foreground=[('selected', 'white')])

# Scrollbar
scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)

# Fetch records on startup
fetch_records()

# Infinite loop to run the app
ws.mainloop()
