
from enum import IntEnum

class AlfredVersion(IntEnum):
    v0 = 0

class AlfredPacketType(IntEnum):
    PUSH_DATA = 0
    ANNOUNCE_MASTER = 1
    REQUEST = 2
    STATUS_TXEND = 3
    STATUS_ERROR = 4
    MODESWITCH = 5
    CHANGE_INTERFACE = 6

class AlfredModeswitchType(IntEnum):
    SLAVE = 0
    MASTER = 1

