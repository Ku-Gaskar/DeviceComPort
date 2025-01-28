import time
import serial.tools.list_ports



def read_available_serial_port() ->list :
    # Получаем список всех доступных портов
    list_ports = serial.tools.list_ports.comports()
    if not list_ports:
        print("No available serial port")

    # Выводим информацию о каждом порте
    for port in list_ports:
        print(f"Устройство: {port.device}")
        print(f"Описание: {port.description}")
        print(f"Производитель: {port.manufacturer}")
        print("---")

    return list_ports


def serial_port_example():
    # Настраиваем параметры соединения
    ser = serial.Serial(
        port='COM1',  # Имя порта (в Windows: COM1, COM2 и т.д., в Linux: /dev/ttyUSB0)
        baudrate=9600,  # Скорость передачи данных
        bytesize=8,  # Размер байта данных
        parity='N',  # Четность (N - нет, E - четный, O - нечетный)
        stopbits=1,  # Количество стоп-битов
        timeout=1  # Таймаут чтения (в секундах)
    )

    try:
        # Проверяем, открыт ли порт
        if ser.is_open:
            print(f"Порт {ser.name} открыт успешно")

            # Отправка данных
            message = "Hello, COM port!"
            ser.write(message.encode())
            print(f"Отправлено: {message}")

            # Чтение данных
            while True:
                if ser.in_waiting > 0:
                    # Читаем строку до символа новой строки
                    line = ser.readline().decode('utf-8').rstrip()
                    print(f"Получено: {line}")

                    # Если получили специальное слово, завершаем работу
                    if line.strip() == "EXIT":
                        break

                time.sleep(0.1)  # Небольшая задержка для снижения нагрузки на процессор

    except serial.SerialException as e:
        print(f"Ошибка при работе с портом: {e}")

    finally:
        # Закрываем соединение
        if ser.is_open:
            ser.close()
            print("Порт закрыт")


# Дополнительные полезные функции
def list_available_ports():
    """Получение списка доступных COM портов"""
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]


def send_bytes(ser, data):
    """Отправка байтов в порт"""
    ser.write(data)


def read_bytes(ser, num_bytes):
    """Чтение определённого количества байтов"""
    return ser.read(num_bytes)



if __name__ == '__main__':
    ports = read_available_serial_port()
