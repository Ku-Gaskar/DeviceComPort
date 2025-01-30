import serial

from code_command import *


class Coordinate:
    """
    Дескриптор для формирования атрибутов класса DrvCommand и записи в COM порт.
    Каждый атрибут настраивается на работу только по одной команде (например MOVE_TO_X)
    """

    def __init__(self, code_command):
        self._code_command = code_command

    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __set__(self, instance, value):
        if value is not None and type(value) == int:
            instance.__dict__[self.name] = value

            # Выполняем команду через _conn
            if hasattr(instance, "write"):
                instance.write(self._code_command, value)


class DrvCommand:
    """
    Класс обеспечивает взаимодействие GUI приложения с интерфейсом COM порта по протоколу прибора.
    """
    x = Coordinate(MOVE_TO_X)
    y = Coordinate(MOVE_TO_Y)
    z = Coordinate(MOVE_TO_Z)
    br = Coordinate(BRIGHTNESS)

    def __init__(self, conn: serial.Serial):
        self._conn = conn
        pass

    @staticmethod
    def prepare_frame(command: str, data: int) -> bytes:
        """
        Метод формирует кадр в строку: "[старт][команда (2 символа)][дата (4 символа)][стоп]"
        :return: готовый кадр для отправки
        """
        frame = ""
        if type(data) == int and (32767 >= data >= 0):
            str_data = ''.join(serial_encode.get(int(s, base=16)) for s in format(data, '04x'))
            frame = "#" + command + str_data + "\r"

        return bytes(frame, 'utf-8')

    def write(self, command: str, data: int = 0):
        """
        Выполняет запись в COM порт
        :param command: Строка из двух символов
        :param data: целое число от 0 до 32767
        :return:
        """
        frame = self.prepare_frame(command, data)
        print(frame)
        self._conn.write(frame)

    def reset(self):
        self.write(RESET)

    def is_connection(self)-> bool:
        self.write(REQUEST_READY)
        ok, fail = b'#GLHHHH\r', b'#GLQQQQ\r'
        response = self._conn.readline(8)

        if response == ok:
            return True
        elif response == fail:
            return False
        else:
            return False
            # raise Exception("Not a valid response")



if __name__ == '__main__':
    drv = DrvCommand(None)
    print(drv.prepare_frame(MOVE_TO_Y, 5689))
    drv.y = 10
    drv.x = 11
    drv.z = 1015
    drv.br = 120
