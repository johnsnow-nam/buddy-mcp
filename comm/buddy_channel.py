#-*- coding:utf-8 -*-
import threading
import serial


class buddy_channel(threading.Thread):
    """Serial read loop and dispatch to Protocol. Thread-safe write."""

    def __init__(self, serial_instance, protocol_factory, packet_factory):
        super(buddy_channel, self).__init__()
        self.daemon = True
        self.serial = serial_instance
        self.protocol_factory = protocol_factory
        self.packet_factory = packet_factory
        self.alive = True
        self._lock = threading.Lock()
        self._connection_made = threading.Event()
        self.protocol = None
        self.packet = None

    def stop(self):
        self.alive = False
        if hasattr(self.serial, 'cancel_read'):
            self.serial.cancel_read()
        self.join(2)

    def run(self):
        if not hasattr(self.serial, 'cancel_read'):
            self.serial.timeout = 1
        self.protocol = self.protocol_factory()
        self.packet = self.packet_factory(
            self.protocol.data_received, self.protocol.write_packet
        )
        try:
            self.protocol.connection_made(self)
        except Exception as e:
            self.alive = False
            self.protocol.connection_lost(e)
            self._connection_made.set()
            return
        self._connection_made.set()
        error = None
        while self.alive and self.serial.is_open:
            try:
                data = self.serial.read(self.serial.in_waiting or 1)
            except serial.SerialException as e:
                error = e
                break
            else:
                if data:
                    try:
                        for ch in bytearray(data):
                            self.packet.add(ch)
                    except Exception as e:
                        error = e
                        break
        self.alive = False
        self.protocol.connection_lost(error)
        self.protocol = None

    def write(self, data):
        with self._lock:
            self.serial.write(data)

    def close(self):
        with self._lock:
            self.stop()
            self.serial.close()

    def __enter__(self):
        self.start()
        self._connection_made.wait()
        if not self.alive:
            raise RuntimeError('connection_lost already called')
        return self.protocol

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
