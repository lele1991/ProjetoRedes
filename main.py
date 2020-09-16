from dataclasses import dataclass
from random import seed, randint
import ctypes
import struct
import binascii
import serial
import time

# -*- coding: utf-8 -*-
# Dados da comunicação
DEVICE = '/dev/ttyUSB0'
BAUD = 9600
# RECIVED_DATA = 'd8a56d3cff3333e741f525'
arduino = serial.Serial(DEVICE, BAUD)


@dataclass
class Data_tx:
    n_req: ctypes.c_uint32
    cmd: ctypes.c_uint8
    data: ctypes.c_uint32
    checksum: ctypes.c_uint16


def random_number():
    seed(4)

    value = randint(1, 4294967296-1)
    # print(value)
    return value


def checksum_calc(n_req, cmd, data):
    n_req_unpacked = int(n_req, 0)
    cmd_unpacked = struct.unpack('B', cmd)[0]
    data_unpacked = struct.unpack('I', data)[0]

    # print(n_req_unpacked, cmd_unpacked, data_unpacked)
    check = (n_req_unpacked + cmd_unpacked + data_unpacked)
    checksum = hex((check ^ 0xffffff))[6:]
    return checksum


def split_frame(data):
    data_splited = []
    for i in range(0, len(data)):
        data_splited.append(hex(data[i]))
    return data_splited


def ordered_data(recived_data):
    orderless_data = recived_data.strip('')
    n = 2
    orderless_data = [orderless_data[i:i+n]
                      for i in range(0, len(orderless_data), n)]

    n_req_order = ''.join((orderless_data[:4])[::-1])
    cmd_order = ''.join((orderless_data[4:5])[::-1])
    data_order = ''.join((orderless_data[5:9])[::-1])
    check_order = ''.join((orderless_data[9:11])[::-1])

    # print(int(hex(int(data_order, 16)), 0))

    n_req_order = hex(int(n_req_order, 16))
    cmd_order = struct.pack('>B', int(cmd_order, 16))
    data_order = struct.pack('>I', int(data_order, 16))
    check_order = struct.pack('>H', int(check_order, 16))

    # print(data_order)

    return n_req_order, cmd_order, data_order, check_order


def com_serial():
    arduino.flushInput()
    arduino.flushOutput()
    time.sleep(2)
    print('Ho')
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
    arduino.write(b'\x04')
    time.sleep(2)

    RECIVED_DATA = arduino.read(11).hex()
    # RECIVED_DATA = arduino.readline()
    print(RECIVED_DATA)
    # RECIVED_DATA = 0
    time.sleep(2)
    return RECIVED_DATA


if __name__ == "__main__":
    n_req_tx = hex(random_number())
    cmd_tx = struct.pack('B', 72)
    data_tx = struct.pack('I', 0)

    checksum_tx = checksum_calc(n_req_tx, cmd_tx, data_tx)

    n_req_tx = binascii.unhexlify(n_req_tx.strip('0x'))

    checksum_tx = binascii.unhexlify(checksum_tx.strip('0x'))
    frame = Data_tx(n_req_tx, cmd_tx, data_tx, checksum_tx)
    print(frame)
    # com_serial()
    while True:
        print(frame)
        recived_data = com_serial()
        n_req_order, cmd_order, data_order, check_order = ordered_data(
            recived_data)

        # print(checksum_calc(n_req_order, cmd_order, data_order))
        print(frame.cmd)
        checksum_recived = True
        if (checksum_recived):
            if (frame.cmd == b'\x54'):
                print("Temperatura: ")
                print(struct.unpack('>f', data_order)[0])
            elif (frame.cmd == b'\x48'):
                print('Umidade: ')
                print(struct.unpack('>f', data_order)[0])
