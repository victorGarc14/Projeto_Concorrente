import threading


#CONSTANTES
EMPTY = 0
RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4
SEMAPHORE = 5

#estado do semáforo
LIBERA_LINHA = 0
LIBERA_COLUNA = 1

LINHAS = 13
COLUNAS = 21


#CLASSE SEMÁFORO
class Semaforo:
    def __init__(self, estado_inicial=LIBERA_LINHA):
        self.estado = estado_inicial
        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)

    def libera_linha(self):
        return self.estado == LIBERA_LINHA

    def libera_coluna(self):
        return self.estado == LIBERA_COLUNA

    def alternar(self):
        with self.cond:
            if self.estado == LIBERA_LINHA:
                self.estado = LIBERA_COLUNA
            else:
                self.estado = LIBERA_LINHA
            self.cond.notify_all()

    def definir_estado(self, novo_estado):
        with self.cond:
            self.estado = novo_estado
            self.cond.notify_all()

    def esperar_liberacao(self, direcao):
        with self.cond:
            while True:
                if direcao in (RIGHT, LEFT) and self.estado == LIBERA_LINHA:
                    return
                if direcao in (UP, DOWN) and self.estado == LIBERA_COLUNA:
                    return
                self.cond.wait()



#ESTRUTURAS DA MALHA
malha = [[EMPTY for _ in range(COLUNAS)] for _ in range(LINHAS)]
direcoes_base = [[EMPTY for _ in range(COLUNAS)] for _ in range(LINHAS)]
semaforos = {}

ordem_semaforos = [
    (5, 0),
    (5, 5),
    (5, 10),
    (5, 15),
    (10, 5),
    (10, 10),
    (10, 15),
    (10, 20),
]


def construir_malha():
    for i in range(LINHAS):
        for j in range(COLUNAS):
            malha[i][j] = EMPTY
            direcoes_base[i][j] = EMPTY

    semaforos.clear()

    # LINHAS HORIZONTAIS
    for j in range(COLUNAS):
        malha[0][j] = LEFT
        direcoes_base[0][j] = LEFT

        malha[5][j] = LEFT
        direcoes_base[5][j] = LEFT

        malha[10][j] = RIGHT
        direcoes_base[10][j] = RIGHT

        malha[12][j] = RIGHT
        direcoes_base[12][j] = RIGHT

    # COLUNAS VERTICAIS
    for i in range(LINHAS):
        malha[i][0] = DOWN
        direcoes_base[i][0] = DOWN

    for i in range(6, 10):
        malha[i][5] = UP
        direcoes_base[i][5] = UP

        malha[i][10] = DOWN
        direcoes_base[i][10] = DOWN

        malha[i][15] = UP
        direcoes_base[i][15] = UP

    for i in range(LINHAS):
        malha[i][20] = UP
        direcoes_base[i][20] = UP

    # SEMÁFOROS
    for indice, (i, j) in enumerate(ordem_semaforos, start=1):
        malha[i][j] = SEMAPHORE
        estado_inicial = LIBERA_LINHA if indice % 2 == 1 else LIBERA_COLUNA
        semaforos[(i, j)] = Semaforo(estado_inicial=estado_inicial)


def dentro(i, j):
    return 0 <= i < LINHAS and 0 <= j < COLUNAS


def obter_semaforo(pos):
    return semaforos.get(pos)


def eh_semaforo(pos):
    return pos in semaforos


def direcao_em(i, j):
    return direcoes_base[i][j]


def eh_transitavel(i, j):
    if not dentro(i, j):
        return False
    return direcoes_base[i][j] != EMPTY or eh_semaforo((i, j))


def proxima_posicao(i, j, direcao):
    if direcao == RIGHT:
        ni, nj = i, j + 1
    elif direcao == LEFT:
        ni, nj = i, j - 1
    elif direcao == UP:
        ni, nj = i - 1, j
    elif direcao == DOWN:
        ni, nj = i + 1, j
    else:
        return None

    if not dentro(ni, nj):
        return None

    return ni, nj


def direcao_horizontal_da_linha(i):
    if i in (10, 12):
        return RIGHT
    if i in (0, 5):
        return LEFT
    return None


def direcao_vertical_da_coluna(j):
    if j in (0, 10):
        return DOWN
    if j in (5, 15, 20):
        return UP
    return None


def simbolo_base(i, j):
    if eh_semaforo((i, j)):
        sem = semaforos[(i, j)]
        return "L " if sem.estado == LIBERA_LINHA else "C "

    valor = malha[i][j]
    if valor == RIGHT:
        return "→ "
    if valor == LEFT:
        return "← "
    if valor == UP:
        return "↑ "
    if valor == DOWN:
        return "↓ "
    return "  "


def renderizar_com_carros(ocupacao):
    linhas_render = []

    cabecalho = "     " + " ".join(f"{j:>2}" for j in range(COLUNAS))
    linhas_render.append(cabecalho)
    linhas_render.append("")

    for i in range(LINHAS):
        partes = [f"{i:>2} |"]
        for j in range(COLUNAS):
            if (i, j) in ocupacao:
                carro = ocupacao[(i, j)]
                if carro.tipo_velocidade == "rapido":
                    celula = "CR"
                elif carro.tipo_velocidade == "medio":
                    celula = "CM"
                else:
                    celula = "CL"
            else:
                celula = simbolo_base(i, j)

            partes.append(f"{celula:>2}")
        linhas_render.append(" ".join(partes))

    return "\n".join(linhas_render)


def print_malha():
    print(renderizar_com_carros({}))


construir_malha()