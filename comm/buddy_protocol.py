#-*- coding:utf-8 -*-
from comm.protocol import Protocol

UDP = 0x30
CMD_EXECUTE = 0x01


class BuddyProtocol(Protocol):
    def __init__(self):
        self.dc1 = 0
        self.dc2 = 0
        self.sv1 = 0
        self.sv2 = 0
        self.v3 = 0
        self.v5 = 0
        self.io1 = 0
        self.io2 = 0
        self.io3 = 0
        self.io4 = 0
        self.ultra = 0
        self.line1 = 0
        self.line2 = 0
        self.running = True
        self.transport = None

    def decideToUseSensor(self, ultra, line1, line2):
        self.ultra = ultra
        self.line1 = line1
        self.line2 = line2
        self.sendDeviceData()

    def connection_made(self, transport):
        self.transport = transport
        self.running = True

    def connection_lost(self, exc):
        self.transport = None
        self.running = False

    def data_received(self, data, len_):
        pass  # optional: parse device state from data

    def write(self, data, len_):
        self.transport.packet.send_packet(data, len_)

    def write_packet(self, data):
        self.transport.write(data)

    def isDone(self):
        return self.running

    def sendIO(self, which_io, value):
        if which_io == "3V":
            self.v3 = value
        elif which_io == "5V":
            self.v5 = value
        elif which_io == "IO1":
            self.io1 = value
        elif which_io == "IO2":
            self.io2 = value
        elif which_io == "IO3":
            self.io3 = value
        elif which_io == "IO4":
            self.io4 = value
        self.sendDeviceData()

    def sendDC(self, dc1, dc2):
        self.dc1 = dc1
        self.dc2 = dc2
        self.sendDeviceData()

    def sendServo(self, sv1, sv2):
        self.sv1 = sv1
        self.sv2 = sv2
        self.sendDeviceData()

    def sendDeviceData(self):
        buffer = bytearray(15)
        buffer[0] = UDP
        buffer[1] = CMD_EXECUTE
        buffer[2] = self.dc1
        buffer[3] = self.dc2
        buffer[4] = self.sv1
        buffer[5] = self.sv2
        buffer[6] = self.v3
        buffer[7] = self.v5
        buffer[8] = self.io1
        buffer[9] = self.io2
        buffer[10] = self.io3
        buffer[11] = self.io4
        buffer[12] = self.ultra
        buffer[13] = self.line1
        buffer[14] = self.line2
        self.write(buffer, 15)
