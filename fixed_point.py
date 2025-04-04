"""Fixed point numbers

Created on 2025.04.04
@author: Jakub
"""


from typing import Self


class fixed(object):
    def __init__(self, value=0, _is_fixed=False):
        if _is_fixed:
            assert type(value) is int
            self.value = value
            return
        elif value == 0:
            self.value = 0
            return

        match value:
            case int():
                self.value = value << 16
            case float():
                self.value = int(value*65536)
            case str():
                self.value = int(float(value) * 65536)
            case fixed():
                # I know it looks weird
                self.value = value.value
            case _:
                raise TypeError(f"{type(value)} can't be interpreted as a fixed point number")

    def __repr__(self) -> str:
        # return f"{self.value >> 16}{str(self._decimal/65536)[1:]}"
        return str(float(self))

    @staticmethod
    def epsilon():
        return fixed(1, True)

    @property
    def _decimal(self):
        return self.value & 65535


    # conversion to other types
    def __int__(self) -> int:
        return self.value >> 16

    def __float__(self) -> float:
        return self.value/65536


    # basic operations
    # addition
    def __add__(self, other) -> Self:
        if type(other) is not fixed:
            return self + fixed(other)
        else:
            return fixed(self.value + other.value, True)

    def __radd__(self, other) -> Self:
        return fixed(other) + self

    # subtraction
    def __sub__(self, other) -> Self:
        if type(other) is not fixed:
            return self - fixed(other)
        else:
            return fixed(self.value - other.value, True)

    def __rsub__(self, other) -> Self:
        return fixed(other) - self

    # multiplication
    def __mul__(self, other) -> Self:
        if type(other) is not fixed:
            return self * fixed(other)
        else:
            # The bits need to be shifted right because of math reasons
            return fixed((self.value * other.value) >> 16, True)

    def __rmul__(self, other: Self | int | float) -> Self:
        return fixed(other) * self

    # division
    def __truediv__(self, other) -> Self:
        if type(other) is not fixed:
            return self / fixed(other)
        else:
            return fixed((self.value << 16) // other.value, True)

    def __rtruediv__(self, other: Self | int | float) -> Self:
        return fixed(other) / self

    # power
    def __pow__(self, power: int) -> Self:
        assert type(power) is int

        if power == 0:
            return fixed.from_int(1)

        elif power > 0:
            result = 1
            for i in range(power):
                result *= self
            return result

        else:
            result = 1
            for i in range(-1, power, -1):
                result /= self
            return result

    # absolute value
    def __abs__(self) -> Self:
        return fixed(abs(self.value), True)


if __name__ == "__main__":
    x = fixed(3)
    y = fixed(5.125)
