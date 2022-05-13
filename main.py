# --------------------Imports--------------------
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import Calendar
from task import Task
import calendar
from db_service import DataBaseService

# --------------------Imports--------------------


# ---------------Tkinter configures--------------
screen = Tk()
screen.title("To-Do List")
screen.geometry("1000x800")
# ---------------Tkinter configures--------------


# ------------------Variables---------------------
current_datetime = datetime.now()
task_list = []
db = DataBaseService()
# ------------------Variables---------------------


# -------------------Widgets----------------------
l1 = Label(screen, text='To-Do List', font=('Arial', 20))
l2 = Label(screen, text='Enter task title', font=('Arial', 20))
task_entry = Entry(screen, width=18, font=('Arial', 20), )
task_box = Listbox(screen, height=12, width=50, selectmode="SINGLE", bd=4, font=('Arial', 15))
b1 = Button(screen, text='add task', width=20, font=('Arial', 17), command=lambda: add_task())
b2 = Button(screen, text='Delete', width=15, font=('Arial', 15), command=lambda: del_one())
b3 = Button(screen, text='Delete All', width=15, font=('Arial', 15), command=lambda: del_all())
b4 = Button(screen, text='Done', width=15, font=('Arial', 15), command=lambda: done())
cal = Calendar(screen, selectmode="day", font=('Arial', 15),
               year=current_datetime.year,
               month=current_datetime.month,
               day=current_datetime.day)
b5 = Button(screen, text='Sort', width=10, font=('Arial', 15), command=lambda: sort())
combo = ttk.Combobox(screen, values=['title', 'status', 'deadline'], font=('Arial', 15), width=10)
combo.current(0)
# -------------------Widgets----------------------
word_for_sort = StringVar()
word_for_sort.set(combo.get())
# -----------------Place Geometry-----------------
l1.place(x=450, y=10)
l2.place(x=200, y=130)
task_entry.place(x=150, y=180)
task_box.place(x=250, y=400)
b1.place(x=150, y=230)
b2.place(x=630, y=700)
b3.place(x=250, y=700)
b4.place(x=50, y=500)
cal.place(x=550, y=100)
b5.place(x=820, y=550)
combo.place(x=820, y=500)


# -----------------Place Geometry-----------------


# -------------------Functions--------------------
def parse_text(text):
    global date
    value = text.split(' | ')
    title = value[0]
    for element in value:
        if len(element) > 1:
            if element == title:
                continue
            date = element
            break
    return [title, date]


def add_task():
    word = task_entry.get()
    deadline = cal.selection_get()
    if len(word) == 0:
        messagebox.showwarning('Empty entry', 'Enter task name')
    else:
        item = Task(word, deadline, False)
        task_list.append(item)
        db.insert_value(word, deadline, status=False)
        task_entry.delete(0, "end")
        list_update()


def del_one():
    try:
        text = task_box.get(task_box.curselection())
        iter_parse_text(text, 'delete')
    except:
        messagebox.showwarning('Cannot delete', 'Not task item selected')


def iter_parse_text(text, arg):
    title = parse_text(text)[0]
    date_task = parse_text(text)[1]
    for el in task_list:
        if el.title == title and date_transform(el.deadline.day, el.deadline.month, el.deadline.year) \
                == date_task:
            if arg == "delete":
                task_list.remove(el)
                db.delete_one(title, date_task)
            elif arg == "done":
                el.status = True
                db.update_value(title, date_task, status=True)
        list_update()


def done():
    try:
        text = task_box.get(task_box.curselection())
        iter_parse_text(text, 'done')
    except:
        messagebox.showinfo('Cannot update', 'No task item selected')


def del_all():
    mb = messagebox.askyesno('Delete all', 'Are you sure')
    if mb:
        task_list.clear()
        db.delete_all()
        list_update()


def date_transform(day, month, year):
    return f"{day} {calendar.month_name[month]}, {year} "


def list_update():
    task_list.clear()
    for element in db.select_values(word_for_sort.get()):
        item = Task(element[0], element[1], element[2])
        task_list.append(item)
    clear_list()
    for i in task_list:
        date = i.deadline
        name = i.title
        st = i.status
        row = f"{name} | {date_transform(date.day, date.month, date.year)} | {st}"
        task_box.insert('end', row)


def clear_list():
    cal.calevent_remove()
    for task in task_list:
        task.get_color_day(current_datetime, cal)
    task_box.delete(0, 'end')


def sort():
    word_for_sort.set(combo.get())
    list_update()


list_update()
# -------------------Functions--------------------


screen.mainloop()
