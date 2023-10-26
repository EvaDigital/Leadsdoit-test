import os
import sys
from pathlib import Path

# Получите путь к корневой директории вашего проекта
project_root = Path(__file__).parent.parent

# Добавьте корневую директорию в PYTHONPATH
sys.path.insert(0, str(project_root))

# Теперь вы можете импортировать main.py из корневой директории
import main
