"""Capa de presentación: cuestionario de consola. Python 3, sin dependencias."""
import argparse
import json
from datos import RepositorioConocimiento
from negocio import MotorInferencia

class ConsolaDJ:
    VARIABLES = ("tipo_evento","momento","grupo_edad","genero_actual","reaccion_publico")
    def __init__(self, motor):
        self.motor = motor

    def mostrar(self):
        for h in self.motor.ranking():
            print(f"{h['id']} {h['nombre']}: {100*h['probabilidad']:.2f}%")

    def ejecutar(self):
        print("Probabilidades ilustrativas; requieren validación del experto.")
        for variable in self.VARIABLES:
            valores = self.motor.repo.valores(variable)
            print("\n"+variable+": "+", ".join(valores))
            respuesta = input("Respuesta (Enter omite): ").strip()
            while respuesta and respuesta not in valores:
                respuesta = input("Valor inválido. Intente de nuevo: ").strip()
            if respuesta:
                self.motor.responder(variable,respuesta)
                self.mostrar()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    repo = RepositorioConocimiento()
    motor = MotorInferencia(repo)
    ui = ConsolaDJ(motor)
    try:
        if args.demo:
            for variable,valor in zip(ui.VARIABLES,
                ("discoteca","desarrollo","jovenes","pop","baila_y_canta")):
                motor.responder(variable,valor)
                print("\nConsulta:",variable,"=",valor)
                ui.mostrar()
        else:
            ui.ejecutar()
        with open("traza.json","w",encoding="utf-8") as archivo:
            json.dump(motor.traza,archivo,ensure_ascii=False,indent=2)
    finally:
        repo.cerrar()
