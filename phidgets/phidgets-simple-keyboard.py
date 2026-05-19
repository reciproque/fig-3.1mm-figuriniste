from Phidget22.Devices.DigitalInput import DigitalInput
from Phidget22.Phidget import Phidget
import keyboard

# Configuration des entrées numériques
digital_inputs = [DigitalInput() for _ in range(5)]
# Associe chaque entrée à une touche du clavier (ex: 1, 2, 3, 4, 5)
keys = ['1', '2', '3', '4', '5']

def on_state_change(self, state):
    index = digital_inputs.index(self)
    key = keys[index]
    if state:  # Si l'entrée passe à True (appui)
        keyboard.press(key)
    else:      # Si l'entrée passe à False (relâchement)
        keyboard.release(key)

# Configuration de chaque entrée
for i, di in enumerate(digital_inputs):
    di.setDeviceSerialNumber(YourDeviceSerialNumber)  # Remplacez par le numéro de série de votre Phidget
    di.setChannel(i)  # Canal 0 à 4
    di.setOnStateChangeHandler(on_state_change)
    di.openWaitForAttachment(5000)

print("Appuyez sur Ctrl+C pour arrêter...")
try:
    while True:
        pass
except KeyboardInterrupt:
    for di in digital_inputs:
        di.close()
    print("Fermeture des entrées...")