
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
import os
import struct
import socketserver

class FakeAlfred(socketserver.BaseRequestHandler):
    def handle(self):
        socket = self.request
        data = bytes(socket.recv(1024))
        if data[0] == 2:
            self.handle_request(data)
        elif data[0] == 0:
            self.handle_push(data)
        else:
            tx_id = b'\x00\x00'
            if len(data) >= 8:
                tx_id = data[5:7]
            self.send_error(tx_id)

    def handle_request(self, data):
        request_type = data[4]
        tx_id = data[5:7]
        src_mac = b'\xaa\xbb\xcc\xdd\xee\xff'
        data = b'\x01\x02\x03\x04\x05\x06'
        data_len = b'\x00\x06'
        resp_len = b'\x00\x14'
        resp_type = b'\x00'
        if request_type == 255:
            return
        elif request_type == 42:
            return self.send_error(tx_id)
        elif request_type == 66:
            # send back bad data length
            data_len = b'\x01\xff'
        elif request_type == 76:
            # send back bad response length
            resp_len = b'\x01\xff'
        elif request_type == 86:
            # send back bad tlv type
            resp_type = b'\x10'
        response = resp_type
        response += b'\x00'
        response += resp_len
        response += tx_id
        response += b'\x00\x00'
        response += src_mac
        response += struct.pack('!B', request_type)
        response += b'\x00'
        response += data_len
        response += data
        self.request.sendall(response)

    def handle_push(self, data):
        pass

    def send_error(self, tx_id):
        response = b'\x03\x00\x00\x04'
        response += tx_id
        response += b'\x00\x01'
        self.request.sendall(response)

if __name__ == "__main__":
    try:
        os.remove("./tmp.sock")
    except OSError:
        pass
    server = socketserver.UnixStreamServer('./tmp.sock', FakeAlfred)
    server.serve_forever()
