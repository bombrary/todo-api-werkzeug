import sqlite3


class TodoNotFound(Exception):
    pass


class Todo:
    TODOS = []
    NEXT_ID = 0
    DB_PATH = 'db.sqlite3'

    def __init__(self, content: str, todo_id=None):
        self.id = todo_id
        self.content = content

    def insert(self):
        with Todo.get_db() as con:
            con.execute('insert into Todo(content) values (?)', (self.content,))
            cur = con.cursor()
            row = cur.execute('select * from Todo where id=last_insert_rowid()').fetchone()
            self.id = row['id']
        return self.id

    def update(self):
        if self.id is None:
            raise TodoNotFound
        with Todo.get_db() as con:
            con.execute('update Todo set content=? where id=?', (self.content, self.id))

    def delete(self):
        if self.id is None:
            raise TodoNotFound
        with Todo.get_db() as con:
            con.execute('delete from Todo where id=?', (self.id,))

    @classmethod
    def get_all(cls):
        with Todo.get_db() as con:
            cur = con.cursor()
            rows = cur.execute('select * from todo').fetchall()
        return [Todo(row['content'], row['id']) for row in rows]

    @classmethod
    def get(cls, todo_id: int):
        with Todo.get_db() as con:
            cur = con.cursor()
            row = cur.execute('select * from todo where id=?', (todo_id,)).fetchone()
            if not row:
                raise TodoNotFound
        return Todo(row['content'], row['id'])

    @classmethod
    def get_db(cls):
        con = sqlite3.connect(Todo.DB_PATH)
        con.row_factory = sqlite3.Row
        return con

    @classmethod
    def init_table(cls):
        with Todo.get_db() as con:
            con.execute('drop table if exists Todo')
            con.execute('''create table Todo(
                              id integer primary key autoincrement,
                              content text not null
                           )''')
            con.commit()
