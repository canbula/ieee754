# ieee754

ieee754 is a Python module which finds the IEEE-754 representation of a floating point number. You can specify a precision given in the list below or you can even use your own custom precision.
<ul>
    <li>Half Precision (16 bit: 1 bit for sign + 5 bits for exponent + 10 bits for mantissa)</li>
    <li>Single Precision (32 bit: 1 bit for sign + 8 bits for exponent + 23 bits for mantissa)</li>
    <li>Double Precision (64 bit: 1 bit for sign + 11 bits for exponent + 52 bits for mantissa)</li>
    <li>Quadruple Precision (128 bit: 1 bit for sign + 15 bits for exponent + 112 bits for mantissa)</li>
    <li>Octuple Precision (256 bit: 1 bit for sign + 19 bits for exponent + 236 bits for mantissa)</li>
</ul>

## Prerequisites

ieee754 does not require any external libraries or modules.

## Installing

To download ieee754, either fork this github repo or simply use Pypi via pip.
```sh
$ pip install ieee754
```

## Using

After installation, you can import ieee754 and use it in your projects.

### Simplest Example

The simplest example is to use the desired precision IEEE-754 representation of a floating point number. You can import the desired precision from ieee754 and use it like this. The available precisions are half, single, double, quadruple and octuple.
```Python
from ieee754 import double

print(double(13.375))
```

### Default Options

Default precision is Double Precision and you can get the output by just calling the instance as a string.
```Python
from ieee754 import IEEE754

x = 13.375
a = IEEE754(x)
# you should call the instance as a string
print(a)
print(str(a))
print(f"{a}")
# you can get the hexadecimal presentation like this
print(a.hex())
# you can get more detailed information like this
print(a.json())
```

### Select a Precision

You can use Half (p=0), Single (p=1), Double (p=2), Quadrupole (p=3) or Octuple precision (p=4).
```Python
from ieee754 import IEEE754

for p in range(5):
    a = IEEE754(x, p)
    print("x = %f | b = %s | h = %s" % (13.375, a, a.hex()))
```

### Use the Precision Name as an Interface

You can use the precision name as an interface to get the IEEE-754 representation of a floating point number. With this method you can get the IEEE-754 representation of a floating point number without creating an instance.
```Python
from ieee754 import half, single, double, quadruple, octuple

x = 13.375
print(half(x))
print(single(x))
print(double(x))
print(quadruple(x))
print(octuple(x))
```

### Using a Custom Precision

You can force exponent, and mantissa size by using force_exponent and force_mantissa parameters to create your own custom precision.
```Python
a = IEEE754(x, force_exponent=6, force_mantissa=12)
print(a)
```



License
----

MIT License

Copyright (c) 2021 Bora Canbula

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
