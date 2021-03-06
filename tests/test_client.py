
import os
import sys
import unittest
import threading
import socketserver
from pennyworth import client
from pennyworth.exceptions import *
from .fake_server import FakeAlfred

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
sock_path = os.path.join(dir_path, 'tmp.sock')


class TestClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            os.remove(sock_path)
        except OSError:
            pass
        cls.server = socketserver.UnixStreamServer(sock_path, FakeAlfred)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server_thread.join()

    def setUp(self):
        self.client = client.AlfredClient(sock_path)

    def test_request(self):
        requested_data = self.client.request_data(153)
        self.assertEqual(len(requested_data), 1)
        expected_dict = {'aa:bb:cc:dd:ee:ff': b'\x01\x02\x03\x04\x05\x06'}
        self.assertDictEqual(requested_data, expected_dict)

    def test_request_no_data(self):
        requested_data = self.client.request_data(255)
        expected_dict = {}
        self.assertDictEqual(requested_data, expected_dict)

    def test_request_error(self):
        with self.assertRaises(AlfredError):
            self.client.request_data(42)

    def test_request_data_length_error(self):
        with self.assertRaises(AlfredDataError):
            self.client.request_data(66)

    def test_request_invalid_response(self):
        with self.assertRaises(AlfredInvalidResponse):
            self.client.request_data(86)
