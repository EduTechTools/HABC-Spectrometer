from time import sleep
import busio
import board
from adafruit_as7341 import AS7341
import adafruit_fram
def write_sample(sample):
    # Sample is a list of 8 ints
    global fram
    global fram_index
    # Don't allow write if we have filled memory (32K FRAM module)
    if (fram_index < 32768 - 16):
        print ("Writing Sample")
        for n in range(0,8):
            curr_bytes = sample[n].to_bytes(2, 'big')
            for bc in range(0,2):
                fram[fram_index] = curr_bytes[bc]
                fram_index = fram_index + 1
    else:
        print ("All full")
def write_sensor():
    write_sample(sensor.all_channels)
def write_test():
    global fram
    global fram_index
    test_data = list()
    for n in range(0,8):
        test_data.append(0)
    write_sample(test_data)
def dump_data():
    global fram
    for n in range(0,(2048 * 8),2):
        bv = fram[n] + fram[n+1]
        if (n % 16 == 0):
            print ('')
        else: 
            print(',', end='')
        print (int.from_bytes(bv, 'big', False), end='')
    print('')
i2c = busio.I2C(board.SCL1, board.SDA1)
sensor = AS7341(i2c)
fram = adafruit_fram.FRAM_I2C(i2c)
fram_index = 0
sleep(60)
dump_data()
sleep(30)
while True:
    write_sensor()
    sleep(10)