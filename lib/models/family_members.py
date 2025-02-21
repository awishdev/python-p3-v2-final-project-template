from models.__init__ import CURSOR, CONN

class Family_Member:
    all = {}
    def __init__(self, name, age, title):
        self.id = None
        self.name = name
        self.age = age
        self.title = title
        self.save()


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
        if any(member.name == self.name for member in Family_Member.all.values()):
            return None
        
        CURSOR.execute('''INSERT INTO family_members (name, age, title) VALUES (?,?,?)''', (self.name, self.age, self.title))
        CONN.commit()
        self.id = CURSOR.lastrowid
        Family_Member.all[self.id] = self
        

    @classmethod
    def instance_from_db(cls, row):
        for member in cls.all.values():
            if member.id == row[0]:
                member.name = row[1]
                member.age = row[2]
                member.title = row[3]
                return member
            
            member = cls(row[1], row[2], row[3])
            member.id = row[0]
            cls.all[member.id]=member

            return member
    @classmethod
    def get_all(cls):

        rows = CURSOR.execute("SELECT * FROM family_members").fetchall()
        members = []
        for row in rows:
            member = cls.instance_from_db(row)
            if member:
                members.append(member)
        
        return members
                
    def delete(self):
        CURSOR.execute("DELETE FROM family_members WHERE id=?", (self.id,))
        CONN.commit()

        del Family_Member.all[self.id]

    @classmethod
    def find_by_id(cls, id):
        member = CURSOR.execute("SELECT * FROM family_members WHERE id = ?", [id]).fetchone()
        if member:
            return cls.instance_from_db(member)
            
    @classmethod
    def update(cls, id, name, age, title):
        # find family member by id and update instance attributes accordingly then update database
        if cls.all[id]:
            cls.all[id].name = name
            cls.all[id].age = age
            cls.all[id].title = title
            #update row in database with new info
            CURSOR.execute("UPDATE family_members SET name=?, age=?, title=? WHERE id=?", (name, age, title, id))
            CONN.commit()
        else:
            raise ValueError("Family member not found.")


