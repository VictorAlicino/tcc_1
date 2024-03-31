import json

class device:
    def __init__(self, sheet: json):
        self.id = sheet['id']
        self.room_id = sheet['room_id']
        self.name = sheet['device_name']
        self.connected_ssid = sheet['network']['ssid']
        self.bssid = sheet['network']['bssid']
        self.vendor = sheet['vendor']
        self.model = sheet['model']
        self.driver = sheet['driver']

    def do_something(self):
        print(f"Device {self.id} is doing something...")
