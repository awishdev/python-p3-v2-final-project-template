from models.__init__ import CURSOR, CONN


class Family_Member:
    all = {}
    def __init__(self, name, age, title):
        self.id = None
        self.name = name
        self.age = age
        self.title = title

    # set attributes as properties
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self._name = value
        else:
            raise ValueError("Name must be a string.")
        
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        if isinstance(value, int) and 0 <= value <= 150:
            self._age = value
        else:
            raise ValueError("Age must be an integer between 0 and 150.")
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if isinstance(value, str):
            self._title = value
        else:
            raise ValueError("Title must be a string.")
        
    #table methods        
    @classmethod
    def create_table(cls):
        CURSOR.execute('''CREATE TABLE IF NOT EXISTS family_members (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            age INTEGER,
                            title TEXT
                        )''')
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS family_members")
        CONN.commit()

    def save(self):
        #check if member exists before saving to avoid duplicates
        if any(member.name == self.name for member in Family_Member.all.values()):
            return None
        # check if member exists in db before saving to avoid duplicates
        dupe = CURSOR.execute('''SELECT * FROM family_members WHERE name =?''', (self.name,)).fetchone()

        if dupe:
            
            self.id = dupe[0]
            Family_Member.all[self.id]=self
            
            
        
        
        CURSOR.execute('''INSERT INTO family_members (name, age, title) VALUES (?,?,?)''', (self.name, self.age, self.title))
        CONN.commit()
        self.id = CURSOR.lastrowid
        Family_Member.all[self.id] = self
        

    @classmethod
    def build_member(cls, row):
        # check dict for member
        for member in cls.all.values():
            if member.id == row[0]:
                member.name = row[1]
                member.age = row[2]
                member.title = row[3]
                return member
            #create a new member if necessary
            member = cls(row[1], row[2], row[3])
            member.id = row[0]
            cls.all[member.id]=member

            return member
    @classmethod
    def get_all(cls):

        rows = CURSOR.execute("SELECT * FROM family_members").fetchall()
        members = []
        # avoid Nones
        for row in rows:
            member = cls.build_member(row)
            if member:
                members.append(member)
        
        return members
                
    def delete(self):
        # import in method to avoid circular import
        from models.tasks import Task
        CURSOR.execute("DELETE FROM family_members WHERE id=?", (self.id,))
        CONN.commit()
        # iterate through tasks and delete tasks for deleted fam member
        for task in Task.all_tasks_for_id(self.id):
            task.delete()

        del Family_Member.all[self.id]

    @classmethod
    def find_by_id(cls, id):
        member = CURSOR.execute("SELECT * FROM family_members WHERE id = ?", [id]).fetchone()
        if member:
            return cls.build_member(member)
            
    @classmethod
    def update(cls, id, name, age, title):
        # update dict entry
        if cls.all[id]:
            cls.all[id].name = name
            cls.all[id].age = age
            cls.all[id].title = title
            # update db
            CURSOR.execute("UPDATE family_members SET name=?, age=?, title=? WHERE id=?", (name, age, title, id))
            CONN.commit()
        else:
            raise ValueError("Family member not found.")

    @classmethod
    def create(cls, name, age=0, title="baby"):
        member = cls(name, age, title)
        member.save()
        return member

