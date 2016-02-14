
import sys
import unittest
from future.utils import isint
from pennyworth import util

class TestRandomInt(unittest.TestCase):
    def test_random_range(self):
        ret = util.get_random_id()
        self.assertTrue(1 <= ret <= 65535)

    def test_random_range2(self):
        ret = util.get_random_id()
        self.assertTrue(1 <= ret <= 65535)

class TestValidators(unittest.TestCase):
    def test_validate_int(self):
        ret = util.validate_int(100)
        self.assertTrue(isint(ret))

    def test_validate_int_from_str(self):
        ret = util.validate_int('100')
        self.assertTrue(isint(ret))

    def test_validate_int_from_bytes(self):
        ret = util.validate_int(b'100')
        self.assertTrue(isint(ret))

    def test_validate_not_int(self):
        with self.assertRaises(ValueError):
            util.validate_int(str)

    def test_validate_not_int_from_str(self):
        with self.assertRaises(ValueError):
            util.validate_int('a')

    def test_validate_not_int_from_bytes(self):
        with self.assertRaises(ValueError):
            util.validate_int(b'\xaa')

    def test_validate_bytes(self):
        ret = util.validate_bytes(b'\xaa\xbb')
        self.assertIsInstance(ret, bytes)

    def test_validate_bytes_from_bytearray(self):
        ret = util.validate_bytes(b'\xaa\xbb')
        self.assertIsInstance(ret, bytes)

    @unittest.skipIf(sys.version_info < (3,), 'Not applicable to python 2.x')
    def test_validate_not_bytes(self):
        with self.assertRaises(ValueError):
            util.validate_bytes(str)

    def test_validate_not_bytes_from_str(self):
        with self.assertRaises(ValueError):
            util.validate_bytes(u'\x99\x99')

class TestDecorators(unittest.TestCase):
    class FakeClient(object):
        def __init__(self):
            self._connected = False

        def _connect(self):
            self._connected = True

        def _disconnect(self):
            self._connected = False

        @util.disconnect
        def decorated_raise(self):
            raise ValueError()

        @util.disconnect
        def do_something(self):
            foo = 'bar'
            foo = list(foo)
            return foo

    def setUp(self):
        self.client = self.FakeClient()

    def test_disconnect(self):
        self.client._connect()
        self.client.do_something()
        self.assertFalse(self.client._connected)

    def test_disconnect_return(self):
        self.client._connect()
        ret = self.client.do_something()
        self.assertFalse(self.client._connected)
        self.assertEqual(ret, ['b', 'a', 'r'])

    def test_disconnect_not_connected(self):
        self.client.do_something()
        self.assertFalse(self.client._connected)

    def test_disconnect_raise(self):
        self.client._connect()
        with self.assertRaises(ValueError):
            self.client.decorated_raise()
        self.assertFalse(self.client._connected)
