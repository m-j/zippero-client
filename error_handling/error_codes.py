from enum import Enum, unique


@unique
class ErrorCodes(Enum):
    GENERAL = 1
    PACKAGE_ALREADY_EXISTS = 2
    PACKAGE_DOESNT_EXIST = 3
    MALICIOUS_DATA = 4
    UNAUTHORIZED = 5