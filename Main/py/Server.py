import bluetooth

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
