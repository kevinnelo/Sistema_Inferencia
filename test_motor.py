import unittest
from datos import RepositorioConocimiento
from negocio import MotorInferencia

class Pruebas(unittest.TestCase):
    def setUp(self):
        self.repo = RepositorioConocimiento()
        self.motor = MotorInferencia(self.repo)
    def tearDown(self):
        self.repo.cerrar()
    def test_distribuciones(self):
        for fila in self.repo.db.execute("SELECT variable,hipotesis_id,SUM(probabilidad) FROM verosimilitud GROUP BY variable,hipotesis_id"):
            self.assertAlmostEqual(fila[2],1)
    def test_bayes_y_traza(self):
        self.motor.responder("reaccion_publico","baila_y_canta")
        fila=self.motor.traza[-1]
        for h in self.motor.posterior:
            self.assertAlmostEqual(self.motor.posterior[h],fila["anterior"][h]*fila["verosimilitudes"][h]/fila["normalizador"])
        self.assertEqual(self.motor.ranking()[0]["id"],"H1")
        self.assertAlmostEqual(sum(self.motor.posterior.values()),1)
    def test_neutralidad_edad_genero(self):
        original=self.motor.posterior.copy()
        self.motor.responder("grupo_edad","adultos_mayores")
        self.motor.responder("genero_actual","rock")
        for h in original: self.assertAlmostEqual(original[h],self.motor.posterior[h])
    def test_repetida_e_invalida(self):
        with self.assertRaises(ValueError): self.motor.responder("momento","inventado")
        self.assertEqual(self.motor.traza,[])
        self.motor.responder("momento","cierre")
        with self.assertRaises(ValueError): self.motor.responder("momento","inicio")
        self.assertEqual(len(self.motor.traza),1)
    def test_orden(self):
        otro=MotorInferencia(self.repo)
        self.motor.responder("momento","cierre")
        self.motor.responder("reaccion_publico","baila_poco")
        otro.responder("reaccion_publico","baila_poco")
        otro.responder("momento","cierre")
        for h in otro.posterior: self.assertAlmostEqual(otro.posterior[h],self.motor.posterior[h])

if __name__ == "__main__": unittest.main()
