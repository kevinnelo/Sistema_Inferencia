PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS hipotesis (
 id TEXT PRIMARY KEY, nombre TEXT NOT NULL, prior REAL NOT NULL CHECK(prior>0 AND prior<=1));
CREATE TABLE IF NOT EXISTS verosimilitud (
 variable TEXT NOT NULL, valor TEXT NOT NULL,
 hipotesis_id TEXT NOT NULL REFERENCES hipotesis(id),
 probabilidad REAL NOT NULL CHECK(probabilidad>0 AND probabilidad<=1),
 PRIMARY KEY(variable,valor,hipotesis_id));
