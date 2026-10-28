"""Capa de datos: consultas parametrizadas a SQLite, sin decisiones musicales."""
import sqlite3
import json
from pathlib import Path

class RepositorioConocimiento:
    def __init__(self, ruta=":memory:"):
        self.db = sqlite3.connect(ruta)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(Path(__file__).with_name("esquema.sql").read_text())
        if not self.db.execute("SELECT COUNT(*) FROM hipotesis").fetchone()[0]:
            self._cargar()

    def _cargar(self):
        contenido = json.loads(Path(__file__).with_name("conocimiento.json").read_text())
        with self.db:
            self.db.executemany("INSERT INTO hipotesis VALUES (:id,:nombre,:prior)", contenido["hipotesis"])
            for variable, valores in contenido["pesos"].items():
                totales = [sum(f[i] for f in valores.values()) for i in range(5)]
                for valor, fila in valores.items():
                    self.db.executemany("INSERT INTO verosimilitud VALUES (?,?,?,?)",
                        [(variable, valor, h["id"], fila[i]/totales[i])
                         for i,h in enumerate(contenido["hipotesis"])])

    def hipotesis(self):
        return [dict(r) for r in self.db.execute("SELECT * FROM hipotesis ORDER BY id")]

    def valores(self, variable):
        return [r[0] for r in self.db.execute(
            "SELECT DISTINCT valor FROM verosimilitud WHERE variable=? ORDER BY valor", (variable,))]

    def evidencia(self, variable, valor):
        return {r[0]:r[1] for r in self.db.execute(
            "SELECT hipotesis_id, probabilidad FROM verosimilitud WHERE variable=? AND valor=?",
            (variable,valor))}

    def cerrar(self):
        self.db.close()
