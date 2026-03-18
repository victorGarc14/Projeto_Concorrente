import time
import malha
from clock import Clock

if __name__ == "__main__":
    print("=== MALHA ===")
    malha.print_malha()
    print()

    clock = Clock(tick_duration=1.0)
    clock.start()

    try:
        time.sleep(30)
    except KeyboardInterrupt:
        pass
    finally:
        clock.stop()
        print("\nClock finalizado.")