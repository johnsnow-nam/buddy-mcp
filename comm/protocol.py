#-*- coding:utf-8 -*-
class Protocol(object):
    """Protocol as used by the ReaderThread. Base class with empty implementations."""

    def connection_made(self, transport):
        """Called when reader thread is started"""
        pass

    def data_received(self, data):
        """Called with snippets received from the serial port"""
        pass

    def connection_lost(self, exc):
        """Called when the serial port is closed or the reader loop terminated."""
        if isinstance(exc, Exception):
            raise exc
