import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    all_dogs = []
    def __init__(self, name="joey", breed = "cocker spaniel"):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(self):
        sql = """
                CREATE TABLE IF NOT EXISTS dogs(
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    breed TEXT
                )
            """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(self):
        sql = """
                DROP TABLE IF EXISTS dogs
            """
        CURSOR.execute(sql)

    def save(self):
        sql = """
                INSERT INTO dogs(name, breed)
                VALUES (?, ?)
            """
        CURSOR.execute(sql, (self.name, self.breed))
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog
    
    @classmethod
    def get_all(cls):
        sql = """
                SELECT *
                FROM dogs    
            """
        dogs = CURSOR.execute(sql).fetchall
        CONN.commit()
        return [cls.new_from_db(row) for row in dogs]