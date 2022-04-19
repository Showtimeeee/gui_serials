import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import sqlite3








class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # главное окно
    def init_main(self):
        toolbar = tk.Frame(bg='#5b92e5', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # кнопка добовления
        self.add_img = tk.PhotoImage(file='img/plus (1).png')
        btn_open_dialog = tk.Button(toolbar, text='Добавить\n запись', command=self.open_dialog, bg='#4989db', bd=10,
                                    padx=20, compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        # кнопка редактирования
        self.update_img = tk.PhotoImage(file='img/edit (1).png')
        btn_edit_dialog = tk.Button(toolbar, text='Изменить\n запись', bg='#4989db', bd=10, padx=20, image=self.update_img,
                                     compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        # кнопка обновить
        self.refresh_img = tk.PhotoImage(file='img/refresh-button.png')
        btn_refresh = tk.Button(toolbar, text='Обновить\n список', bg='#4989db', bd=10, padx=20, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # Кнопка поиска
        self.search_img = tk.PhotoImage(file='img/search_btn.png')
        btn_search = tk.Button(toolbar, text='Поиск\nзаписи', bg='#4989db', bd=10, padx=20, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)


        # кнопка удаления
        self.delete_img = tk.PhotoImage(file='img/del_button.png')
        btn_delete = tk.Button(toolbar, text='Удалить\n запись', bg='#4989db', bd=10, padx=20, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # колонки в окне(размер, расположения)
        self.tree = ttk.Treeview(self, column=('ID', 'description', 'Surname', 'Year', 'Kinopoisk', 'Score'),
                                 height=80, show='headings')

        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('description', width=100, anchor=tk.CENTER)
        self.tree.column('Surname', width=80, anchor=tk.CENTER)
        self.tree.column('Year', width=80, anchor=tk.CENTER)
        self.tree.column('Kinopoisk', width=80, anchor=tk.CENTER)
        self.tree.column('Score', width=80, anchor=tk.CENTER)
        # названия колонки в окне, названия
        self.tree.heading('ID', text='ID')
        self.tree.heading('description', text='Название')
        self.tree.heading('Surname', text='Жанр')
        self.tree.heading('Year', text='Год')
        self.tree.heading('Kinopoisk', text='Kinopoisk')
        self.tree.heading('Score', text='Оценка')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def records(self, description, Surname, Year, Kinopoisk, Score):
        self.db.insert_data(description, Surname, Year, Kinopoisk, Score)
        self.view_records()

    # редактирование данных SQL, указываем ID (выделяем строку где нужно изменить данные)
    def update_record(self, description, Surname, Year, Kinopoisk, Score):
        self.db.c.execute('''UPDATE  serials SET description=?, Surname=?, Year=?,
        Kinopoisk=?, Score=? WHERE ID=? ''', (description, Surname, Year,
                                              Kinopoisk, Score, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()


    def view_records(self):
        self.db.c.execute('''SELECT * FROM serials''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    # функция удаление записи SQL
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM serials WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # формирование SQL запроса #
    def search_records(self, description):
        description = ('%' + description + '%',)
        self.db.c.execute('''SELECT * FROM serials WHERE score LIKE ?''', description)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]  # fetchall возвращает кортедж поиска




# вызывает окно добавления
    def open_dialog(self):
        Child()

# вызывает окно редактирования
    def open_update_dialog(self):
        Update()

# вызывает поиск
    def open_search_dialog(self):
        Search()

    # окно добавления
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app


    def init_child(self):
        self.title('Добавить сериал')
        self.geometry('600x220+400+300')
        self.resizable(False, False)
        # таблица
        label_description = ttk.Label(self, text='Название')
        label_description.place(x=50, y=50)
        label_surname = ttk.Label(self, text='Жанр')
        label_surname.place(x=50, y=80)
        label_year = ttk.Label(self, text='Год')
        label_year.place(x=50, y=110)
        label_kinopoisk = ttk.Label(self, text='Kinopoisk')
        label_kinopoisk.place(x=50, y=140)
        label_score = ttk.Label(self, text='Оценка')
        label_score.place(x=50, y=170)



        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=50)

        self.entry_surname = ttk.Entry(self)
        self.entry_surname.place(x=200, y=80)

        ##### combobox Score
        self.combobox = ttk.Combobox(self, values=[u'Комедия', u'Фантастика', u'Боевик', u'Драма', u'Приключения',
                                                   u'Ужасы', u'Мульт'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

        self.entry_year = ttk.Entry(self)
        self.entry_year.place(x=200, y=110)

        self.entry_kinopoisk = ttk.Entry(self)
        self.entry_kinopoisk.place(x=200, y=140)

        self.entry_score = ttk.Entry(self)
        self.entry_score.place(x=200, y=170)

        btn_cancel = ttk.Button(self, text='Выход', command=self.destroy)
        btn_cancel.place(x=500, y=190)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=500, y=160)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_description.get(),
                                                                       #self.entry_surname.get(),
                                                                       self.combobox.get(),
                                                                       self.entry_year.get(),
                                                                       self.entry_kinopoisk.get(),
                                                                       self.entry_score.get()))

        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=500, y=160)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_description.get(),
                                                                          self.combobox.get(),
                                                                          self.entry_year.get(),
                                                                          self.entry_kinopoisk.get(),
                                                                          self.entry_score.get()))
        self.btn_ok.destroy()

    # при редактировании показывает старые значения
    def default_data(self):
        self.db.c.execute('''SELECT * FROM serials WHERE id=?''', (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_description.insert(0, row[1])
        self.entry_surname.insert(0, row[2])
        self.entry_year.insert(0, row[3])
        self.entry_kinopoisk.insert(0, row[4])
        self.entry_score.insert(0, row[5])

# Поиск
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Введите оценку')
        self.geometry('300x100+400+300')
        self.resizable(False, False)


        # поле ввода поиска
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=80, y=20)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=180, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=80, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

# Конструктор класса, создание базы данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('serials.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS serials (id integer primary key, description text, surname text, year integer, kinopoisk real, score text)''')
        self.conn.commit()

    def insert_data(self, description, surname, year, kinopoisk, score):
        self.c.execute('''INSERT INTO serials(description, surname, year, kinopoisk, score) VALUES (?, ?, ?, ?, ?)''',
                       (description, surname, year, kinopoisk, score))
        self.conn.commit()








if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Мои Сериалы')
    root.iconbitmap('img/aktion.ico')
    root.geometry('650x550+300+200')
    root.resizable(False, False)
    root.mainloop()