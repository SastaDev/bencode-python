'''
Bencode is binary serialization format used in BitTorrent for storing and transmitting loosely structured data.

It supports four data types:
    * Integer - int
    * Byte String - str
    * List - list
    * Dictionary - dict

Class Encoder:
    * Encodes Python int, str, list, and dict objects to their corresponding Bencode representations.

    - Example:
        >>> import bencode
        >>> encoder = bencode.Encoder() # Initialize class Encoder instance.
        >>> data = 'spam' # A python string.
        >>> encoder.encode(data) # Encodes python string to bencode byte string.
        b'4:spam'

    * Read Encoder class docstring for more information.

Class Decoder:
    * Decodes Bencode representations of int, str, list, and dict objects to their Python representations.

    - Example:
        >>> import bencode
        >>> decoder = bencode.Decoder() # Initialize class Decoder instance.
        >>> data = b'4:spam' # A bencode byte string.
        >>> decoder.decode(data) # Decodes bencode byte string to python string.
        'spam'

    * Read Decoder class docstring for more information.
'''

from .encoder import Encoder
from .decoder import Decoder

__version__ = '0.0.1'
__author__ = 'Sasta Dev'