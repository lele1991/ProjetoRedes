from dataclasses import dataclass
from random import seed, randint
import ctypes
import struct
import binascii
import serial
import time

# Dados da comunicação
DEVICE = '/dev/ttyUSB0'
BAUD = 9600


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


def com_serial():

    arduino = serial.Serial(DEVICE, BAUD)
    arduino.flushInput()
    arduino.flushOutput()
    time.sleep(2)

    while True:
        # N_REQ - 4 bytes
        arduino.write(frame.n_req)
        # time.sleep(1)
        # arduino.write(n_req_tx[1].encode())
        # time.sleep(1)
        # arduino.write(n_req_tx[2].encode())
        # time.sleep(1)
        # arduino.write(n_req_tx[3].encode())
        time.sleep(1)

        # cmd - 1 byte (54 ou 48)
        arduino.write(frame.cmd)
        time.sleep(1)

        # data - 4 bytes
        arduino.write(frame.data)
        time.sleep(1)
        # arduino.write(data_tx[1].encode())
        # time.sleep(1)
        # arduino.write(data_tx[2].encode())
        # time.sleep(1)
        # arduino.write(n_req_tx[3].encode())
        # time.sleep(1)

        # checksum - 2 bytes
        arduino.write(frame.checksum)
        time.sleep(1)
        # arduino.write(checksum_tx[1].encode())
        # time.sleep(1)

        # endframe
        arduino.write(b'\x04')
        time.sleep(2)

        inm = arduino.read(11).hex()
        # inm = arduino.readline()
        print(inm)
        inm = 0
        time.sleep(2)


if __name__ == "__main__":
    n_req_tx = hex(random_number())
    cmd_tx = struct.pack('B', 84)
    data_tx = struct.pack('I', 0)
    checksum_tx = checksum_calc(n_req_tx, cmd_tx, data_tx)

    n_req_tx = binascii.unhexlify(n_req_tx.strip('0x'))
    checksum_tx = binascii.unhexlify(checksum_tx.strip('0x'))
    frame = Data_tx(n_req_tx, cmd_tx, data_tx, checksum_tx)

    print(frame)
    # print(checksum_tx)

    com_serial()
