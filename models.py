from PostgresDB import PgDB
class Model:
    def __init__(self):
        self.pgdb = PgDB()
    # def...
    
class User(Model):
    def __init__(self, id: int, name: str, exp: int=0, intervalic_level: int=1):
        self.id = id
        self.name = name
        self.exp = exp
        self.intervalic_level = intervalic_level

    def toString(self):
        return f"""Nombre: {self.name}
Experiencia: {self.exp}
Nivel Interválico: {self.intervalic_level}"""