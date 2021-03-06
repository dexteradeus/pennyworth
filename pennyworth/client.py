
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
import struct
import socket
from .util import get_random_id, validate_int, validate_bytes, disconnect
from .packet import AlfredVersion, AlfredPacketType
from .exceptions import *

class AlfredClient(object):
    def __init__(self, sock='/var/run/alfred.sock'):
        self.sock_path = sock
        self._connected = False
        self.src_mac = bytes(6)

    def _connect(self):
        self.sock = socket.socket(socket.AF_UNIX)
        self.sock.connect(self.sock_path)
        self._connected = True

    def _disconnect(self):
        self.sock.close()
        self._connected = False

    def _send(self, data):
        if not self._connected:
            self._connect()
        self.sock.sendall(bytes(data))

    def _send_recv(self, data, tx_id):
        self._send(data)
        tlv_hdr = bytes(self.sock.recv(4))
        ret_data = {}
        while tlv_hdr:
            tlv_type = tlv_hdr[0]
            tlv_ver = tlv_hdr[1]
            tlv_len = struct.unpack('!H', tlv_hdr[2:4])[0]
            trans_hdr = bytes(self.sock.recv(4))
            trans_id = struct.unpack('!H', trans_hdr[0:2])[0]
            trans_seq = struct.unpack('!H', trans_hdr[2:4])[0]
            if tlv_type == AlfredPacketType.STATUS_TXEND:
                if trans_seq == 1:
                    raise AlfredError('Error received from server')
            elif tlv_type != AlfredPacketType.PUSH_DATA or trans_id != tx_id:
                raise AlfredInvalidResponse(
                    'Invalid response received from server')
            recv_data = bytes(self.sock.recv(tlv_len-4))
            src_mac = recv_data[0:6]
            data_type = recv_data[6]
            data_ver = recv_data[7]
            data_len = struct.unpack('!H', recv_data[8:10])[0]
            data = recv_data[10:]
            if len(data) != data_len:
                raise AlfredDataError('Failed to receive all data from server. '
                    'Received {} bytes. Should have received {}'
                    .format(len(data), data_len))
            src_mac = ':'.join(['{:02x}'.format(x) for x in src_mac])
            ret_data[src_mac] = data
            tlv_hdr = bytes(self.sock.recv(4))
        return ret_data

    @disconnect
    def request_data(self, data_type):
        """
        Request data from the Alfred server of the given data type

        Params:
        data_type : integer of the type of data requested (0-255)

        """
        data_type = validate_int(data_type)
        request = bytearray([0 for _ in range(7)])
        tx_id = get_random_id()
        struct.pack_into('!B', request, 0, AlfredPacketType.REQUEST)
        struct.pack_into('!B', request, 1, AlfredVersion.v0)
        struct.pack_into('!H', request, 2, 3)
        struct.pack_into('!B', request, 4, data_type)
        struct.pack_into('!H', request, 5, tx_id)
        return self._send_recv(request, tx_id)

    @disconnect
    def send_data(self, data_type, data, version=0):
        """
        Set data in the Alfred cloud for the given data type

        Params:
        data_type : integer of the type of data to be set (0-255)
        data : byte string of the data
        version : optional version to set for this data (default = 0)
        """
        data_type = validate_int(data_type)
        data = validate_bytes(data)
        data_len = len(data)
        update = bytearray([0 for _ in range(8)])
        tx_id = get_random_id()
        seq_num = 0
        struct.pack_into('!B', update, 0, AlfredPacketType.PUSH_DATA)
        struct.pack_into('!B', update, 1, AlfredVersion.v0)
        struct.pack_into('!H', update, 2, 14+data_len)
        struct.pack_into('!H', update, 4, tx_id)
        struct.pack_into('!H', update, 6, seq_num)
        payload = self.src_mac
        payload += struct.pack('!B', data_type)
        payload += struct.pack('!B', version)
        payload += struct.pack('!H', data_len)
        payload += data
        push_data = bytes(update) + payload
        self._send(push_data)
