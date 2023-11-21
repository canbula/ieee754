from decimal import Decimal, getcontext


class IEEE754:
    """
    IEEE 754 Floating Point Representation
    https://en.wikipedia.org/wiki/IEEE_754

    Author: Bora Canbula
    Email: bora.canbula@cbu.edu.tr
    Link: https://github.com/canbula/ieee754

    Parameters
    ----------
    number : str
        Floating point number to be converted.
    precision : int, optional
        Precision of the number, by default 2
    force_exponent : int, optional
        Force the exponent bits, by default None
    force_mantissa : int, optional
        Force the mantissa bits, by default None

    Returns
    -------
    IEEE754
        IEEE 754 representation of the number
    """

    def __init__(
        self,
        number: str = "0.0",
        precision: int = 2,
        force_exponent: int = None,
        force_mantissa: int = None,
    ) -> None:
        getcontext().prec = 256
        self.precision: int = precision
        exponent_list: list[int] = [5, 8, 11, 15, 19]
        mantissa_list: list[int] = [10, 23, 52, 112, 236]
        self.__exponent: int = (
            force_exponent
            if force_exponent is not None
            else exponent_list[self.precision]
        )
        self.__mantissa: int = (
            force_mantissa
            if force_mantissa is not None
            else mantissa_list[self.precision]
        )
        self.output: dict = {
            "number": "",
            "edge_case": False,
            "sign_bit": "",
            "exponent_bits": "",
            "mantissa_bits": "",
            "total_bits": "",
            "sign": "",
            "scale": "",
            "scaled_number": "",
            "scaled_number_in_binary": "",
            "unable_to_scale": False,
            "bias": "",
            "exponent": "",
            "mantissa": "",
            "result": "",
            "hexadecimal": "",
            "hexadecimal_parts": [],
            "converted_number": "",
            "error": "",
        }
        self.__bias: int = 2 ** (self.__exponent - 1) - 1
        self.__edge_case: str = None
        self.number: Decimal = self.validate_number(number)
        self.original_number: Decimal = self.number
        if self.__edge_case is None:
            self.sign: str = self.find_sign()
            self.number = self.number.copy_abs()
            self.__scale, self.number = self.scale_up_to_integer(self.number, 2)
            self.binary: str = f"{self.number:b}"
            self.binary_output: str = (
                f"{self.binary[:-self.__scale]}.{self.binary[-self.__scale:]}"
            )
            self.exponent = self.find_exponent()
            self.mantissa = self.find_mantissa()
            self.converted_number, self.error = self.back_to_decimal_from_bits()

    def validate_number(self, number: str) -> Decimal:
        if number == "":
            number = "0.0"
        if Decimal(number).is_infinite():
            if Decimal(number) > 0:
                # +inf: 0 11111111 00000000000000000000000
                self.sign = "0"
                self.exponent = f"{'1' * self.__exponent}"
                self.mantissa = f"{'0' * self.__mantissa}"
                self.__edge_case = f"{self.sign} {self.exponent} {self.mantissa}"
                return Decimal("Infinity")
            # -inf: 1 11111111 00000000000000000000000
            self.sign = "1"
            self.exponent = f"{'1' * self.__exponent}"
            self.mantissa = f"{'0' * self.__mantissa}"
            self.__edge_case = f"{self.sign} {self.exponent} {self.mantissa}"
            return Decimal("-Infinity")
        if Decimal(number).is_nan() and Decimal(number).is_snan():
            # snan: 0 11111111 00000000000000000000001
            self.sign = "0"
            self.exponent = f"{'1' * self.__exponent}"
            self.mantissa = f"{'0' * (self.__mantissa - 1)}1"
            self.__edge_case = f"{self.sign} {self.exponent} {self.mantissa}"
            return Decimal("NaN")
        if Decimal(number).is_nan() and Decimal(number).is_qnan():
            # qnan: 0 11111111 10000000000000000000000
            self.sign = "0"
            self.exponent = f"{'1' * self.__exponent}"
            self.mantissa = f"1{'0' * (self.__mantissa - 1)}"
            self.__edge_case = f"{self.sign} {self.exponent} {self.mantissa}"
            return Decimal("NaN")
        if not number == number:
            # nan: 0 11111111 11111111111111111111111
            self.sign = "0"
            self.exponent = f"{'1' * self.__exponent}"
            self.mantissa = f"{'1' * self.__mantissa}"
            self.__edge_case = f"{self.sign} {self.exponent} {self.mantissa}"
            return Decimal("NaN")
        if Decimal(number) == 0:
            if Decimal(number).is_signed():
                # -0: 1 00000000 00000000000000000000000
                self.sign = "1"
                self.exponent = f"{'0' * self.__exponent}"
                self.mantissa = f"{'0' * self.__mantissa}"
                self.__edge_case = f"{self.sign} {self.exponent} {self.mantissa}"
            else:
                # +0: 0 00000000 00000000000000000000000
                self.sign = "0"
                self.exponent = f"{'0' * self.__exponent}"
                self.mantissa = f"{'0' * self.__mantissa}"
                self.__edge_case = f"{self.sign} {self.exponent} {self.mantissa}"
            return Decimal("0")
        if isinstance(number, int):
            number = f"{number}.0"
        if not isinstance(number, str):
            number = str(number)
        try:
            number = Decimal(number)
        except:
            raise ValueError(f"Invalid number: {number}")
        denormalized_range = self.calculate_denormalized_range(
            self.__exponent, self.__mantissa
        )
        if Decimal(number).copy_abs() < Decimal(denormalized_range[0]):
            raise ValueError(
                f"Number is too small, must be larger than {denormalized_range[0]}, we lost both exponent and mantissa, please increase precision."
            )
        if Decimal(number).copy_abs() < Decimal(denormalized_range[1]):
            raise ValueError(
                f"Number is too small, must be larger than {denormalized_range[1]}, we lost exponent, please increase precision."
            )
        return number

    @staticmethod
    def calculate_denormalized_range(exponent_bits: int, mantissa_bits: int) -> tuple:
        bias = 2 ** (exponent_bits - 1) - 1
        smallest_normalized = 2 ** -(bias - 1)
        smallest_denormalized = smallest_normalized * 2**-mantissa_bits
        largest_denormalized = smallest_normalized - 2 ** -(bias + mantissa_bits - 1)

        return (smallest_denormalized, largest_denormalized)

    def find_sign(self) -> str:
        if self.number < 0:
            return "1"
        return "0"

    def scale_up_to_integer(self, number: Decimal, base: int) -> (int, int):
        scale = 0
        while number != int(number):
            number *= base
            scale += 1
        self.output["unable_to_scale"] = scale > 100
        return scale, int(number)

    def find_exponent(self) -> str:
        exponent = len(self.binary) - 1 + self.__bias - self.__scale
        return f"{exponent:0{self.__exponent}b}"

    def find_mantissa(self) -> str:
        mantissa = f"{self.binary[1:]:<0{self.__mantissa}}"
        if len(mantissa) > self.__mantissa:
            mantissa = f"{mantissa[: self.__mantissa - 1]}1"
        return mantissa

    def __str__(self) -> str:
        if self.__edge_case is not None:
            return self.__edge_case
        return f"{self.sign} {self.exponent} {self.mantissa}"

    def hex(self) -> (str, list[str]):
        h = ""
        hex_parts = []
        s = str(self).replace(" ", "")
        if len(s) % 4 != 0:
            next_multiple = (len(s) // 4 + 1) * 4
            s = "0" * (next_multiple - len(s)) + s
        limit = len(s) - (len(s) % 4)
        for i in range(0, limit, 4):
            ss = s[i : i + 4]
            si = 0
            for j in range(4):
                si += int(ss[j]) * (2 ** (3 - j))
            hex_parts.append(ss)
            sh = hex(si)
            h += sh[2]
        return h.upper(), hex_parts

    def json(self) -> dict:
        return self.produce_output()

    def __repr__(self) -> str:
        return self.__str__()

    def produce_output(self) -> dict:
        self.output["number"] = self.original_number
        self.output["sign_bit"] = "1"
        self.output["exponent_bits"] = self.__exponent
        self.output["mantissa_bits"] = self.__mantissa
        self.output["total_bits"] = 1 + self.__exponent + self.__mantissa
        self.output["sign"] = self.sign
        self.output["exponent"] = self.exponent
        self.output["mantissa"] = self.mantissa
        self.output["bias"] = self.__bias
        self.output["hexadecimal"], self.output["hexadecimal_parts"] = self.hex()
        self.output["result"] = self.__str__()
        if self.__edge_case is None:
            self.output["scale"] = self.__scale
            self.output["scaled_number"] = self.number
            self.output["scaled_number_in_binary"] = self.binary
            (
                self.output["converted_number"],
                self.output["error"],
            ) = self.back_to_decimal_from_bits()
        else:
            self.output["edge_case"] = True
        return self.output

    def back_to_decimal_from_bits(self) -> (Decimal, Decimal):
        """
        Returns
        -------
        Decimal
            Decimal representation of the number
        """
        sign, exponent, mantissa = self.__str__().split(" ")
        sign = (-1) ** int(sign)
        exponent = int(exponent, 2) - self.__bias
        mantissa = int(mantissa, 2)
        number = Decimal(sign * (1 + mantissa * 2**-self.__mantissa) * 2**exponent)
        error = Decimal(self.original_number - number).copy_abs()
        return number, error


def half(x: str) -> IEEE754:
    """
    IEEE 754 Half Precision Representation

    Parameters
    ----------
    x : str
        Floating point number to be converted.

    Returns
    -------
    IEEE754
        IEEE 754 representation of the number

    Examples
    --------
    >>> half(13.375)
    0 10010 1010110000

    >>> half(13.375).hex()
    4AB0

    >>> half(13.375).json()
    {'exponent-bits': 5, 'mantissa-bits': 10, 'bias': 15, 'sign': '0', 'exponent': '10010', 'mantissa': '1010110000', 'binary': '1101011', 'binary_output': '1101.011', 'hex': '4AB0', 'up scaled number': 107, 'scale': 3, 'number': 13.375}

    Project
    -------
    https://github.com/canbula/ieee754
    """
    return IEEE754(x, 0)


def single(x: str) -> IEEE754:
    """
    IEEE 754 Single Precision Representation

    Parameters
    ----------
    x : str
        Floating point number to be converted.

    Returns
    -------
    IEEE754
        IEEE 754 representation of the number

    Examples
    --------
    >>> single(13.375)
    0 10000010 10101100000000000000000

    >>> single(13.375).hex()
    41560000

    >>> single(13.375).json()
    {'exponent-bits': 8, 'mantissa-bits': 23, 'bias': 127, 'sign': '0', 'exponent': '10000010', 'mantissa': '10101100000000000000000', 'binary': '1101011', 'binary_output': '1101.011', 'hex': '41560000', 'up scaled number': 107, 'scale': 3, 'number': 13.375}

    Project
    -------
    https://github.com/canbula/ieee754
    """
    return IEEE754(x, 1)


def double(x: str) -> IEEE754:
    """
    IEEE 754 Double Precision Representation

    Parameters
    ----------
    x : str
        Floating point number to be converted.

    Returns
    -------
    IEEE754
        IEEE 754 representation of the number

    Examples
    --------
    >>> double(13.375)
    0 10000000010 1010110000000000000000000000000000000000000000000000

    >>> double(13.375).hex()
    402AC00000000000

    >>> double(13.375).json()
    {'exponent-bits': 11, 'mantissa-bits': 52, 'bias': 1023, 'sign': '0', 'exponent': '10000000010', 'mantissa': '1010110000000000000000000000000000000000000000000000', 'binary': '1101011', 'binary_output': '1101.011', 'hex': '402AC00000000000', 'up scaled number': 107, 'scale': 3, 'number': 13.375}

    Project
    -------
    https://github.com/canbula/ieee754
    """
    return IEEE754(x, 2)


def quadruple(x: str) -> IEEE754:
    """
    IEEE 754 Quadruple Precision Representation

    Parameters
    ----------
    x : str
        Floating point number to be converted.

    Returns
    -------
    IEEE754
        IEEE 754 representation of the number

    Examples
    --------
    >>> quadruple(13.375)
    0 100000000000010 1010110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

    >>> quadruple(13.375).hex()
    4002AC00000000000000000000000000

    >>> quadruple(13.375).json()
    {'exponent-bits': 15, 'mantissa-bits': 112, 'bias': 16383, 'sign': '0', 'exponent': '100000000000010', 'mantissa': '1010110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', 'binary': '1101011', 'binary_output': '1101.011', 'hex': '4002AC00000000000000000000000000', 'up scaled number': 107, 'scale': 3, 'number': 13.375}

    Project
    -------
    https://github.com/canbula/ieee754
    """
    return IEEE754(x, 3)


def octuple(x: str) -> IEEE754:
    """
    IEEE 754 Octuple Precision Representation

    Parameters
    ----------
    x : str
        Floating point number to be converted.

    Returns
    -------
    IEEE754
        IEEE 754 representation of the number

    Examples
    --------
    >>> octuple(13.375)
    0 1000000000000000010 10101100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

    >>> octuple(13.375).hex()
    40002AC000000000000000000000000000000000000000000000000000000000

    >>> octuple(13.375).json()
    {'exponent-bits': 19, 'mantissa-bits': 236, 'bias': 262143, 'sign': '0', 'exponent': '1000000000000000010', 'mantissa': '10101100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', 'binary': '1101011', 'binary_output': '1101.011', 'hex': '40002AC000000000000000000000000000000000000000000000000000000000', 'up scaled number': 107, 'scale': 3, 'number': 13.375}

    Project
    -------
    https://github.com/canbula/ieee754
    """
    return IEEE754(x, 4)


if __name__ == "__main__":
    # you can call the precision functions by using their names
    x = 13.375
    print(half(x))
    print(single(x))
    print(double(x))
    print(quadruple(x))
    print(octuple(x))
    # with default options (Double Precision)
    x = 13.375
    a = IEEE754(x)
    # you should call the instance as a string
    print(a)
    print(str(a))
    print(f"{a}")
    # you can get the hexadecimal presentation like this
    print(a.hex())
    # or you can specify a precision
    for p in range(5):
        a = IEEE754(x, p)
        print("x = %f | b = %s | h = %s" % (13.375, a, a.hex()))
        print(a.json())
    # or you can use your own custom precision
    a = IEEE754(x, force_exponent=6, force_mantissa=12)
    print(f"{a}")
    # you can get more details with json
    print(a.json())
    # you can get the converted number and the error
    x = 8.7
    a = IEEE754(x, 1)
    print(f"{x} is converted as {a.converted_number} ± {a.error}")
    x = -0.75
    a = IEEE754(x, 1)
    print(f"{x} is converted as {a.converted_number} ± {a.error}")
    # test edge cases
    print(IEEE754(0))
    print(IEEE754("-0"))
    print(IEEE754("Infinity"))
    print(IEEE754("-Infinity"))
    print(IEEE754("NaN"))
    print(IEEE754("-NaN"))
