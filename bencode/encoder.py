from typing import Union
from . import exceptions

class Encoder:
    def __init__(self):
        pass

    def encode_integer(self, data: int) -> bytes:
        '''
Encodes a python integer to bencode integer.

- Example:
    >>> from bencode import Encoder
    >>> encoder = Encoder()
    >>> encoder.encode(42)
    b'i42e'

- Exceptions:
    * exceptions.EncodeIntegerError:
        - if data is not a python integer.

- Returns:
    Returns converted python integer to bencode integer in bytes.
        '''
        if not isinstance(data, int):
            raise exceptions.EncodeIntegerError(f'Expected int, got {type(data)}')
        integer = f'i{data}e'
        result = integer.encode()
        return result

    def encode_string(self, data: Union[bytes, str]) -> bytes:
        '''
Encodes a python string or python bytes to bencode string.

- Example:
    >>> from bencode import Encoder
    >>> encoder = Encoder()
    >>> encoder.encode('spam')
    b'4:spam'

- Exceptions:
    * exceptions.EncodeStringError:
        - if data is not a python string or python bytes.

- Returns:
    Returns converted python string or python bytes to bencode string in bytes.

        '''
        if not isinstance(data, (str, bytes)):
            raise exceptions.EncodeStringError(f'Expected str or byte, got {type(data)}')
        data = data.encode() if not isinstance(data, bytes) else data
        length = str(len(data)).encode()
        result = length + b':' + data
        return result

    def encode_list(self, data: list) -> bytes:
        '''
Encodes a python list to bencode list.

- Example:
    >>> from bencode import Encoder
    >>> encoder = Encoder()
    >>> encoder.encode(['spam'])
    b'l4:spame'

- Exceptions:
    * exceptions.EncodeListError:
        - if data is not a python list.

- Returns:
    Returns converted python list to bencode list in bytes.

        '''
        if not isinstance(data, list):
            raise exceptions.EncodeListError(f'Expected list, got {type(data)}')
        result = b'l'
        for item in data:
            if isinstance(item, int):
                integer = self.encode_integer(item)
                result += integer
                continue
            if isinstance(item, (str, bytes)):
                string = self.encode_string(item)
                result += string
                continue
            if isinstance(item, list):
                _list = self.encode_list(item)
                result += _list
                continue
            if isinstance(item, dict):
                dictionary = self.encode_dictionary(item)
                result += dictionary
                continue
        result += b'e'
        return result

    def encode_dictionary(self, data: dict) -> bytes:
        '''
Encodes a python dict to bencode dict.

- Example:
    >>> from bencode import Encoder
    >>> encoder = Encoder()
    >>> encoder.encode({'spam': 42})
    b'd4:spami42ee'

- Exceptions:
    * exceptions.EncodeDictionaryError:
        - if data is not a python dict.
        - if dict key is not a string or not a byte.
        - if the value of key of the dict is not a int, str, list or dict.

- Returns:
    Returns converted python dict to bencode dict in bytes.
        '''
        if not isinstance(data, dict):
            raise exceptions.EncodeListError(f'Expected dict, got {type(data)}')
        result = b'd'
        for key, value in data.items():
            if isinstance(key, (str, bytes)):
                string = self.encode_string(key)
                result += string
            else:
                raise exceptions.EncodeDictionaryError(f'Expected dict key type str or byte, got {type(key)}')
            if isinstance(value, (str, bytes)):
                string = self.encode_string(value)
                result += string
            elif isinstance(value, int):
                integer = self.encode_integer(value)
                result += integer
            elif isinstance(value, list):
                _list = self.encode_list(value)
                result += _list
            elif isinstance(value, dict):
                dictionary = self.encode_dictionary(value)
                result += dictionary
            else:
                raise exceptions.EncodeDictionaryError(f'Expected type int, str, list or dict, got {type(value)}')
        result += b'e'
        return result

    def encode(self, data: Union[bytes, str, int, list, dict]) -> Union[bytes, str, int, list, dict]:
        '''
Encodes Returns bytes of bencode int, str, list and dict objects to their corresponding Python representations.

- Example:
    >>> from bencode import Encoder
    >>> encoder = Encoder()
    >>> # Encode a python integer.
    >>> encoder.encode(42)
    b'i42e'
    >>> # Encode a python string.
    >>> encoder.encode('spam')
    b'4:spam'
    >>> # Encode a python list.
    >>> encoder.encode(['spam'])
    b'l4:spame'
    >>> # Encode a python dict.
    >>> encoder.encode({'spam': 42})
    b'd4:spami42ee'

- Exceptions:
    * exceptions.EncodeError:
        - if data is not a python int, str, list or dict.

- Returns:
    Returns bytes of bencode int, str, list and dict objects to their corresponding Python representations.
        '''
        if isinstance(data, (str, bytes)):
            return self.encode_string(data)
        elif isinstance(data, int):
            return self.encode_integer(data)
        elif isinstance(data, list):
            return self.encode_list(data)
        elif isinstance(data, dict):
            return self.encode_dictionary(data)
        raise exceptions.EncodeError(f'Expected type int, str, list or dict, got {type(data)}')