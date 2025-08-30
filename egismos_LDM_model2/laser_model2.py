import serial
import threading
import time
import re

class LaserController:
    def __init__(self, com_port: str, baudrate: int = 9600):
        self.com_port = com_port
        self.baudrate = baudrate
        self.ser = None
        self.is_running = False
        self.result = None
        self.lock = threading.Lock()
        self.thread = None

        # LDM Commands
        self.laser_OFF = bytes([0xAA, 0x00, 0x43, 0x43, 0xA8])
        self.laser_ON = bytes([0xAA, 0x00, 0x42, 0x42, 0xA8])
        self.single = bytes([0xAA, 0x00, 0x44, 0x44, 0xA8])
        self.con = bytes([0xAA, 0x00, 0x45, 0x45, 0xA8])
        self.stopcon = bytes([0xAA, 0x00, 0x46, 0x46, 0xA8])

    def connect(self):
        try:
            self.ser = serial.Serial(self.com_port, baudrate=self.baudrate, timeout=1)
            self.laser_off()
            time.sleep(0.5)
            print(f"Laser connected successfully on {self.com_port}")
        except serial.SerialException as e:
            print(f"Failed to connect to {self.com_port}: {e}")
            self.ser = None

    def laser_on(self):
        if self.ser and self.ser.is_open:
            self.ser.write(self.laser_ON)

    def laser_off(self):
        if self.ser and self.ser.is_open:
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            self.ser.write(self.laser_OFF)

    def stop_con(self):
        if self.ser and self.ser.is_open:
            self.ser.write(self.stopcon)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()

    def read_loop(self):
        while self.is_running and self.ser:
            try:
                with self.lock:
                    data = self.ser.read_all()
                if data:
                    self.process_data(data)
            except Exception as e:
                print(f"Error reading data: {e}")
            time.sleep(0.5)

    def start_continuous_measurement(self):
        if not self.ser or not self.ser.is_open:
            print("Device not connected!")
            return
        self.is_running = True
        self.thread = threading.Thread(target=self.read_loop, daemon=True)
        self.thread.start()
        self.ser.write(self.con)

    def single_measure(self):
        if not self.ser or not self.ser.is_open:
            print("Device not connected!")
            return None
        self.laser_off()
        time.sleep(0.2)
        self.ser.write(self.single)
        time.sleep(0.2)
        data = self.ser.read_all()
        return self.process_data(data)

    def process_data(self, data):
        for i, byte in enumerate(data):
            if byte == 0x44 and i + 6 < len(data):
                raw = data[i + 1:i + 7]
                try:
                    decoded = raw.decode('utf-8')
                    numeric = re.sub(r'\D', '', decoded)
                    if numeric.isdigit():
                        result = int(numeric) / 1000
                        with self.lock:
                            self.result = result
                        return result
                except UnicodeDecodeError:
                    continue
        with self.lock:
            self.result = None
        return None

    def get_result(self):
        with self.lock:
            return self.result

    def close(self):
        self.is_running = False
        if self.thread:
            self.thread.join()
        if self.ser and self.ser.is_open:
            self.ser.close()
        print("LaserController closed.")
