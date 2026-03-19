from clock import Clock
from car import criar_carros, snapshot_ocupacao
from ambulance import criar_ambulancia
from gui import SimulacaoGUI


if __name__ == "__main__":
    clock = Clock(tick_duration=0.8)
    carros = criar_carros(clock)
    ambulancia = criar_ambulancia(clock)
    if ambulancia:
        carros.append(ambulancia)
    clock.start()
    for carro in carros:
        carro.start()
    try:
        gui = SimulacaoGUI(clock, snapshot_ocupacao)
        gui.run()
    finally:
        for carro in carros:
            carro.stop()
        clock.stop()
        print("\nSimulação encerrada.")