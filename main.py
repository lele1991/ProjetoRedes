import random
import ctypes
from datetime import datetime
from dataclasses import dataclass
import serial
import time
import struct

# DEVICE = '/dev/ttyUSB0'
DEVICE = '/dev/ttyACM0'
BAUD = 9600
TEMPERATURE = 84
HUMIDITY = 72
ENDFRAME = b'\x04'

arduino = serial.Serial(DEVICE, BAUD)


@dataclass
class Package:
    n_req: ctypes.c_uint32
    cmd: ctypes.c_uint8
    data: ctypes.c_uint32
    checksum: ctypes.c_uint16


def com_serial():
    arduino.flushInput()
    arduino.flushOutput()
    time.sleep(2)

    # while True:
    # N_REQ - 4 bytes
    arduino.write(frame.n_req)
    time.sleep(1)

    # cmd - 1 byte (54 ou 48)
    arduino.write(frame.cmd)
    time.sleep(1)

    # data - 4 bytes
    arduino.write(frame.data)
    time.sleep(1)

    # checksum - 2 bytes
    arduino.write(frame.checksum)
    time.sleep(1)
    # time.sleep(1)

    # endframe
    arduino.write(ENDFRAME)
    time.sleep(2)

    recived_data = arduino.read(11).hex()
    # RECIVED_DATA = arduino.readline()
    # print(recived_data)
    # recived_data = 0
    time.sleep(2)
    return recived_data


def random_number():
    random.seed(datetime.now())

    value = random.randint(1, 4294967296-2)
    # print((value))
    return value


def checksum_calc(n_req, cmd, data):
    n_req_int = int(n_req, 16)
    cmd_int = int(cmd, 16)
    data_int = int(data, 16)

    check = (n_req_int + cmd_int + data_int)
    checksum = int(hex((check ^ 0xffffff))[6:], 16)
    return hex(checksum)


def ordered_data(recived_data):
    orderless_data = recived_data.strip('')
    n = 2
    orderless_data = [orderless_data[i:i+n]
                      for i in range(0, len(orderless_data), n)]

    n_req_order = ''.join((orderless_data[:4])[::-1])
    cmd_order = ''.join((orderless_data[4:5])[::-1])
    data_order = ''.join((orderless_data[5:9])[::-1])
    check_order = ''.join((orderless_data[9:11])[::-1])

    # print(n_req_order, cmd_order, data_order, check_order)

    n_req_order = hex(int(n_req_order, 16))
    cmd_order = hex(int(cmd_order, 16))
    data_order = hex(int(data_order, 16))
    check_order = hex(int(check_order, 16))

    return n_req_order, cmd_order, data_order, check_order


if __name__ == "__main__":
    while True:
        n_req = hex(random_number())
        cmd = hex(TEMPERATURE)
        data = hex(0)
        checksum = checksum_calc(n_req, cmd, data)

        # print(n_req, cmd, data, checksum)

        n_req_packed = struct.pack('>I', int(n_req, 16))
        cmd_packed = struct.pack('B', int(cmd, 16))
        data_packed = struct.pack('>I', int(data, 16))
        checksum_packed = struct.pack('>H', int(checksum, 16))

        frame = Package(n_req_packed, cmd_packed, data_packed, checksum_packed)
        # print(frame)
        recived_frame = com_serial()
        # print(recived_frame)

        n_req_order, cmd_order, data_order, check_order = ordered_data(
            recived_frame)

        checksum_recived = checksum_calc(n_req_order, cmd_order, data_order)
        # print(check_order, checksum_recived)

        mesure_float = struct.pack('>I', int(data_order, 16))

        if (checksum_recived == check_order):
            if(cmd == hex(TEMPERATURE)):
                print('Temperatura: {} °C "'.format(
                    struct.unpack('>f', mesure_float)[0]))
            elif (cmd == hex(HUMIDITY)):
                print('Umidade: {} % "'.format(
                    struct.unpack('>f', mesure_float)[0]))
            else:
                print('Comando não encontrado')
        else:
            print('Erro no Checksum recebido!')
