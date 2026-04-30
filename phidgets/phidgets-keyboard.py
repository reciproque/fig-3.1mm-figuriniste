import time
from threading import Thread

# Import Phidget22 modules at the top level
# https://www.phidgets.com/docs/OS_-_Getting_Started

try:
    from Phidget22.Phidget import *
    from Phidget22.Devices.CapacitiveTouch import *
    phidgets_available = True
except ImportError:
    phidgets_available = False

# Import tkinter for the GUI mock
try:
    import tkinter as tk
    from tkinter import ttk
    tkinter_available = True
except ImportError:
    tkinter_available = False

# Import pynput for hotkey detection
try:
    from pynput import keyboard as pynput_keyboard
    pynput_available = True
except ImportError:
    pynput_available = False

# --- Configuration ---
use_mock = True  # Set to False to use real Phidget22 hardware

# --- Mock Phidgets Interface (GUI with buttons) ---
class MockPhidgetsInterface:
    def __init__(self, num_sensors=6):
        if not tkinter_available:
            raise ImportError("tkinter is not available. Install it or use a different mock.")
        self.num_sensors = num_sensors
        self.sensor_states = [False] * num_sensors
        self.listeners = []
        self.root = tk.Tk()
        self.root.title("Phidgets Mock Interface")
        self.create_buttons()
        if pynput_available:
            self.bind_keys()  # Bind keyboard keys to sensors

    def create_buttons(self):
        for i in range(self.num_sensors):
            button = ttk.Button(
                self.root,
                text=f"Sensor {i} (Key {chr(65 + i)})",  # A, B, C, D, E, F
                command=lambda i=i: self.simulate_touch(i)
            )
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="ew")

    def bind_keys(self):
        # Use pynput to listen for key presses
        def on_press(key):
            try:
                # Check if the key is a-f (lowercase or uppercase)
                if key.char.lower() in ['a', 'b', 'c', 'd', 'e', 'f']:
                    sensor_index = ord(key.char.lower()) - ord('a')
                    self.simulate_touch(sensor_index)
            except AttributeError:
                pass  # Ignore non-character keys

        # Start the listener in a non-blocking way
        listener = pynput_keyboard.Listener(on_press=on_press)
        listener.start()

    def add_listener(self, listener):
        self.listeners.append(listener)

    def simulate_touch(self, sensor_index):
        if 0 <= sensor_index < self.num_sensors:
            self.sensor_states[sensor_index] = True
            for listener in self.listeners:
                listener(sensor_index)
            self.root.after(100, lambda: self.reset_sensor(sensor_index))  # Reset after 100ms

    def reset_sensor(self, sensor_index):
        self.sensor_states[sensor_index] = False

    def start(self):
        print("Mock Phidgets Interface: Click the buttons or press a-f to simulate sensor touches.")
        self.root.mainloop()

# --- Real Phidget22 Interface (for deployment) ---
class Phidget22Interface:
    def __init__(self, num_sensors=6):
        if not phidgets_available:
            raise ImportError("Phidget22 library not found. Install it with: pip install Phidget22")
        self.num_sensors = num_sensors
        self.listeners = []
        self.capacitive_touch = CapacitiveTouch()
        self.capacitive_touch.setOnTouchHandler(self.on_touch)
        self.capacitive_touch.openWaitForAttachment(5000)

    def add_listener(self, listener):
        self.listeners.append(listener)

    def on_touch(self, channel, touched):
        if touched:
            sensor_index = channel.getIndex()
            for listener in self.listeners:
                listener(sensor_index)
            time.sleep(0.1)  # Debounce delay

    def start(self):
        print("Phidget22 Interface: Waiting for sensor touches...")
        while True:
            time.sleep(1)

# --- Keyboard Emulator ---
class KeyboardEmulator:
    def __init__(self, phidgets_interface):
        self.phidgets = phidgets_interface
        self.phidgets.add_listener(self.on_sensor_touched)

    def on_sensor_touched(self, sensor_index):
        key = str(sensor_index + 1)  # Map sensor 0 to key '1', etc.
        print(f"Sensor {sensor_index} touched. Pressing key: {key}")
        import pyautogui
        pyautogui.press(key)  # Use pyautogui to press the key

    def start(self):
        if isinstance(self.phidgets, MockPhidgetsInterface):
            self.phidgets.start()  # Run Tkinter in the main thread
        else:
            self.phidgets.start()  # Run Phidget22 in a thread

# --- Main Program ---
if __name__ == "__main__":
    # Initialize the appropriate interface
    if use_mock:
        if not tkinter_available:
            print("tkinter is not available. Falling back to console mock.")
            # Fallback to console mock if tkinter is not available
            class ConsoleMockPhidgetsInterface:
                def __init__(self, num_sensors=6):
                    self.num_sensors = num_sensors
                    self.sensor_states = [False] * num_sensors
                    self.listeners = []

                def add_listener(self, listener):
                    self.listeners.append(listener)

                def simulate_touch(self, sensor_index):
                    if 0 <= sensor_index < self.num_sensors:
                        self.sensor_states[sensor_index] = True
                        for listener in self.listeners:
                            listener(sensor_index)
                        time.sleep(0.1)
                        self.sensor_states[sensor_index] = False

                def start(self):
                    print("Console Mock Phidgets Interface: Press a-f to simulate sensor touches.")
                    if not pynput_available:
                        print("pynput is not available. Install it with: pip install pynput")
                        return

                    def on_press(key):
                        try:
                            if key.char.lower() in ['a', 'b', 'c', 'd', 'e', 'f']:
                                sensor_index = ord(key.char.lower()) - ord('a')
                                self.simulate_touch(sensor_index)
                        except AttributeError:
                            pass

                    listener = pynput_keyboard.Listener(on_press=on_press)
                    listener.start()
                    listener.join()  # Keep the listener running
            phidgets = ConsoleMockPhidgetsInterface(num_sensors=6)
        else:
            phidgets = MockPhidgetsInterface(num_sensors=6)
    else:
        if not phidgets_available:
            print("Phidget22 library not found. Install it with: pip install Phidget22")
            exit(1)
        try:
            phidgets = Phidget22Interface(num_sensors=6)
        except Exception as e:
            print(f"Error initializing Phidget22: {e}")
            exit(1)

    # Initialize keyboard emulator
    emulator = KeyboardEmulator(phidgets)

    # Start the emulator
    if isinstance(phidgets, MockPhidgetsInterface):
        # Run Tkinter in the main thread
        emulator.start()
    else:
        # Run Phidget22 in a separate thread
        emulator_thread = Thread(target=emulator.start)
        emulator_thread.daemon = True
        emulator_thread.start()

        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nExiting...")