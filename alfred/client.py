
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
import struct
import socket
from .util import get_random_id, validate_int, validate_bytes
from .packet import AlfredVersion, AlfredPacketType
from .exceptions import AlfredError

class AlfredClient(object):
    def __init__(self, sock='/var/run/alfred.sock'):
        self.sock_path = sock
        self._connected = False

    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX)
        self.sock.connect(self.sock_path)
        self._connected = True

    def send_recv(self, data, tx_id):
        if not self._connected:
            self.connect()
        self.sock.sendall(bytes(data))
        tlv_hdr = self.sock.recv(4)
        if not tlv_hdr:
            return None
        tlv_type = tlv_hdr[0]
        tlv_ver = tlv_hdr[1]
        tlv_len = struct.unpack('!H', tlv_hdr[2:4])[0]
        trans_hdr = self.sock.recv(4)
        trans_id = struct.unpack('!H', trans_hdr[0:2])[0]
        trans_seq = struct.unpack('!H', trans_hdr[2:4])[0]
        if tlv_type == AlfredPacketType.STATUS_TXEND:
            if trans_seq == 1:
                raise AlfredError('Error received from server')
        elif tlv_type != AlfredPacketType.PUSH_DATA or trans_id != tx_id:
            raise AlfredError('Invalid response received from server')
        recv_data = self.sock.recv(tlv_len-4)
        src_mac = recv_data[0:6]
        data_type = recv_data[6]
        data_ver = recv_data[7]
        data_len = struct.unpack('!H', recv_data[8:10])[0]
        data = recv_data[10:]
        if len(data) != data_len:
            raise AlfredError('Failed to receive all data from server. '
                'Received {} bytes. Should have received {}'.format(len(data),
                data_len))
        self.sock.close()
        src_mac = ':'.join(['{:02x}'.format(x) for x in src_mac])
        return src_mac, data

    def request_data(self, data_type):
        data_type = validate_int(data_type)
        request = bytearray([0 for _ in range(7)])
        tx_id = get_random_id()
        struct.pack_into('!B', request, 0, AlfredPacketType.REQUEST)
        struct.pack_into('!B', request, 1, AlfredVersion.v0)
        struct.pack_into('!H', request, 2, 3)
        struct.pack_into('!B', request, 4, data_type)
        struct.pack_into('!H', request, 5, tx_id)
        return self.send_recv(request, tx_id)

