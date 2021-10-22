from tkinter import *
import tkinter.messagebox
from tkinter import ttk
import pymysql

con = pymysql.connect(host="localhost", user="root", password="bai0125..", db="student")
cur = con.cursor()
gui = Tk()
gui.title('学生成绩管理')
gui.iconbitmap(default='e8.ico')

v_name = StringVar()
v_sex = IntVar()
v_class = IntVar()
v_score = DoubleVar()
v_note = StringVar()
v_list = StringVar()

Label(gui, text='姓名:').grid(row=1, column=0)
cb = ttk.Combobox(gui, width=10, textvariable=v_name)
cb.grid(row=1, column=1, columnspan=2, sticky=W, padx=5, pady=15)
Label(gui, text='班级:').grid(row=1, column=3, sticky=W)
Entry(gui, width=5, textvariable=v_class).grid(row=1, column=4, padx=10, pady=15)
Label(gui, text='成绩:').grid(row=1, column=5, sticky=W)
Entry(gui, width=5, textvariable=v_score).grid(row=1, column=6, padx=10, pady=15)
Label(gui, text='性别:').grid(row=2, column=0, padx=20)
Radiobutton(gui, text='男', variable=v_sex, value=1).grid(row=2, column=1)
Radiobutton(gui, text='女', variable=v_sex, value=0).grid(row=2, column=2)
Label(gui, text='备注:').grid(row=2, column=3, sticky=W)
Entry(gui, textvariable=v_note).grid(row=2, column=4, columnspan=3, padx=10, pady=15)
tree = ttk.Treeview(gui, show="headings", height=8, columns=("姓名", "班级", "分数"), selectmode=tkinter.BROWSE)
tree.column("姓名", anchor="center", width=90)
tree.column("班级", anchor="center", width=90)
tree.column("分数", anchor="center", width=90)
tree.heading("姓名", text="Name")
tree.heading("班级", text="Class")
tree.heading("分数", text="Score")
tree.grid(row=3, column=0, rowspan=4, columnspan=5, sticky=W, padx=20, pady=15)


def que_student():
    if v_name.get() == '':
        cur.execute('select * from Person')
        tkinter.messagebox.showinfo('错误', '请选择姓名！')
    else:
        cur.execute('select * from Person where name=%s', (v_name.get()))
    row = cur.fetchall()
    if cur.rowcount == 1:
        qurygui(row)
    else:
        v_name.set('')
        v_sex.set(1)
        v_class.set(0)
        v_score.set(0.0)
        v_note.set('')


def init():
    cur.execute('select distinct(name) from person')
    roww = cur.fetchall()
    cb["values"] = roww
    cur.execute('select * from person')
    row = cur.fetchall()
    obj = tree.get_children()
    for o in obj:
        tree.delete(o)
    if cur.rowcount != 0:
        for i in range(cur.rowcount):
            tree.insert("", i, values=(row[i][0], str(row[i][2]), str(row[i][3])))


def ins_student():
    cur.execute('insert into Person values(%s,%s,%s,%s,%s)',
                (v_name.get(), v_sex.get(), v_class.get(), v_score.get(), v_note.get()))
    con.commit()
    tkinter.messagebox.showinfo('提示', v_name.get() + '的信息录入成功')
    v_name.set('')
    init()


def upt_student():
    cur.execute('update Person set sex=%s,class=%s,score=%s,note=%s where name=%s',
                (v_sex.get(), v_class.get(), v_score.get(), v_note.get(), v_name.get()))
    con.commit()
    tkinter.messagebox.showinfo('提示', v_name.get() + '的信息修改成功')
    v_name.set('')
    init()


def del_student():
    cur.execute('delete from Person where name=%s', (v_name.get()))
    con.commit()
    tkinter.messagebox.showinfo('提示', v_name.get() + '的信息删除成功')
    v_name.set('')
    init()


def qurygui(row):
    qgui = Tk()
    qgui.title('查询结果')
    if row[0][1] == 1:
        k = '男'
    else:
        k = '女'
    Label(qgui, text='姓名:').grid(row=1, column=0)
    Label(qgui, text=row[0][0]).grid(row=1, column=1, sticky=W, pady=10)
    Label(qgui, text='班级:').grid(row=1, column=2, sticky=W)
    Label(qgui, text=row[0][2]).grid(row=1, column=3, pady=10)
    Label(qgui, text='性别:').grid(row=1, column=4, sticky=W)
    Label(qgui, width=5, text=k).grid(row=1, column=5, padx=10, pady=10)
    Label(qgui, text='成绩:').grid(row=2, column=0)
    Label(qgui, width=5, text=row[0][3]).grid(row=2, column=1)
    Label(qgui, text='备注:').grid(row=2, column=2, sticky=W)
    Label(qgui, text=row[0][4]).grid(row=2, column=3, columnspan=3, padx=10, sticky=W)


Button(gui, text='录 入', width=10, command=ins_student).grid(row=3, column=5, columnspan=2, sticky=W, padx=5,
                                                            pady=5)
Button(gui, text='修 改', width=10, command=upt_student).grid(row=4, column=5, columnspan=2, sticky=W, padx=5, pady=5)
Button(gui, text='删 除', width=10, command=del_student).grid(row=5, column=5, columnspan=2, sticky=W, padx=5, pady=5)
Button(gui, text='查 询', width=10, command=que_student).grid(row=6, column=5, columnspan=2, sticky=W, padx=5, pady=5)
init()
mainloop()
