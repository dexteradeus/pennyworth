[![Build Status](https://travis-ci.org/dexteradeus/pennyworth.svg?branch=master)](https://travis-ci.org/dexteradeus/pennyworth)

# Pennyworth

Python interaction with an Alfred (Almighty Lightweight Fact Remote Exchange Daemon) server

## Installation

    python setup.py install

## Usage

To request data from the Alfred Server:

    from pennyworth import client
    c = client.AlfredClient()
    data = c.request_data(153)

To set data in the Alfred cloud:

    from pennyworth import client
    c = client.AlfredClient()
    data = c.send_data(153, b'this is some data')

You can also set the version number of the data:

    data = c.send_data(153, b'this is some new data', version=2)

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request. Patches Welcome&trade;

## License

The MIT License (MIT)
Copyright &copy; 2016 Chris Hand

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
