from tkinter import *
from tkinter import messagebox
import database
from database import Database
from datetime import date

db = Database('list.db')
date_today = str(date.today().strftime('%m/%d/%Y'))

# Methods
def generate_list():
    grocery_list.delete(0, END)
    table_headers = ('Store', 'Item', 'Price')
    grocery_list.insert(END, '| --' + table_headers[0] + '--  |  --' +
                        table_headers[1] + '--  |  --' + table_headers[2] + '--  |')
    # for row in db.fetch():
    #     grocery_list.insert(END, ' -' + row[1] + ' | ' + row[2] + ' | $' + row[3])
    for row in db.fetch():
        grocery_list.insert(END, row[0:])


def add_item():
    if store_text.get() == '' or item_text.get() == '' or price_text.get() == '':
        messagebox.showerror(
            'Fields Empty', 'You must complete all fields before adding an item.')
        return
    db.insert(store_text.get(), item_text.get(), price_text.get())
    grocery_list.delete(0, END)
    # May need to to .insert()
    clear_input()
    generate_list()


def update_item():
    db.update(chosen_item[0], store_text.get(),
              item_text.get(), price_text.get())
    clear_input()
    generate_list()


def remove_item():
    db.remove(chosen_item[0])
    clear_input()
    generate_list()


def print_list():
    db.export_list_to_csv()


def delete_list():
    msg_box = messagebox.askquestion('WARNING!', 'You are about to delete your entire list. Are you sure you would like to continue?')
    if msg_box == 'yes':
        db.drop_table()
        generate_list()
        messagebox.showinfo('List Deleted', 'The deed is done..')
    else:
        messagebox.showinfo('Returning...', 'Got it')


def exit_app():
    msg_box = messagebox.askquestion('Is this goodbye?', 'Are you sure you would like to exit the application?')
    if msg_box == 'yes':
        messagebox.showinfo('Leaving...', 'Goodbye, my friend.')
        db.__del__()
        app.destroy()
    else:
        messagebox.showinfo('Returning...', 'Good. I never liked goodbyes.')


def clear_input():
    store_text_box.delete(0, END)
    item_text_box.delete(0, END)
    price_text_box.delete(0, END)


def selection(event):
    try:
        global chosen_item
        index = grocery_list.curselection()[0]
        chosen_item = grocery_list.get(index)
        # print(chosen_item)
        # print(grocery_list.get(index))

        store_text_box.delete(0, END)
        store_text_box.insert(END, chosen_item[1])
        item_text_box.delete(0, END)
        item_text_box.insert(END, chosen_item[2])
        price_text_box.delete(0, END)
        price_text_box.insert(END, chosen_item[3])
    except IndexError:
        pass


app = Tk()
app.title('MascuList')
app.config(bg='steelBlue')
app.geometry('750x450')

# Greeting/Welcome Header
welcome = Label(app, text='~MascuList~', font=('bold', 20), bg='steelBlue')
welcome.grid(row=0, column=2, columnspan=4, pady=3)
welcome_msg = Label(app, text='  Shop like a man...', font=('italic', 10), bg='steelBlue')
welcome_msg.grid(row=1, column=2, columnspan=4, sticky=N)


# Labels and text boxes
# Store
store_text = StringVar()
store_label = Label(app, text='Store: ', font=('bold', 14), pady=10, bg='steelBlue')
store_label.grid(row=2, column=0, sticky=W)
store_text_box = Entry(app, textvariable=store_text)
store_text_box.grid(row=2, column=1)


# Item
item_text = StringVar()
item_label = Label(app, text='Item: ', font=('bold', 14), pady=10, bg='steelBlue')
item_label.grid(row=3, column=0, sticky=W)
item_text_box = Entry(app, textvariable=item_text)
item_text_box.grid(row=3, column=1)


# Price
price_text = StringVar()
price_label = Label(app, text='Price: ', font=('bold', 14), pady=10, bg='steelBlue')
price_label.grid(row=4, column=0, sticky=W)
price_text_box = Entry(app, textvariable=price_text)
price_text_box.grid(row=4, column=1)


# Date
date_label = Label(app, text='Date: ', font=('bold', 14), pady=10, bg='steelBlue')
date_label.grid(row=5, column=0, sticky=W)
date_text = Label(app, text=f'{date_today}', font=('italic', 12), bg='steelBlue')
date_text.grid(row=5, column=1)


# Grocery List
grocery_list = Listbox(app, height=8, width=75, bg='ghostWhite', border=0)
grocery_list.grid(row=2, column=2, columnspan=6,
                  rowspan=5, sticky=E+W+S+N, padx=5)
# Scrollbar
scrollbar = Scrollbar(app, orient=VERTICAL)
scrollbar.grid(row=2, column=8, rowspan=5, sticky=S+N)
# Set scroll in Grocery list
grocery_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=grocery_list.yview)
# Capture Selection
grocery_list.bind('<<ListboxSelect>>', selection)


# CRUD Buttons
# Add Item
add_btn = Button(app, text='Add Item', width=12, bg='ghostWhite', command=add_item)
add_btn.grid(row=7, column=2, pady=5)
# Update Item
update_btn = Button(app, text='Update Item', width=12, bg='ghostWhite', command=update_item)
update_btn.grid(row=7, column=3)
# Remove Item
remove_btn = Button(app, text='Remove Item', width=12, bg='ghostWhite', command=remove_item)
remove_btn.grid(row=7, column=4)
# Print List
print_btn = Button(app, text='Print List', width=12, bg='ghostWhite', command=print_list)
print_btn.grid(row=7, column=5)


# Delete List
delete_list_btn = Button(app, text='Delete List', width=12, bg='red', fg='white', command=delete_list)
delete_list_btn.place(relx = 0.75, rely = .9, anchor = CENTER)
# Exit
exit_btn = Button(app, text='Exit', width=12, bg='black', fg='white', command=exit_app)
exit_btn.place(relx = 0.25, rely = .9, anchor = CENTER)


generate_list()
app.mainloop()
