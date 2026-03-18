import os
import time
import malha
from clock import Clock
from car import criar_carros, snapshot_ocupacao
from ambulance import criar_ambulancia


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


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
        while True:
            ocupacao = snapshot_ocupacao()
            limpar_tela()

            print("SIMULAÇAO")
            print(f"Tick atual: {clock.tick}")
            print()
            print("Legenda:")
            print("CR = carro rápido | CM = carro médio | CL = carro lento")
            print("L  = semáforo liberando linha | C  = semáforo liberando coluna")
            print()

            print("Estados dos semáforos:")
            print(clock.estado_resumido())
            print()

            print(malha.renderizar_com_carros(ocupacao))
            time.sleep(0.2)

    except KeyboardInterrupt:
        pass
    finally:
        for carro in carros:
            carro.stop()
        clock.stop()
        print("\nSimulação encerrada.")