from math import cos, sin, sqrt, pow, radians, tan, atan, atan2, degrees
import olympe
from drone.droneState import DroneState
from olympe.messages.ardrone3.PilotingSettings import MaxTilt
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing
from olympe.messages.move import extended_move_by
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from olympe.messages.ardrone3.GPSSettingsState import HomeChanged
from olympe.messages.ardrone3.PilotingState import PositionChanged
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged
from Log import Log

logger = Log()

class Drone():
    state = DroneState.LAND
    r2 = 6371008.77141
    atDest = False
    # log untuk mencatat koordinat titik takeoff dan landing drone
    FILE = "/home/kaoripi/TA/Main/coordinate/coordinate.txt"
    
    def __init__(self, ip):
        self.DRONE_IP = ip
        self.drone = olympe.Drone(self.DRONE_IP)

    def write(self, text):
        # fungsi untuk mencatat log
        with open(self.FILE, 'a') as f:
            f.write(text)

    def connectToDrone(self):
        self.drone.connect()

    def setMaxTilt(self, tilt):
        self.drone(MaxTilt(1)).wait().success()

    def waitGPSFix(self):
        # fungsi untuk menunggu gps di drone siap untuk digunakan
        self.drone(GPSFixStateChanged(_policy = 'wait'))
    
    def getPosition(self):
        # fungsi untuk mendapatkan koordinat lokasi drone
        if self.state == DroneState.LAND:
            return self.drone.get_state(HomeChanged)
        elif self.state == DroneState.TAKEOFF:
            return self.drone.get_state(PositionChanged)

    def takeoff(self):
        if self.state == DroneState.LAND:
            assert self.drone(
                TakeOff()
                >> FlyingStateChanged(state="hovering", _timeout=10)
            ).wait().success()
            self.state = DroneState.TAKEOFF
            self.write("Takeoff...\n")

    def ext_move(self, front, right, down):
        # extended_move_by(d_x, d_y, d_z, d_psi, max_horizontal_speed, max_vertical_speed, max_yaw_rotation_speed, _timeout=10, _no_expect=False, _float_tol=(1e-07, 1e-09))
        # d_x (float) – Wanted displacement along the FRONT axis [m]
        # d_y (float) – Wanted displacement along the RIGHT axis [m]
        # d_z (float) – Wanted displacement along the DOWN axis [m]
        # d_psi (float) – Wanted ROTATION of heading [rad]
        # max_horizontal_speed (float) – Maximum horizontal speed in m/s.
        # max_vertical_speed (float) – Maximum vertical speed in m/s.
        # max_yaw_rotation_speed (float) – Maximum yaw rotation speed in degrees/s.

        if self.state == DroneState.TAKEOFF:
            assert self.drone(
                extended_move_by(front, right, down, 0.0, 0.7, 0.7, 0.5)
                >> FlyingStateChanged(state="hovering", _timeout=10)
            ).wait().success()

    def move(self, front, right, down):
        # moveBy(dX, dY, dZ, dPsi, _timeout=10, _no_expect=False, _float_tol=(1e-07, 1e-09))
        # dX (float)   – Wanted displacement along the FRONT axis [m]
        # dY (float)   – Wanted displacement along the RIGHT axis [m]
        # dZ (float)   – Wanted displacement along the DOWN axis [m]
        # dPsi (float) – Wanted rotation of heading [rad]

        if self.state == DroneState.TAKEOFF:
            assert self.drone(
                moveBy(front, right, down, 0)
                >> FlyingStateChanged(state="hovering", _timeout=10)
            ).wait().success()
    
    def moveTo(self, dist, altitude):
        # fungsi untuk menggerakan drone, fungsi ini di sdk parrot bernama "moveBy" dan
        # memiliki 4 parameter, yaitu moveBy(maju_mundur, kanan_kiri, atas_bawah, memutar drone sebesar x derajat)
        if self.state == DroneState.TAKEOFF:
            assert self.drone(
                moveBy(dist, 0, altitude, 0)
                >> FlyingStateChanged(state="hovering", _timeout=10)
            ).wait().success()
    
    def rotate(self, deg):
        # fungsi memutar drone, sebenarnya fungsi yang digunakan sama persis dengan fungsi moveTo, namun 
        # saya bedakan supaya lebih mudah dipahami
        if self.state == DroneState.TAKEOFF:
            assert self.drone(
                moveBy(0, 0, 0, radians(deg))
                >> FlyingStateChanged(state="hovering", _timeout=10)
            ).wait().success()
    
    def land(self):
        if self.state == DroneState.TAKEOFF:
            assert self.drone(
                Landing()
                >> FlyingStateChanged(state="landed", _timeout=10)
            ).wait().success()
            self.state = DroneState.LAND
            self.write("Landing...\n")

    def disconnectFromDrone(self):
        self.drone.disconnect()

    def vincenty_formula(self, latitude1, longitude1, latitude2, longitude2):
        #fungsi menghitung jarak drone dengan titik tujuan
        numerator = ( (cos(latitude2) * sin(longitude2-longitude1)) * (cos(latitude2) * sin(longitude2-longitude1)) ) + ( (cos(latitude1) * sin(latitude2) - sin(latitude1) * cos(latitude2) * cos(longitude2-longitude1)) * (cos(latitude1) * sin(latitude2) - sin(latitude1) * cos(latitude2) * cos(longitude2-longitude1)))
        denominator = sin(latitude1) * sin(latitude2) + cos(latitude1) * cos(latitude2) * cos(longitude2-longitude1)
        distance = self.r2 * atan(sqrt(numerator)/denominator)
        return distance
    
    def calculateBearing(self, init, dest):
        dL = dest[1] - init[1]
        x = cos(dest[0]) * sin(dL)
        y = cos(init[0]) * sin(dest[0]) - sin(init[0]) * cos(dest[0]) * cos(dL)
        return atan2(x,y)    
    
    def calculateDistance(self, latitude2, longitude2):
        start = []
        dest = [latitude2, longitude2]
        count = 0

        coordinate = self.getPosition()
        start.append(coordinate['latitude'])
        start.append(coordinate['longitude'])
        
        print(start)
       
        if start[0] != 500.0 and start[1] != 500.0:
            self.write("{},{}\n".format(start[0], start[1]))
            logger.warning("{},{}\n".format(start[0], start[1]))

        distance = self.vincenty_formula(radians(start[0]), radians(start[1]), radians(dest[0]), radians(dest[1]))
        bearing = self.calculateBearing(start, dest)
        normalizeBearing = (degrees(bearing) + 360) % 360
        return distance, normalizeBearing
