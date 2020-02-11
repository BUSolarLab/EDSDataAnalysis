from tkinter import *
from PIL import ImageTk, Image
import sqlite3


root = Tk()

# create table
'''
c.execute("""CREATE TABLE addresses (
    first_name text,
    last_name text,
    address text,
    city text,
    state text,
    zipcode integer
    )""")
'''

# make update function to save the changes
def update():
    # create a database or connect to one, create connection
    conn = sqlite3.connect('address_book.db')
    # create a cursor
    c = conn.cursor()
    record_id = select_box.get()
    c.execute("""UPDATE addresses SET
        first_name = :first,
        last_name =:last,
        address = :address,
        city = :city,
        state = :state,
        zipcode = :zipcode

        WHERE oid = :oid""",
        {
            'first': f_name_editor.get(),
            'last': l_name_editor.get(),
            'address': address_editor.get(),
            'city': city_editor.get(),
            'state': state_editor.get(),
            'zipcode': zipcode_editor.get(),
            'oid': record_id
        })
    # commit changes
    conn.commit()
    # close connection
    conn.close()
    # close the editor window
    editor.destroy()

# create function to update the record
def edit():
    global editor
    editor = Tk()
    editor.title("Update A Record")
    # create a database or connect to one, create connection
    conn = sqlite3.connect('address_book.db')
    # create a cursor
    c = conn.cursor()
    # get id boxes
    record_id = select_box.get()
    # query the database
    c.execute("SELECT * FROM addresses WHERE oid = " + record_id)
    records = c.fetchall()
    # create global variables for text box names
    global f_name_editor
    global l_name_editor
    global address_editor
    global city_editor
    global state_editor
    global zipcode_editor
    # create text boxes
    f_name_editor = Entry(editor, width=30)
    f_name_editor.grid(row=0, column=1, padx=20, pady=(10,0))
    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=1, column=1, padx=20)
    address_editor = Entry(editor, width=30)
    address_editor.grid(row=2, column=1, padx=20)
    city_editor = Entry(editor, width=30)
    city_editor.grid(row=3, column=1, padx=20)
    state_editor = Entry(editor, width=30)
    state_editor.grid(row=4, column=1, padx=20)
    zipcode_editor = Entry(editor, width=30)
    zipcode_editor.grid(row=5, column=1, padx=20)
    select_box_editor = Entry(editor, width=30)
    select_box_editor.grid(row=6, column=1)

    # create text box labels
    f_name_label = Label(editor, text="First Name")
    f_name_label.grid(row=0,column=0,pady=(10,0))
    l_name_label = Label(editor, text="Last Name")
    l_name_label.grid(row=1,column=0)
    address_label = Label(editor, text="Address")
    address_label.grid(row=2,column=0)
    city_label = Label(editor, text="City")
    city_label.grid(row=3,column=0)
    state_label = Label(editor, text="State")
    state_label.grid(row=4,column=0)
    zipcode_label = Label(editor, text="Zipcode")
    zipcode_label.grid(row=5,column=0)
    select_box_label = Label(editor, text="Select ID Number")
    select_box_label.grid(row=6, column=0)

    # loop through results
    for record in records:
        f_name_editor.insert(0, record[0])
        l_name_editor.insert(0, record[1])
        address_editor.insert(0, record[2])
        city_editor.insert(0, record[3])
        state_editor.insert(0, record[4])
        zipcode_editor.insert(0, record[5])

    # create an save button
    save_btn = Button(editor, text="Save Record", command = update)
    save_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

# function to delete a record
def delete():
    # create a database or connect to one, create connection
    conn = sqlite3.connect('address_book.db')
    # create a cursor
    c = conn.cursor()
    # delete a record
    c.execute("DELETE from addresses WHERE oid= " + select_box.get())
    # commit changes
    conn.commit()
    # close connection
    conn.close()

# submit function for database
def submit():
    # create a database or connect to one, create connection
    conn = sqlite3.connect('address_book.db')
    # create a cursor
    c = conn.cursor()
    # insert into table
    c.execute("INSERT INTO addresses VALUES (:f_name, :l_name, :address, :city, :state, :zipcode)",
            {
                'f_name': f_name.get(),
                'l_name': l_name.get(),
                'address': address.get(),
                'city': city.get(),
                'state': state.get(),
                'zipcode': zipcode.get()
            })
    # commit changes
    conn.commit()
    # close connection
    conn.close()
    #clear the text boxes
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)

# create query function
def query():
    # create a database or connect to one, create connection
    conn = sqlite3.connect('address_book.db')
    # create a cursor
    c = conn.cursor()
    # query the database
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()
    #print(records)
    # loop through results
    print_records=''
    for record in records:
        print_records += str(record[0]) + " " + str(record[1]) + " " + str(record[6]) + "\n"

    query_label = Label(root, text=print_records)
    query_label.grid(row=12, column=0, columnspan=2)
    # commit changes
    conn.commit()
    # close connection
    conn.close()

# add stuff to table, once already created
# create text boxes
f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20, pady=(10,0))
l_name = Entry(root, width=30)
l_name.grid(row=1, column=1, padx=20)
address = Entry(root, width=30)
address.grid(row=2, column=1, padx=20)
city = Entry(root, width=30)
city.grid(row=3, column=1, padx=20)
state = Entry(root, width=30)
state.grid(row=4, column=1, padx=20)
zipcode = Entry(root, width=30)
zipcode.grid(row=5, column=1, padx=20)
select_box = Entry(root, width=30)
select_box.grid(row=9, column=1)

# create text box labels
f_name_label = Label(root, text="First Name")
f_name_label.grid(row=0,column=0,pady=(10,0))
l_name_label = Label(root, text="Last Name")
l_name_label.grid(row=1,column=0)
address_label = Label(root, text="Address")
address_label.grid(row=2,column=0)
city_label = Label(root, text="City")
city_label.grid(row=3,column=0)
state_label = Label(root, text="State")
state_label.grid(row=4,column=0)
zipcode_label = Label(root, text="Zipcode")
zipcode_label.grid(row=5,column=0)
select_box_label = Label(root, text="Select ID Number")
select_box_label.grid(row=9, column=0)

# create submit button
submit_btn = Button(root, text="Add Record To Database", command=submit)
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# create a query button
query_btn = Button(root, text="Show Records", command = query)
query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

# create a delete button
delete_btn = Button(root, text="Delete Record", command = delete)
delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

# create an update button
edit_btn = Button(root, text="Edit Record", command = edit)
edit_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=145)


root.mainloop()

#NOTES
# going to use sqlite3, comes with python
# not as power as mysql or postgres
# gonna save db in the current directory
# if not connect to db, it will create
# need to create cursor, middle-man for database, courier
# when making changes to database, want to commit
# then close connection
# but the content of the database, is the table - a spreadsheet with columns and rows.
# new entry is a new row
# most databases have primary key for each record (each entry), its an id key for each entry
# c.fetchall() gets all records
# c.fetchone(), c.fetchmany(50)
# records shown as a list of rows, and each row is a tuple