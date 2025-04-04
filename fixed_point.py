"""Fixed point numbers

Created on 2025.04.04
@author: Jakub
"""


from typing import Self


class fix(object):
    def __init__(self, value: int=0):
        assert type(value) is int
        self.value = value

    def __repr__(self) -> str:
        return str(self.to_float())

    @staticmethod
    def epsilon():
        return fix(1)

    def _decimal(self):
        return self.value & 65535


    # conversion from types
    @staticmethod
    def from_int(val: int) -> Self:
        return fix(val << 16)

    def to_int(self) -> int:
        return self.value >> 16

    @staticmethod
    def from_float(val: float) -> Self:
        return fix(int(val*65536))

    def to_float(self) -> float:
        return self.to_int() + self._decimal()/65536


    # basic operations
    # addition
    def __add__(self, other: Self | int | float) -> Self:
        if type(other) is int:
            return fix(self.value + (other << 16))
        if type(other) is float:
            return fix(self.value + int(other*65536))
        return fix(self.value + other.value)

    def __radd__(self, other: Self | int | float) -> Self:
        return self + other

    # subtraction
    def __sub__(self, other: Self | int | float) -> Self:
        if type(other) is int:
            return fix(self.value - (other << 16))
        if type(other) is float:
            return fix(self.value - int(other*65536))
        return fix(self.value - other.value)

    def __rsub__(self, other: Self | int | float) -> Self:
        return self - other

    # multiplication
    def __mul__(self, other: Self | int | float) -> Self:
        if type(other) is int:
            return fix(self.value * other)
        if type(other) is float:
            return fix(int(self.value * other))
        return fix((self.value * other.value) >> 16)

    def __rmul__(self, other: Self | int | float) -> Self:
        return self * other

    # division
    def __truediv__(self, other: Self | int | float) -> Self:
        if type(other) is int or type(other) is float:
            return fix(int(self.value / other))
        return fix(int((self.value << 16) / other.value))

    def __rtruediv__(self, other: Self | int | float) -> Self:
        if type(other) is int:
            return fix.from_int(other) / self
        if type(other) is float:
            return fix.from_float(other) / self
        return fix(int((other.value << 16) / self.value))

    # absolute value
    def __abs__(self) -> Self:
        return fix(abs(self.value))


if __name__ == "__main__":
    x = fix.from_int(3)
    y = fix.from_float(5.125)
