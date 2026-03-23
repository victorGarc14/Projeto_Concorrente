from malha import LEFT, RIGHT, UP, DOWN
import tkinter as tk
from PIL import Image, ImageTk
import malha
import os
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPRITE_PATH = os.path.join(BASE_DIR, "sprites")

CELL_SIZE = 30


class SimulacaoGUI:
    def __init__(self, clock, snapshot_func):
        self.clock = clock
        self.snapshot_func = snapshot_func
        self.last_tick = -1

        self.root = tk.Tk()
        self.root.title("Simulação de Tráfego")

        largura = malha.COLUNAS * CELL_SIZE
        altura = malha.LINHAS * CELL_SIZE

        self.canvas = tk.Canvas(self.root, width=largura, height=altura)
        self.canvas.pack()

        self.info = tk.Label(self.root, text="", font=("Arial", 12))
        self.info.pack()

        self.carro_rapido = self.carregar_sprite_direcional("carro_rapido.png")
        self.carro_medio = self.carregar_sprite_direcional("carro_medio.png")
        self.carro_lento = self.carregar_sprite_direcional("carro_lento.png")
        self.ambulancia = self.carregar_sprite_direcional("ambulancia.png")

        self.semaforo_linha = self.carregar_imagem("semaforo_linha.png")
        self.semaforo_coluna = self.carregar_imagem("semaforo_coluna.png")

        self.atualizar()
    
    def carregar_imagem(self, nome):
        caminho = os.path.join(SPRITE_PATH, nome)
        try:
            img = Image.open(caminho)
            img = img.resize((CELL_SIZE, CELL_SIZE), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Erro ao carregar {nome}: {caminho}")
            return None
    
    def carregar_sprite_direcional(self, nome):
        caminho = os.path.join(SPRITE_PATH, nome)
        try:
            img = Image.open(caminho)
            img = img.resize((CELL_SIZE, CELL_SIZE), Image.LANCZOS)

            return {
                RIGHT: ImageTk.PhotoImage(img),
                LEFT: ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)),
                UP: ImageTk.PhotoImage(img.rotate(90, expand=True)),
                DOWN: ImageTk.PhotoImage(img.rotate(-90, expand=True)),
            }
        except Exception as e:
            print(f"Erro ao carregar {nome}: {caminho}")
            return None

    def desenhar_sprite(self, i, j, imagem):
        x = j * CELL_SIZE + CELL_SIZE // 2
        y = i * CELL_SIZE + CELL_SIZE // 2
        self.canvas.create_image(x, y, image=imagem)
        
    def desenhar_rua(self, i, j):
        x1 = j * CELL_SIZE
        y1 = i * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE

        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill="#cccccc",
            outline="black"
        )
        direcao = malha.direcoes_base[i][j]
        simbolos = {
            malha.RIGHT: "→",
            malha.LEFT: "←",
            malha.UP: "↑",
            malha.DOWN: "↓",
        }

        if direcao in simbolos:
            self.canvas.create_text(
                (x1 + x2) // 2,
                (y1 + y2) // 2,
                text=simbolos[direcao],
                font=("Arial", 12)
            )

    def atualizar(self):
        try:
            if self.last_tick != self.clock.tick:
                self.last_tick = self.clock.tick
                ocupacao = self.snapshot_func()
                self.canvas.delete("all")
                for i in range(malha.LINHAS):
                    for j in range(malha.COLUNAS):
                        if (i, j) in ocupacao:
                            carro = ocupacao[(i, j)]
                            direcao = carro.get_direcao_atual()
                            if carro.tipo_velocidade == "ambulancia":
                                self.desenhar_sprite(i, j, self.ambulancia[direcao])
                            elif carro.tipo_velocidade == "rapido":
                                self.desenhar_sprite(i, j, self.carro_rapido[direcao])
                            elif carro.tipo_velocidade == "medio":
                                self.desenhar_sprite(i, j, self.carro_medio[direcao])
                            else:
                                self.desenhar_sprite(i, j, self.carro_lento[direcao])
                            continue
                        
                        if malha.eh_semaforo((i, j)):
                            sem = malha.semaforos[(i, j)]
                            if sem.estado == malha.LIBERA_LINHA:
                                self.desenhar_sprite(i, j, self.semaforo_linha)
                            else:
                                self.desenhar_sprite(i, j, self.semaforo_coluna)
                            continue
                        
                        if malha.malha[i][j] != malha.EMPTY:
                            self.desenhar_rua(i, j)
                
            self.root.after(40, self.atualizar)
        except Exception as e:
            print(f"Erro na atualização da GUI: {e}")
            self.root.after(40, self.atualizar)

    def run(self):
        self.root.mainloop()