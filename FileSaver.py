import os
from datetime import datetime
import json
from typing import Optional

class FileSaver:
    def __init__(self, base_path: str = "logs"):

        self.base_path = base_path
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):

        os.makedirs(self.base_path, exist_ok=True)
    
    def _generate_filename(self, timestamp: Optional[datetime] = None) -> str:
  
        if timestamp is None:
            timestamp = datetime.now()
        return timestamp.strftime("keylog_%Y-%m-%d_%H-%M-%S.log")
    
    def save_content_to_file(self, content: str, custom_filename: Optional[str] = None):
        
        filename = custom_filename if custom_filename else self._generate_filename()
        filepath = os.path.join(self.base_path, filename)
        
        try:
            with open(filepath, 'a', encoding='utf-8') as file:
                file.write(content)
            print(f"Log guardado exitosamente en: {filepath}")
        except IOError as e:
            print(f"Error al guardar el log: {e}")
    
    def save_as_json(self, data: dict, custom_filename: Optional[str] = None):
       
        filename = custom_filename if custom_filename else self._generate_filename()
        filename = filename.replace('.log', '.json')
        filepath = os.path.join(self.base_path, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            print(f"JSON guardado exitosamente en: {filepath}")
        except (IOError, TypeError) as e:
            print(f"Error al guardar el JSON: {e}")
savere = FileSaver()
