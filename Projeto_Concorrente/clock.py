import threading
import time
import malha


class Clock(threading.Thread):
    def __init__(self, tick_duration=1.0):
        super().__init__(daemon=True)

        self.tick = 0
        self.tick_duration = tick_duration
        self.running = True

        self.green_time = 6

        self.tick_lock = threading.Lock()
        self.tick_cond = threading.Condition(self.tick_lock)

    def wait_next_tick(self, ultimo_tick_visto):
        with self.tick_cond:
            while self.running and self.tick <= ultimo_tick_visto:
                self.tick_cond.wait()

            if not self.running:
                return None

            return self.tick

    def alternar_todos_os_semaforos(self):
        for pos in malha.ordem_semaforos:
            sem = malha.obter_semaforo(pos)
            if sem is not None:
                sem.alternar()

    def estado_resumido(self):
        partes = []
        for indice, pos in enumerate(malha.ordem_semaforos, start=1):
            sem = malha.obter_semaforo(pos)
            estado = "L" if sem.estado == malha.LIBERA_LINHA else "C"
            partes.append(f"S{indice}:{estado}")
        return " | ".join(partes)

    def run(self):
        while self.running:
            time.sleep(self.tick_duration)

            with self.tick_cond:
                self.tick += 1
                self.tick_cond.notify_all()

            if self.tick % self.green_time == 0:
                self.alternar_todos_os_semaforos()

    def stop(self):
        self.running = False
        with self.tick_cond:
            self.tick_cond.notify_all()