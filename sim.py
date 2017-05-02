import json
import math
import paho.mqtt.client as MQTT
import random
import time

c = MQTT.Client()

new_device_x = None
new_device_y = None

class Sim(object):
    def __init__(self, lampis):
        self.lampis = lampis
        self.device_x = 5.0
        self.device_y = 1.0
        self.device_z = 1.0

    def change_device_location(self, x, y, z):
        self.device_x = x
        self.device_y = y
        self.device_z = z

    def update(self, device_x, device_y, device_z):
        for lampi in self.lampis:
            lampi.update(device_x, device_y, device_z)

    def run(self):
        while True:
            time.sleep(1.0) # secs
            print('Run simulation step. Actual position: <%.2f, %.2f, %.2f>' % (self.device_x, self.device_y, self.device_z,))
            global new_device_x
            global new_device_y
            global new_device_z
            if new_device_x is not None and new_device_y is not None and new_device_z:
                self.change_device_location(new_device_x, new_device_y, new_device_z)
                new_device_x = None
                new_device_y = None
                new_device_z = None
            self.update(self.device_x, self.device_y, self.device_z)

class Lampi(object):
    def __init__(self, device_id, client, x, y, z):
        self.device_id = device_id
        self.c = client
        self.x = x
        self.y = y
        self.z = z

    def rssi_from_distance(self, dist):
        '''
        RSSI = -10 * n * log_10(dist) + A

        -50 @ 1m, A = -50
        -56 @ 2m, etc.
        '''
        n = 2.3
        A = -50

        rssi = -10 * n * math.log10(dist) + A
        return rssi

    def publish_rssi(self, rssi):
        rssi += random.randint(-5, 5) # add +- 5 to rssi
        peripheral = {
            'id': 'Track this Device',
            'address': '',
            'addressType': '',
            'connectable': 'True',
            'advertisement': {
                'localName': '<name>',
                'txPowerLevel': 0,
                'serviceUuids': ['1234'],
                'serviceSolicitationUuid': [''],
                'manufacturerData': '',
                'serviceData': [
                    {
                        'uuid': '12345',
                        'data': ''
                    }
                ]
            },
            'rssi': rssi,
        }
        periph_json = json.dumps(peripheral)
        self.c.publish('/devices/' + self.device_id + '/rssi', periph_json)

    def update(self, device_x, device_y, device_z):
        dx = device_x - self.x
        dy = device_y - self.y
        dz = device_z - self.z

        dist = math.sqrt(dx * dx + dy * dy + dz * dz)
        rssi = self.rssi_from_distance(dist)
        # print('lampi update %s %s -> %s' % (self.device_id, dist, rssi,))
        self.publish_rssi(rssi)

if __name__ == '__main__':
    c.connect('localhost', port=1883, keepalive=60)
    s = Sim([
        Lampi('a', c, 0.0, 0.0, 0.0),
        Lampi('b', c, 0.0, 10.0, 0.0),
        Lampi('c', c, 5.0, 0.0, 0.0),
    ])
    c.loop_start()
    s.run()
    c.loop_stop()
