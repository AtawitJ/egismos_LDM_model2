# egismos_LDM_model2

Python module for controlling **Egismos LDM-2M-100-RS** (Laser Distance Module, Version 2) via USB serial.

## Installation

```bash
git clone https://github.com/YourUsername/egismos_LDM_model2.git
cd egismos_LDM_model2
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Usage

Run the example script:

```bash
python run.py
```

You will be prompted to enter the COM port of your laser module (e.g., `COM11`).

- **Single Measurement:** Returns a single distance reading in meters.
- **Continuous Measurement:** Reads continuously and updates distance in real-time.
- **Laser ON/OFF:** Controlled automatically in the script.

## License

MIT License
