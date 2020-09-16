import serial
import time

# Dados da comunicação
DEVICE = '/dev/ttyACM0'
BAUD = 9600


def com_serial():
    arduino = serial.Serial(DEVICE, BAUD)
    arduino.flushInput()
    arduino.flushOutput()
    time.sleep(2)

    while True:
        # N_REQ - 4 bytes
        arduino.write(b'\x30')
        time.sleep(1)
        arduino.write(b'\x31')
        time.sleep(1)
        arduino.write(b'\x32')
        time.sleep(1)
        arduino.write(b'\x33')
        time.sleep(1)

        # cmd - 1 byte (54 ou 48)
        arduino.write(b'\x54')
        time.sleep(1)

        # data - 4 bytes
        arduino.write(b'\x00')
        time.sleep(1)
        arduino.write(b'\x00')
        time.sleep(1)
        arduino.write(b'\x00')
        time.sleep(1)
        arduino.write(b'\x00')
        time.sleep(1)

        # checksum - 2 bytes
        arduino.write(b'\xcd')
        time.sleep(1)
        arduino.write(b'\x78')
        time.sleep(1)

        # endframe
        arduino.write(b'\x04')
        time.sleep(2)

        inm = arduino.read(11).hex()
        print(type(inm))
        inm = 0
        time.sleep(2)
        # arduino.flush()


if __name__ == "__main__":

    com_serial()
