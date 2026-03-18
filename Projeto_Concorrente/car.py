import random
import threading
import malha


VELOCIDADES = {
    "emergencia": 1,
    "rapido": 1,
    "medio": 2,
    "lento": 4,
}

ocupacao = {}
ocupacao_lock = threading.Lock()


def posicoes_iniciais_possiveis():
    posicoes = []

    for i in range(malha.LINHAS):
        for j in range(malha.COLUNAS):
            if malha.eh_transitavel(i, j) and not malha.eh_semaforo((i, j)):
                posicoes.append((i, j))

    return posicoes


class Car(threading.Thread):
    def __init__(self, car_id, tipo_velocidade, posicao_inicial, clock):
        super().__init__(daemon=True)

        self.car_id = car_id
        self.tipo_velocidade = tipo_velocidade
        self.intervalo_ticks = VELOCIDADES[tipo_velocidade]
        self.posicao = posicao_inicial
        self.clock = clock
        self.running = True

        self.ultimo_tick_visto = -1
        self.direcao_atual = self.direcao_inicial()

        with ocupacao_lock:
            ocupacao[self.posicao] = self

    def nome(self):
        return f"Car-{self.car_id:02d}-{self.tipo_velocidade.upper()}"

    def direcao_inicial(self):
        i, j = self.posicao

        horizontal = malha.direcao_horizontal_da_linha(i)
        vertical = malha.direcao_vertical_da_coluna(j)

        if horizontal is not None:
            return horizontal
        if vertical is not None:
            return vertical

        return malha.direcao_em(i, j)

    def pode_tentar_mover_neste_tick(self, tick):
        return tick % self.intervalo_ticks == 0

    def eixo_horizontal(self, direcao):
        return direcao in (malha.RIGHT, malha.LEFT)

    def eixo_vertical(self, direcao):
        return direcao in (malha.UP, malha.DOWN)

    def direcao_disponivel(self, direcao):
        prox = malha.proxima_posicao(*self.posicao, direcao)
        if prox is None:
            return None
        if not malha.eh_transitavel(*prox):
            return None
        return prox

    def opcoes_de_movimento(self):
        i, j = self.posicao

        horizontal = malha.direcao_horizontal_da_linha(i)
        vertical = malha.direcao_vertical_da_coluna(j)

        opcoes = []

        if self.eixo_vertical(self.direcao_atual):
            # prefere continuar no eixo vertical, mas aceita virar para linha
            if vertical is not None:
                prox_vertical = self.direcao_disponivel(vertical)
                if prox_vertical is not None:
                    opcoes.append((vertical, prox_vertical))

            if horizontal is not None:
                prox_horizontal = self.direcao_disponivel(horizontal)
                if prox_horizontal is not None:
                    opcoes.append((horizontal, prox_horizontal))
        else:
            # prefere continuar no eixo horizontal, mas aceita virar para coluna
            if horizontal is not None:
                prox_horizontal = self.direcao_disponivel(horizontal)
                if prox_horizontal is not None:
                    opcoes.append((horizontal, prox_horizontal))

            if vertical is not None:
                prox_vertical = self.direcao_disponivel(vertical)
                if prox_vertical is not None:
                    opcoes.append((vertical, prox_vertical))

        # remove duplicatas caso apareçam
        unicas = []
        vistos = set()
        for direcao, prox in opcoes:
            chave = (direcao, prox)
            if chave not in vistos:
                vistos.add(chave)
                unicas.append((direcao, prox))

        return unicas

    def escolher_movimento(self):
        opcoes = self.opcoes_de_movimento()

        if not opcoes:
            return None

        # se houver mais de uma opção, escolhe aleatoriamente
        direcao_escolhida, prox = random.choice(opcoes)
        self.direcao_atual = direcao_escolhida
        return prox

    def esperar_semaforo_se_necessario(self, prox):
        if not malha.eh_semaforo(prox):
            return

        sem = malha.obter_semaforo(prox)
        if sem is None:
            return

        if self.direcao_atual in (malha.RIGHT, malha.LEFT):
            if sem.libera_linha():
                return
        else:
            if sem.libera_coluna():
                return

        sem.esperar_liberacao(self.direcao_atual)

    def tentar_mover(self, tick):
        prox = self.escolher_movimento()
        if prox is None:
            return

        self.esperar_semaforo_se_necessario(prox)

        with ocupacao_lock:
            if prox in ocupacao:
                carro_frente = ocupacao[prox]

                # desaceleração natural
                if self.intervalo_ticks < carro_frente.intervalo_ticks:
                    return
                return

            del ocupacao[self.posicao]
            ocupacao[prox] = self
            self.posicao = prox

    def run(self):
        while self.running:
            tick = self.clock.wait_next_tick(self.ultimo_tick_visto)
            if tick is None:
                break

            self.ultimo_tick_visto = tick

            if not self.pode_tentar_mover_neste_tick(tick):
                continue

            self.tentar_mover(tick)

    def stop(self):
        self.running = False

    def __repr__(self):
        return f"{self.nome()}@{self.posicao}"


def criar_carros(clock):
    tipos = [
        "rapido", "rapido",
        "medio", "medio",
        "lento", "lento",
        "medio", "medio", "medio", "medio",
    ]

    posicoes = posicoes_iniciais_possiveis()
    escolhidas = random.sample(posicoes, len(tipos))

    carros = []
    for idx, (tipo, pos) in enumerate(zip(tipos, escolhidas), start=1):
        carro = Car(idx, tipo, pos, clock)
        carros.append(carro)

    return carros


def snapshot_ocupacao():
    with ocupacao_lock:
        return dict(ocupacao)


def estado_atual_carros():
    with ocupacao_lock:
        return sorted(
            [(car.car_id, car.tipo_velocidade, pos) for pos, car in ocupacao.items()],
            key=lambda x: x[0]
        )