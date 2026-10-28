"""Capa de negocio: actualización bayesiana incremental y trazabilidad."""
class MotorInferencia:
    def __init__(self, repositorio):
        self.repo = repositorio
        self.catalogo = self.repo.hipotesis()
        self.respuestas = {}
        self.traza = []
        self.posterior = {h["id"]:h["prior"] for h in self.catalogo}

    def responder(self, variable, valor):
        if variable in self.respuestas:
            raise ValueError("Variable ya respondida; inicie una sesión nueva para corregirla.")
        probabilidades = self.repo.evidencia(variable, valor)
        if set(probabilidades) != set(self.posterior):
            raise ValueError("Respuesta desconocida o conocimiento incompleto.")
        anterior = self.posterior.copy()
        productos = {h:anterior[h]*probabilidades[h] for h in anterior}
        normalizador = sum(productos.values())
        self.posterior = {h:p/normalizador for h,p in productos.items()}
        self.respuestas[variable] = valor
        self.traza.append({"variable":variable,"valor":valor,"anterior":anterior,
                           "verosimilitudes":probabilidades,"normalizador":normalizador,
                           "posterior":self.posterior.copy()})
        return self.ranking()

    def ranking(self):
        return sorted([{"id":h["id"],"nombre":h["nombre"],
                        "probabilidad":self.posterior[h["id"]]} for h in self.catalogo],
                      key=lambda h:(-h["probabilidad"],h["id"]))
