# bencoding
# http://www.bittorrent.org/beps/bep_0003.html

import collections
"""
Strings are length-prefixed base ten followed by a colon and the string.
For example 4:spam corresponds to 'spam'.

>>> encode(b'spam')
b'4:spam'

Integers are represented by an 'i' followed by the number in base 10 followed by an 'e'.
For example i3e corresponds to 3 and i-3e corresponds to -3.
Integers have no size limitation. i-0e is invalid.
All encodings with a leading zero, such as i03e, are invalid,
other than i0e, which of course corresponds to 0.

>>> decode(b'i3e')
3
>>> decode(b'i-3e')
-3
>>> decode(b'i0e')
0
>>> decode(b'i03e')
Traceback (most recent call last):
  ...
ValueError: invalid literal for int() with base 0: '03'


Lists are encoded as an 'l' followed by their elements (also bencoded) followed by an 'e'.
For example l4:spam4:eggse corresponds to ['spam', 'eggs'].

>>> decode(b'l4:spam4:eggse')
[b'spam', b'eggs']

Dictionaries are encoded as a 'd' followed by a list of alternating keys
and their corresponding values followed by an 'e'.
For example, d3:cow3:moo4:spam4:eggse corresponds to {'cow': 'moo', 'spam': 'eggs'}
Keys must be strings and appear in sorted order (sorted as raw strings, not alphanumerics).

>>> decode(b'd3:cow3:moo4:spam4:eggse')
OrderedDict([(b'cow', b'moo'), (b'spam', b'eggs')])

"""

def encode(*val):
    coded_str = ''
    for elem in val:
        if isinstance(elem, str):
            coded_str += str(len(elem)) + ':' + str(elem)
        if isinstance(elem, int):
            coded_str += 'i' + str(elem) + 'e'
        if isinstance(elem, (list, tuple)):
            coded_str += 'l' + str(encode(*elem)) + 'e'
        if isinstance(elem, dict):
            coded_str += 'd' + str(encode(*elem)) + 'e'
        # if not isinstance(elem, (list, tuple, dict)):
        #     coded_str += bytes(bencode.encode(elem))
        # else:
        #     coded_str += bytes(encode(elem))
    return str.encode(coded_str)


def decode(val, dict_mod=False):
    final_list = [] if dict_mod==False else collections.OrderedDict()
    this_is_key = True
    d_last_key = ''
    val = val.decode()
    while val:
        key = val[0]
        if key == 'i':
            val = val[1:]
            num_leng = val.find('e')
            number = int(val[:num_leng])
            if dict_mod:
                 if this_is_key:
                     d_last_key = number
                     final_list[d_last_key] = ''
                 else:
                     final_list[d_last_key] = number
            else:
                 final_list.append(number)
            val = val[num_leng + 1:]
            if val == '':
                return number
        if key == 'l':
            if dict_mod:
                if this_is_key:
                    d_last_key = decode(str.encode(val[1:]))
                    final_list[d_last_key] = ''
                else:
                    final_list[d_last_key] = decode(str.encode(val[1:]))
            else:
                final_list.append(decode(str.encode(val[1:])))
            val = val[1:]
        if key == 'd':
            val = val[1:]
            if dict_mod:
                if this_is_key:
                    d_last_key = decode(str.encode(val), dict_mod=True)
                    final_list[d_last_key] = ''
                else:
                    final_list[d_last_key] = decode(str.encode(val), dict_mod=True)
            else:
                final_list.append(decode(str.encode(val), dict_mod=True))
        if key == 'e':
            return final_list
        else:
            separat_pos = val.find(':')
            str_leng = int(val[:separat_pos])
            val = val[separat_pos + 1:]
            target_str = val[:str_leng]
            if dict_mod:
                 if this_is_key:
                     d_last_key = target_str
                     final_list[d_last_key] = ''
                 else:
                     final_list[d_last_key] = target_str
            else:
                 final_list.append(target_str)
            val = val[str_leng:]
            if val == '':
                return str.encode(target_str)
        this_is_key = not this_is_key
    return final_list


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)