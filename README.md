# ieee754

ieee754 is small Python library which gives you the IEEE-754 representation of a floating point number. You can specify a precision given in the list below or you can even use your own custom precision.
<ul>
<li>Half Precision (16 bit: 1 bit for sign + 5 bits for exponent + 10 bits for mantissa)</li>
<li>Single Precision (32 bit: 1 bit for sign + 8 bits for exponent + 23 bits for mantissa)</li>
<li>Double Precision (64 bit: 1 bit for sign + 11 bits for exponent + 52 bits for mantissa)</li>
<li>Quadrupole Precision (128 bit: 1 bit for sign + 15 bits for exponent + 112 bits for mantissa)</li>
<li>Octuple Precision (256 bit: 1 bit for sign + 19 bits for exponent + 236 bits for mantissa)</li>

## Prerequisites

ieee754 uses numpy, so you should install numpy first.
```sh
$ pip install numpy
```

## Installing

To download ieee754, either fork this github repo or simply use Pypi via pip.
```sh
$ pip install ieee754
```

## Using
After installation, you can import ieee754 and use it in your projects.

### Default Options
Default precision is Double Precision and you can get the output by just calling the instance as a string.
```Python
from ieee754 import IEEE754

x = 13.375
a = IEEE754(x)
# you should call the instance as a string
print(str(a))
print(f"{a}")
# you can get the hexadecimal presentation like this
print(a.str2hex())
```

### Select a Precision
You can use Half (p=0), Single (p=1), Double (p=2), Quadrupole (p=3) or Octuple precision (p=4).
```Python
from ieee754 import IEEE754

for p in range(5):
    a = IEEE754(x, p)
    print("x = %f | b = %s | h = %s" % (13.375, a, a.str2hex()))
```

### Using a Custom Precision
You can force total length, exponent, and mantissa size, and also the bias.
```Python
a = IEEE754(x, force_length=19, force_exponent=6, force_mantissa=12, force_bias=31)
print(f"{a}")
```



License
----

MIT License

Copyright (c) 2021 Bora Canbula

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.