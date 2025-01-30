import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
from typing import Callable, Optional

class SerialSettingsDialog(tk.Toplevel):
# class SerialSettingsDialog:
    def __init__(self, parent, settings_manager, on_save: Optional[Callable] = None):
        """
        Диалоговое окно настроек COM-порта
        
        Args:
            parent: Родительское окно
            settings_manager: Экземпляр класса SerialSettings
            on_save: Callback-функция, вызываемая после сохранения настроек
        """
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.on_save = on_save
        
        self.title("Настройки COM-порта")
        self.resizable(False, False)
        
        # Делаем окно модальным
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        self._load_current_settings()
        
        # Центрируем окно относительно родительского
        self.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50))

    def _create_widgets(self):
        """Создание элементов интерфейса"""
        mainframe = ttk.Frame(self, padding="10")
        mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # COM порт
        ttk.Label(mainframe, text="COM порт:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(mainframe, textvariable=self.port_var)
        self.port_combo['values'] = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Скорость
        ttk.Label(mainframe, text="Скорость:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.baudrate_var = tk.StringVar()
        baudrates = ['1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200']
        self.baudrate_combo = ttk.Combobox(mainframe, textvariable=self.baudrate_var, values=baudrates)
        self.baudrate_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Размер байта
        ttk.Label(mainframe, text="Размер байта:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.bytesize_var = tk.StringVar()
        bytesizes = ['5', '6', '7', '8']
        self.bytesize_combo = ttk.Combobox(mainframe, textvariable=self.bytesize_var, values=bytesizes)
        self.bytesize_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Четность
        ttk.Label(mainframe, text="Четность:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.parity_var = tk.StringVar()
        parities = [('Нет', 'N'), ('Четный', 'E'), ('Нечетный', 'O'), ('Отметка', 'M'), ('Пробел', 'S')]
        self.parity_combo = ttk.Combobox(mainframe, textvariable=self.parity_var)
        self.parity_combo['values'] = [p[0] for p in parities]
        self.parity_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Стоп-биты
        ttk.Label(mainframe, text="Стоп-биты:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.stopbits_var = tk.StringVar()
        stopbits = ['1', '1.5', '2']
        self.stopbits_combo = ttk.Combobox(mainframe, textvariable=self.stopbits_var, values=stopbits)
        self.stopbits_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Таймаут
        ttk.Label(mainframe, text="Таймаут (сек):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.timeout_var = tk.StringVar()
        self.timeout_entry = ttk.Entry(mainframe, textvariable=self.timeout_var)
        self.timeout_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Кнопка сохранить
        ttk.Button(mainframe, text="Сохранить", command=self._save_settings).grid(
            row=6, column=0, columnspan=2, pady=20)
        
        # Настраиваем отступы
        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5)

    def _load_current_settings(self):
        """Загрузка текущих настроек"""
        config = self.settings_manager.config['Serial']
        
        self.port_var.set(config['port'])
        self.baudrate_var.set(config['baudrate'])
        self.bytesize_var.set(config['bytesize'])
        
        # Преобразование кода четности в читаемый текст
        parity_map = {'N': 'Нет', 'E': 'Четный', 'O': 'Нечетный', 'M': 'Отметка', 'S': 'Пробел'}
        self.parity_var.set(parity_map.get(config['parity'], 'Нет'))
        
        self.stopbits_var.set(config['stopbits'])
        self.timeout_var.set(config['timeout'])

    def _save_settings(self):
        """Сохранение настроек"""
        # Преобразование читаемого текста в код четности
        parity_map = {
            'Нет': 'N', 'Четный': 'E', 'Нечетный': 'O', 
            'Отметка': 'M', 'Пробел': 'S'
        }
        
        # Обновляем все настройки
        self.settings_manager.update_setting('port', self.port_var.get())
        self.settings_manager.update_setting('baudrate', self.baudrate_var.get())
        self.settings_manager.update_setting('bytesize', self.bytesize_var.get())
        self.settings_manager.update_setting('parity', parity_map[self.parity_var.get()])
        self.settings_manager.update_setting('stopbits', self.stopbits_var.get())
        self.settings_manager.update_setting('timeout', self.timeout_var.get())
        
        # Вызываем callback, если он задан
        if self.on_save:
            self.on_save()
            
        self.destroy()
