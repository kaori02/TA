from math import cos, sin, sqrt, pow, radians, tan, atan, atan2, degrees
import olympe
from drone.droneState import DroneState
from olympe.messages.ardrone3.PilotingSettings import MaxTilt
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, PCMD, CancelMoveBy
from olympe.messages.move import extended_move_by
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from olympe.messages.ardrone3.GPSSettingsState import HomeChanged
from olympe.messages.ardrone3.PilotingState import PositionChanged
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged
from Log import Log
from datetime import datetime

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
        logger.warning(f"extended move called with front {front}, right {right}, down {down}")
        if self.state == DroneState.TAKEOFF:
            assert self.drone(
                extended_move_by(front, right, down, 0.0, 0.8, 0.8, 0.0)
                # >> FlyingStateChanged(state="hovering", _timeout=10)
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
    
    def move_PCMD(self, right, front, up):
        # flag (u8) – Boolean flag: 1 if the ROLL and PITCH values should be taken in consideration. 0 otherwise

        # roll (i8) – Roll angle as signed percentage. On copters: Roll angle expressed as signed percentage of the max pitch/roll setting, in range [-100, 100] 
        #     -100 corresponds to a roll angle of max pitch/roll to the LEFT (drone will fly left) 
        #     100 corresponds to a roll angle of max pitch/roll to the [RIGHT] (drone will fly right) 
        #     This value may be clamped if necessary, in order to respect the maximum supported physical tilt of the copter.

        # pitch (i8) – Pitch angle as signed percentage. On copters: Expressed as signed percentage of the max pitch/roll setting, in range [-100, 100] 
        #     -100 corresponds to a pitch angle of max pitch/roll towards sky (drone will fly backward)
        #     100 corresponds to a pitch angle of max pitch/roll towards ground (drone will fly FORWARD) 
        #     This value may be clamped if necessary, in order to respect the maximum supported physical tilt of the copter. 

        # yaw (i8) – Yaw rotation speed as signed percentage. On copters: Expressed as signed percentage of the max yaw rotation speed setting, in range [-100, 100]. 
        #     -100 corresponds to a counter-clockwise rotation of max yaw rotation speed 
        #     100 corresponds to a clockwise rotation of max yaw rotation speed 
        #     This value may be clamped if necessary, in order to respect the maximum supported physical tilt of the copter.

        # gaz (i8) – Throttle as signed percentage. On copters: Expressed as signed percentage of the max vertical speed setting, in range [-100, 100] 
        #     -100 corresponds to a max vertical speed towards ground 
        #     100 corresponds to a max vertical speed towards sky 
        #     This value may be clamped if necessary, in order to respect the maximum supported physical tilt of the copter. 
        #     During the landing phase, putting some positive gaz will cancel the land. 

        # timestampAndSeqNum (u32) – Command timestamp in milliseconds (low 24 bits) + command sequence number (high 8 bits) [0;255].
        logger.warning(f"calling PCMD with right {right}, front {front}, up {up}")
        if self.state == DroneState.TAKEOFF:
            self.drone(PCMD(1, right, front, 0, up, timestampAndSeqNum=0))
    
    def cancel(self):
        logger.warning(f"calling cancel")
        if self.state == DroneState.TAKEOFF:
            self.drone(CancelMoveBy())
    
    def cancel_PCMD(self):
        logger.warning(f"calling cancel PCMD")
        if self.state == DroneState.TAKEOFF:
            self.drone(PCMD(1, 0, 0, 0, 0, timestampAndSeqNum=0))

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

    def writeCurrentPosition(self):
        coordinate = self.getPosition()
        if coordinate['latitude'] != 500.0 and coordinate['longitude'] != 500.0:
          self.write("{}: {},{}\n".format(datetime.now(), coordinate['latitude'], coordinate['longitude']))
