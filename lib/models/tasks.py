from models.__init__ import CONN, CURSOR
from models.family_members import Family_Member


class Task:
    all = {}
    def __init__(self, description, family_member_id):
        self.id = None
        self.description = description
        self.family_member_id = family_member_id
    #attribute properties
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
        
    #table methods

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
        # check if task exists before saving to avoid duplicates
        if any(task.description == self.description for task in Task.all.values()):
            return None
        # check if task exists in db before saving to avoid duplicates
        dupe = CURSOR.execute('''SELECT * FROM tasks WHERE description =?''', (self.description,)).fetchone()

        if dupe:
            return None

        CURSOR.execute('''INSERT INTO tasks (description, family_member_id) VALUES (?,?)''', (self.description, self.family_member_id))
        CONN.commit()
        self.id = CURSOR.lastrowid
        Task.all[self.id] = self

    @classmethod
    def build_task(cls, row):

        for task in cls.all.values():
            #check dict for task
            if task.id == row[0]:
                task.description = row[1]
                task.family_member_id = row[2]
                return task
                #create a new task if necessary
            task = cls(row[1], row[2])
            task.id = row[0]
            cls.all[task.id]=task

            return task
        
    @classmethod
    def get_all(cls):
        # fetch all rows from the tasks table and create list of instances
        rows = CURSOR.execute("SELECT * FROM tasks").fetchall()
        return [cls.build_task(row) for row in rows]
    
    def delete(self):
        # self destruct
        CURSOR.execute("DELETE FROM tasks WHERE id=?", (self.id,))
        CONN.commit()

        del Task.all[self.id]

    @classmethod
    def find_by_id(cls, id):
        task = CURSOR.execute("SELECT * FROM tasks WHERE id =?", [id]).fetchone()
        return cls.build_task(task) if task else None
    
    @classmethod
    def all_tasks_for_id(cls, foreign_key):
        tasks = CURSOR.execute("SELECT * FROM tasks WHERE family_member_id =?", [foreign_key]).fetchall()
        return [cls.build_task(task) for task in tasks]
    
    @classmethod
    def find_by_description(cls, description):
        tasks = CURSOR.execute("SELECT * FROM tasks WHERE description =?", [description]).fetchall()
        return [cls.build_task(task) for task in tasks]
    
    @classmethod
    def create(cls, description, foreign_key):
        new_task = cls(description, foreign_key)
        new_task.save()
        return new_task

    
    