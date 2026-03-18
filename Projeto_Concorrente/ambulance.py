import random
import car 
import malha

class Ambulance(car.Car):
    def __init__(self, car_id, posicao_inicial, clock):
        # A ambulância usa o tipo 'emergencia' (intervalo 1)(mudei o nome somente caso queira diminuir os ticks para 0.5)
        super().__init__(car_id, "emergencia", posicao_inicial, clock)

    def esperar_semaforo_se_necessario(self, prox):
        if not malha.eh_semaforo(prox):
            return

        sem = malha.obter_semaforo(prox)
        if sem:
            # REGRA DE PRIORIDADE: Força a abertura do sinal
            sem.forcar_liberacao(self.direcao_atual)
            # Como o método forcar_liberacao já dá o notify_all, ela pode seguir sem esperar. 

def criar_ambulancia(clock):
    """Função análoga ao criar_carros, mas específica para a ambulância"""
    posicoes = car.posicoes_iniciais_possiveis()
    if not posicoes:
        return None
    
    posicao_escolhida = random.choice(posicoes)
    # Usamos um ID alto (ex: 99) para diferenciar nos logs
    return Ambulance(99, posicao_escolhida, clock)