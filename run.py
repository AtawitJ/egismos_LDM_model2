from egismos_LDM_model2.laser_model2 import LaserController
import time

def main():
    com_port = input("Enter COM port for Laser (e.g., COM11): ").strip()
    laser = LaserController(com_port=com_port)
    laser.connect()
    if not laser.ser:
        print("Cannot proceed without connection. Exiting.")
        return

    laser.laser_on()
    print("Laser ON")
    time.sleep(1)

    single_result = laser.single_measure()
    print(f"Single measurement result: {single_result} meters")

    print("Starting continuous measurement for 5 seconds...")
    laser.start_continuous_measurement()
    start_time = time.time()
    while time.time() - start_time < 5:
        result = laser.get_result()
        if result is not None:
            print(f"Continuous measurement: {result} meters")
        time.sleep(0.5)

    laser.laser_off()
    print("Laser OFF")
    laser.close()

if __name__ == "__main__":
    main()
