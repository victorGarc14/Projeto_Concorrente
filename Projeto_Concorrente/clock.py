import threading
import time
import malha


class Clock(threading.Thread):
    def __init__(self, tick_duration=1.0):
        super().__init__(daemon=True)

        self.tick = 0
        self.tick_duration = tick_duration
        self.running = True

        # Ordem dos semáforos
        self.semaphore_order = [
            (5, 0), (5, 5), (5, 10), (5, 15),
            (10, 5), (10, 10), (10, 15), (10, 20),
        ]

        # Cada semáforo fica aberto por 6 ticks
        self.green_time = 6

        self.current_index = 0
        self.open_tick = 0

    #CONTROLE DE SEMÁFOROS

    def close_all(self):
        for sem in malha.semaforos.values():
            sem.fechar()

    def current_semaphore_pos(self):
        return self.semaphore_order[self.current_index]

    def open_current(self):
        pos = self.current_semaphore_pos()
        sem = malha.obter_semaforo(pos)

        if sem:
            sem.abrir()
            print(f"[CLOCK] Tick {self.tick:02d} -> OPEN   {pos}")

    def close_current(self):
        pos = self.current_semaphore_pos()
        sem = malha.obter_semaforo(pos)

        if sem:
            sem.fechar()
            print(f"[CLOCK] Tick {self.tick:02d} -> CLOSE  {pos}")

    def next_semaphore(self):
        self.current_index = (self.current_index + 1) % len(self.semaphore_order)
        self.open_tick = self.tick
        self.open_current()

    #LOOP PRINCIPAL

    def run(self):
        self.close_all()

        self.open_tick = 0
        self.open_current()

        while self.running:
            print(f"[CLOCK] Tick: {self.tick}")
            time.sleep(self.tick_duration)
            self.tick += 1

            if self.tick - self.open_tick >= self.green_time:
                self.close_current()
                self.next_semaphore()

    def stop(self):
        self.running = False
        self.close_all()