
import miio
from miio import Device, DeviceException
import sys
import configparser

# Configuration file parsing
config = configparser.ConfigParser()
config.read('config.ini')

# Device information
DEVICE_IP = config['DEVICE']['IP']
DEVICE_TOKEN = config['DEVICE']['TOKEN']

# Initialize the device
try:
    device = miio.Device(DEVICE_IP, DEVICE_TOKEN)
except DeviceException:
    print("Failed to connect to the device. Check IP and token.")
    sys.exit(1)

def turn_on_light():
    """Turn on the Xiaomi Lite Light."""
    device.send('set_power', ['on'])

def turn_off_light():
    """Turn off the Xiaomi Lite Light."""
    device.send('set_power', ['off'])

def set_brightness(brightness):
    """Set the brightness of the light.
    
    Args:
        brightness (int): Brightness level (0-100).
    """
    device.send('set_bright', [brightness])

def get_status():
    """Get the current status of the light."""
    status = device.send('get_prop', ['power', 'bright'])
    return status

# Example usage
if __name__ == '__main__':
    turn_on_light()
    set_brightness(50)
    print(get_status())
    turn_off_light()
