import math
import time

new_device_x = None
new_device_y = None

class Sim(object):
    def __init__(self, lampis):
        self.lampis = lampis
        self.device_x = 5.0
        self.device_y = 5.0

    def change_device_location(self, x, y):
        self.device_x = x
        self.device_y = y

    def update(self, device_x, device_y):
        for lampi in lampis:
            lampi.update(device_x, device_y)

    def run(self):
        while True:
            time.sleep(1.0) # secs
            if new_device_x is not None and new_device_y is not None:
                self.change_device_location(new_device_x, new_device_y)
                new_device_x = None
                new_device_y = None
            self.update(self.device_x, self.device_y)

class Lampi(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rssi_from_distance(self, dist):
        '''
        RSSI = -10 * n * log_10(dist) + A

        -50 @ 1m, A = -50
        -56 @ 2m, etc.
        '''
        n = 2.3
        A = -50

        return -10 * n * math.log10(dist) + A

    def update(self, device_x, device_y):
        dx = device_x - self.x
        dy = deivce_y - self.y

        dist = math.sqrt(dx * dx + dy * dy)
