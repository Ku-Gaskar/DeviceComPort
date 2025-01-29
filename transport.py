import configparser
import os
from typing import Optional
import serial
import serial.tools.list_ports

class SerialSettings:
    """Класс для управления настройками COM-порта через INI файл"""
    
    def __init__(self, config_path: str):
        """
        Инициализация класса
        
        Args:
            config_path (str): Путь к INI файлу
        """
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self._load_settings()
    
    def _load_settings(self) -> None:
        """Загрузка настроек из файла"""
        if not os.path.exists(self.config_path):
            self._create_default_settings()
        else:
            self.config.read(self.config_path)
    
    def _create_default_settings(self) -> None:
        """Создание файла с настройками по умолчанию"""
        self.config['Serial'] = {
            'port': 'COM1',
            'baudrate': '9600',
            'bytesize': '8',
            'parity': 'N',
            'stopbits': '1',
            'timeout': '1.0'
        }
        self.save_settings()
    
    def save_settings(self) -> None:
        """Сохранение текущих настроек в файл"""
        with open(self.config_path, 'w') as file:
            self.config.write(file)
    
    def update_setting(self, setting_name: str, value: str) -> None:
        """
        Обновление значения настройки
        
        Args:
            setting_name (str): Имя настройки
            value (str): Новое значение
        """
        if setting_name in self.config['Serial']:
            self.config['Serial'][setting_name] = str(value)
            self.save_settings()
        else:
            raise ValueError(f"Неизвестная настройка: {setting_name}")
    
    def get_serial_connection(self) -> Optional[serial.Serial]:
        """
        Создание объекта Serial с текущими настройками
        
        Returns:
            Optional[serial.Serial]: Объект для работы с COM-портом
        """
        try:
            return serial.Serial(
                port=self.config['Serial']['port'],
                baudrate=int(self.config['Serial']['baudrate']),
                bytesize=int(self.config['Serial']['bytesize']),
                parity=self.config['Serial']['parity'],
                stopbits=int(self.config['Serial']['stopbits']),
                timeout=float(self.config['Serial']['timeout'])
            )
        except serial.SerialException as e:
            print(f"Ошибка при создании соединения: {e}")
            return None

    # Дополнительные полезные функции
    @staticmethod
    def list_available_ports():
        """Получение списка доступных COM портов"""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]