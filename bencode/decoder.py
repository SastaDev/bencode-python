from typing import Optional, Tuple, Union
from . import exceptions

class Decoder:
    def __init__(self) -> None:
        '''
Decodes Bencode representations of int, str, list, and dict objects to their Python representations.
        '''
        pass

    def decode_integer(self, data: Union[bytes, str], pos: Optional[int] = 0) -> Tuple[int, int]:
        '''
Decodes bencode integer to python integer.

- Example:
    >>> from bencode import Decoder
    >>> decoder = Decoder()
    >>> decoder.decode_integer(b'i42e')
    (42, 3)

- Exceptions:
    * exceptions.DecodeIntegerError:
        - If data is not bytes or not str.
        - Start of integer not found.
        - End of integer not found.
        - Invalid integer.

- Returns:
    Returns a tuple of python integer and ending index of integer in the data.
        '''
        if not isinstance(data, (bytes, str)):
            raise DecodeIntegerError(f'Expected bytes or str, got {type(data)}')
        data = data.encode() if isinstance(data, str) else data
        if data[pos] != ord('i'):
            raise exceptions.DecodeIntegerError(f'Start of integer not found, at position {pos}')
        end = data.find(b'e', pos)
        if end == -1:
            raise exceptions.DecodeIntegerError(f'End of integer not found, from position {pos}')
        try:
            integer = int(data[pos+1:end])
        except ValueError:
            raise exceptions.DecodeIntegerError(f'Invalid integer, from position {pos}')
        return integer, end

    def decode_string(self, data: Union[bytes, str], pos: Optional[int] = 0) -> Tuple[bytes, int]:
        '''
Decodes bencode string to python bytes of string.

- Example:
    >>> from bencode import Decoder
    >>> decoder = Decoder()
    >>> decoder.decode_string(b'4:spam')
    (b'spam', 5)

- Exceptions:
    * exceptions.DecodeStringError:
        - If data is not bytes or not str.
        - Colon of string not found.
        - Invalid length of string.
        - Expected length of string is not statisfied by length of string.

- Returns:
    Returns a tuple of python bytes of string and ending index of string in the data.
        '''
        if not isinstance(data, (bytes, str)):
            raise DecodeStringError(f'Expected bytes or str, got {type(data)}')
        data = data.encode() if isinstance(data, str) else data
        colon_index = data.find(b':', pos)
        if colon_index == -1:
            raise exceptions.DecodeStringError(f'Colon of string not found, from position {pos}')
        try:
            length = int(data[pos:colon_index])
        except ValueError:
            raise exceptions.DecodeStringError(f'Invalid length of string, from position {pos}')
        end = colon_index+1 + length
        string = data[colon_index+1:end]
        if len(string) < length:
            raise exceptions.DecodeStringError(f'Expected string length {length}, got {len(string)}, from position {pos}')
        return string, end-1

    def decode_list(self, data: Union[bytes, str], pos: Optional[int] = 0) -> Tuple[list, int]:
        '''
Decodes bencode list to python list.

- Example:
    >>> from bencode import Decoder
    >>> decoder = Decoder()
    >>> decoder.decode_list(b'l4:spame')
    ([b'spam'], 7)

- Exceptions:
    * exceptions.DecodeListError:
        - If data is not bytes or not str.
        - Start of list not found.
        - Invalid data type in list.
        - End of list not found.

- Returns:
    Returns a tuple of python list and ending index of list in the data.
        '''
        if not isinstance(data, (bytes, str)):
            raise DecodeListError(f'Expected bytes or str, got {type(data)}')
        data = data.decode() if not isinstance(data, bytes) else data
        if data[pos] != ord('l'):
            raise exceptions.DecodeListError(f'Start of list not found, at position {pos}')
        current_pos = pos + 1
        contents = []
        while current_pos < len(data):
            if data[current_pos] == ord('i'):
                integer, end = self.decode_integer(data, current_pos)
                contents.append(integer)
                current_pos = end + 1
                continue
            if ord('0') <= data[current_pos] <= ord('9'):
                string, end = self.decode_string(data, current_pos)
                contents.append(string)
                current_pos = end + 1
                continue
            if data[current_pos] == ord('l'):
                _list, end = self.decode_list(data, current_pos)
                contents.append(_list)
                current_pos = end + 1
                continue
            if data[current_pos] == ord('d'):
                dictionary, end = self.decode_dictionary(data, current_pos)
                contents.append(dictionary)
                current_pos = end + 1
                continue
            if data[current_pos] == ord('e'):
                break
            raise exceptions.DecodeListError(f'Invalid data type in list, at position {current_pos}')
        else:
            raise exceptions.DecodeListError(f'End of list not found, from position {pos}')
        return contents, current_pos

    def decode_dictionary(self, data: Union[bytes, str], pos: Optional[int] = 0) -> Tuple[dict, int]:
        '''
Decodes bencode dict to python dict.

- Example:
    >>> from bencode import Decoder
    >>> decoder = Decoder()
    >>> decoder.decode_dictionary(b'd4:spami42ee')
    ({b'spam': 42}, 11)

- Exceptions:
    * exceptions.DecodeDictionaryError:
        - If data is not bytes or not str.
        - Start of dict not found.
        - Invalid data type in dict.
        - End of dict not found.

- Returns:
    Returns a tuple of python dict and ending index of dict in the data.

        '''
        if not isinstance(data, (bytes, str)):
            raise DecodeDictionaryError(f'Expected bytes or str, got {type(data)}')
        data = data.decode() if not isinstance(data, bytes) else data
        if data[pos] != ord('d'):
            raise exceptions.DecodeListError(f'Start of dictionary not found, at position {pos}')
        current_pos = pos + 1
        result = {}
        while current_pos < len(data):
            if data[current_pos] == ord('e'):
                break
            key, end = self.decode_string(data, current_pos)
            current_pos = end + 1
            if data[current_pos] == ord('i'):
                integer, end = self.decode_integer(data, current_pos)
                result[key] = integer
                current_pos = end + 1
                continue
            if ord('0') <= data[current_pos] <= ord('9'):
                string, end = self.decode_string(data, current_pos)
                result[key] = string
                current_pos = end + 1
                continue
            if data[current_pos] == ord('l'):
                _list, end = self.decode_list(data, current_pos)
                result[key] = _list
                current_pos = end + 1
                continue
            if data[current_pos] == ord('d'):
                dictionary, end = self.decode_dictionary(data, current_pos)
                result[key] = dictionary
                current_pos = end + 1
                continue
            raise exceptions.DecodeDictionaryError(f'Invalid dictionary value, at position {current_pos}')
        else:
            raise exceptions.DecodeDictionaryError(f'End of dictionary not found, from position {pos}')
        return result, current_pos

    def decode(self, data: Union[bytes, str], pos: Optional[int] = 0) -> Union[bytes, int, list, dict]:
        '''
Decodes bencode data types to python data types.

- Example:
    >>> from bencode import Decoder
    >>> decoder = Decoder()
    >>> # Decode a bencode integer.
    >>> decoder.decode(b'i42e')
    42
    >>> # Decode a bencode string.
    >>> decoder.decode(b'4:spam')
    b'spam'
    >>> # Decode a bencode list.
    >>> decoder.decode(b'l4:spame')
    [b'spam']
    >>> # Decode a bencode dict.
    >>> decoder.decode(b'd4:spami42ee')
    {b'spam': 42}

- Returns:
    Returns bytes of Python int, str, list, and dict objects to their corresponding Bencode representations.
        '''
        if not isinstance(data, bytes):
            data = data.encode()
        if data[pos] == ord('i'):
            integer, end = self.decode_integer(data, pos)
            return integer
        if ord('0') <= data[pos] <= ord('9'):
            string, end = self.decode_string(data, pos)
            return string
        if data[pos] == ord('l'):
            _list, end = self.decode_list(data, pos)
            return _list
        if data[pos] == ord('d'):
            dictionary, end = self.decode_dictionary(data, pos)
            return dictionary