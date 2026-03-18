import threading


#CONSTANTES

EMPTY = 0
RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4
SEMAPHORE = 5

LINHAS = 13
COLUNAS = 21

#CLASSE SEMÁFORO

class Semaforo:
    def __init__(self, estado_inicial=0):
        self.estado = estado_inicial
        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)

    def esperar_verde(self):
        with self.cond:
            while self.estado == 0:
                self.cond.wait()

    def abrir(self):
        with self.cond:
            self.estado = 1
            self.cond.notify_all()

    def fechar(self):
        with self.cond:
            self.estado = 0


#ESTRUTURAS DA MALHA

malha = [[EMPTY for _ in range(COLUNAS)] for _ in range(LINHAS)]
semaforos = {}


def construir_malha():
    # limpa a malha
    for i in range(LINHAS):
        for j in range(COLUNAS):
            malha[i][j] = EMPTY

    semaforos.clear()

    # LINHAS HORIZONTAIS

    for j in range(COLUNAS):
        malha[0][j] = LEFT      # linha 0  ->
        malha[5][j] = LEFT       # linha 5  <-
        malha[10][j] = RIGHT     # linha 10 ->
        malha[12][j] = RIGHT     # linha 12 -> 

    #COLUNAS VERTICAIS

    # coluna 0 inteira ↓
    for i in range(LINHAS):
        malha[i][0] = DOWN

    # colunas 5, 10, 15 apenas entre linhas 6 e 9
    for i in range(6, 10):
        malha[i][5] = UP
        malha[i][10] = DOWN
        malha[i][15] = UP

    # coluna 20 inteira ↑ 
    for i in range(LINHAS):
        malha[i][20] = UP

    # SEMÁFOROS
    posicoes_semaforos = [
        (10, 5), (10, 10), (10, 15), (10, 20),
        (5, 0), (5, 5), (5, 10), (5, 15),
    ]

    for i, j in posicoes_semaforos:
        malha[i][j] = SEMAPHORE
        semaforos[(i, j)] = Semaforo(estado_inicial=0)

#VISUALIZAÇÃO
def print_malha():
    simbolos = {
        EMPTY: " ",
        RIGHT: "→",
        LEFT: "←",
        UP: "↑",
        DOWN: "↓",
        SEMAPHORE: "●",
    }

    for i in range(LINHAS):
        linha = ""
        for j in range(COLUNAS):
            linha += simbolos[malha[i][j]] + " "
        print(linha)


def obter_semaforo(pos):
    return semaforos.get(pos)


def tem_semaforo_adjacente(i, j):
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = i + di, j + dj
        if (ni, nj) in semaforos:
            return (ni, nj)
    return None


# =========================
# INICIALIZAÇÃO
# =========================
construir_malha()