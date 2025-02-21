from models.__init__ import CONN, CURSOR
from models.family_members import Family_Member


class Task:
    all = {}
    def __init__(self, description, family_member_id):
        self.id = None
        self.description = description
        self.family_member_id = family_member_id
        self.save()

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        if isinstance(value, str):
            self._description = value
        else:
            raise ValueError("Description must be a string.")
        
    @property
    def family_member_id(self):
        return self._family_member_id
    
    @family_member_id.setter
    def family_member_id(self, value):
        if isinstance(value, int):
            self._family_member_id = value
        else:
            raise ValueError("Family member ID must be an integer.")

    @classmethod
    def create_table(cls):
        CURSOR.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY,
                            description TEXT,
                            family_member_id INTEGER,
                            FOREIGN KEY (family_member_id) REFERENCES family_members(id)
                        )''')
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS tasks")
        CONN.commit()

    def save(self):
        if any(task.description == self.description for task in Task.all.values()):
            return None
        
        CURSOR.execute('''INSERT INTO tasks (description, family_member_id) VALUES (?,?)''', (self.description, self.family_member_id))
        CONN.commit()
        self.id = CURSOR.lastrowid
        Task.all[self.id] = self

    @classmethod
    def instance_from_db(cls, row):
        for task in cls.all.values():
            if task.id == row[0]:
                task.description = row[1]
                task.family_member_id = row[2]
            else:
                task = cls(row[1], row[2])
                cls.all[task.id]=task

            return task
        
    @classmethod
    def get_all(cls):
        rows = CURSOR.execute("SELECT * FROM tasks").fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    def delete(self):
        CURSOR.execute("DELETE FROM tasks WHERE id=?", (self.id,))
        CONN.commit()

        del Task.all[self.id]

    @classmethod
    def find_by_id(cls, id):
        task = CURSOR.execute("SELECT * FROM tasks WHERE id =?", [id]).fetchone()
        return cls.instance_from_db(task) if task else None
    
    @classmethod
    def all_tasks_for_id(cls, id):
        tasks = CURSOR.execute("SELECT * FROM tasks WHERE family_member_id =?", [id]).fetchall()
        return [cls.instance_from_db(task) for task in tasks]
    
    