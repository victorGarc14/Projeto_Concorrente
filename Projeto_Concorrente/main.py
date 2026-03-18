import threading
import time
import malha


# =========================
# THREAD DE CONTROLE DE SEMÁFOROS
# =========================
def controlador_semaforos():
    while True:
        print("\n[CONTROLADOR] Abrindo semáforos...")
        for sem in malha.semaforos.values():
            sem.abrir()

        time.sleep(3)

        print("\n[CONTROLADOR] Fechando semáforos...")
        for sem in malha.semaforos.values():
            sem.fechar()

        time.sleep(3)


# =========================
# THREAD TESTE (SIMULA CARRO PARADO NO SINAL)
# =========================
def teste_semaforo(pos):
    sem = malha.obter_semaforo(pos)

    if sem is None:
        print("Não há semáforo nessa posição!")
        return

    print(f"[CARRO TESTE] Chegou no semáforo {pos} e vai esperar abrir...")
    
    sem.esperar_verde()

    print(f"[CARRO TESTE] Semáforo {pos} abriu! Pode seguir!")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    print("=== MALHA VIÁRIA ===\n")
    malha.print_malha()

    # Escolhe um semáforo qualquer para teste
    pos_teste = list(malha.semaforos.keys())[0]

    # Thread do controlador
    t_controlador = threading.Thread(target=controlador_semaforos, daemon=True)

    # Thread que simula um carro esperando no semáforo
    t_carro = threading.Thread(target=teste_semaforo, args=(pos_teste,))

    t_controlador.start()
    time.sleep(1)  # garante que começa fechado

    t_carro.start()

    t_carro.join()