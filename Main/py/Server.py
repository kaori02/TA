from time import sleep
import bluetooth
import sys
import json
BUFFER = 1024
    
class Servers:
    def __init__(self):
        self.stop = False
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.bind(("",bluetooth.PORT_ANY))
        self.sock.listen(1)
        self.accept_connection()
        
    def receive(self):
        data = self.client.recv(BUFFER)
        if data:
            return data.decode()
        return ""

    def send(self,data):
        return self.client.send(data.encode())
    
    def accept_connection(self):
        self.port = self.sock.getsockname()[1]
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        bluetooth.advertise_service(self.sock, "Server", service_id=uuid,
                                    service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE])
        try:
            self.client, self.info = self.sock.accept()
        
        except Exception:
            self.close
                
    def close(self):
        self.client.close()
        self.sock.close()
        return

if __name__ == '__main__':
    server = Servers()
    while True:
      try:
        received = server.receive()

        if received.endswith("vincenty") or received.endswith("haversine"):
          splitted_data = received.split()
          destLat = splitted_data[0]
          destLon = splitted_data[1]
          currLat = splitted_data[2]
          currLon = splitted_data[3]

          print("destLat, destLon, currLat, currLon")
          print(str(destLat) + " " + str(destLon) + " " + str(currLat) + " " + str(currLon))

          with open("loc.json") as f:
            dataJSON = json.load(f)
          
          dataJSON["Dest"] = [float(destLat), float(destLon)]
          dataJSON["Home"] = [float(currLat), float(currLon)]

          with open("loc.json", "w") as f:
            json.dump(dataJSON, f)

        sleep(0.5)
      except KeyboardInterrupt:
        sys.exit

