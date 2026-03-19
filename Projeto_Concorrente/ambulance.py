from car import Car, ocupacao, ocupacao_lock
import malha
class Ambulancia(Car):
    def __init__(self, car_id, posicao_inicial, clock):
        super().__init__(car_id, "rapido", posicao_inicial, clock)
        self.tipo_velocidade = "ambulancia"

    def nome(self):
        return f"AMB-{self.car_id:02d}"

    def esperar_semaforo_se_necessario(self, prox):
        if not malha.eh_semaforo(prox):
            return

        sem = malha.obter_semaforo(prox)
        if sem is None:
            return

        if self.direcao_atual in (malha.RIGHT, malha.LEFT):
            sem.forcar_linha()
        else:
            sem.forcar_coluna()

        sem.esperar_liberacao(self.direcao_atual)
        
    def abrir_semaforos_a_frente(self):
        pos = self.posicao

        while True:
            prox = malha.proxima_posicao(*pos, self.direcao_atual)

            if prox is None:
                return

            if malha.eh_semaforo(prox):
                sem = malha.obter_semaforo(prox)

                if self.direcao_atual in (malha.RIGHT, malha.LEFT):
                    sem.forcar_linha()
                else:
                    sem.forcar_coluna()

                return
            if not malha.eh_transitavel(*prox):
                return

            pos = prox
            
            
    def run(self):
        while self.running:
            tick = self.clock.wait_next_tick(self.ultimo_tick_visto)
            if tick is None:
                break

            self.ultimo_tick_visto = tick

            self.abrir_semaforos_a_frente()

            if not self.pode_tentar_mover_neste_tick(tick):
                continue

            self.tentar_mover(tick)
