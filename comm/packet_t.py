#-*- coding:utf-8 -*-
PS_STX = 0
PS_DATA = 1
PS_ESC = 2
MAX_PACKET_LEN = 1024
STX = 0x02
ETX = 0x03
ESC = 0x23
DLE = 0x40
DEFAULT_CRC = 0xff


class packet_t(object):
    def __init__(self, rx=None, tx=None):
        self.m_buffer = bytearray(MAX_PACKET_LEN)
        self.m_completion_handler = rx
        self.m_write_handler = tx
        self.reset()

    def reset(self):
        self.m_pos = 0
        self.m_state = PS_STX
        self.m_crc = DEFAULT_CRC

    def write_bytes(self, ch):
        if ch <= ETX:
            self.m_write_handler(bytearray([ESC]))
            ch = ch ^ DLE
            self.m_write_handler(bytearray([ch]))
        elif ch == ESC:
            self.m_write_handler(bytearray([ch]))
            self.m_write_handler(bytearray([ch]))
        else:
            self.m_write_handler(bytearray([ch]))

    def send_packet(self, buf, len_):
        if self.m_write_handler is None:
            return
        self.m_write_handler(bytearray([STX]))
        crc = DEFAULT_CRC
        i = 0
        while len_ != 0:
            len_ -= 1
            ch = buf[i]
            i += 1
            self.write_bytes(ch)
            crc ^= ch
        self.write_bytes(crc)
        self.m_write_handler(bytearray([ETX]))

    def add_data(self, ch):
        if self.m_pos >= MAX_PACKET_LEN:
            self.reset()
            return
        self.m_crc ^= ch
        self.m_buffer[self.m_pos] = ch
        self.m_pos += 1

    def add(self, ch):
        if ch == STX:
            self.reset()
        if self.m_state == PS_STX:
            self.m_state = PS_DATA
        elif self.m_state == PS_DATA:
            if ch == ETX:
                self.m_state = PS_STX
                if self.m_pos >= 2 and self.m_crc == 0:
                    self.m_pos -= 1
                    if self.m_completion_handler:
                        self.m_completion_handler(self.m_buffer, self.m_pos)
                    return
            elif ch == ESC:
                self.m_state = PS_ESC
            else:
                if ch < ETX:
                    self.reset()
                else:
                    self.add_data(ch)
        elif self.m_state == PS_ESC:
            if ch == ESC:
                self.m_state = PS_DATA
                self.add_data(ch)
            else:
                self.m_state = PS_DATA
                self.add_data(ch ^ DLE)
