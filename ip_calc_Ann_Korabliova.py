def in_binary(number):
    """str -> str
    Returns converted ip address to binary

    >>> in_binary('25.34.101.255')
    '00011001.00100010.01100101.11111111'
    >>> in_binary('255.0.255.0')
    '11111111.00000000.11111111.00000000'
    """

    numbers = ['0'*(8-len(bin(int(i))[2:])) + bin(int(i))[2:]
               for i in number.split(".")]
    return '.'.join(numbers)


def from_binary(number):
    """str -> str
    Returns converted ip address to decimal

    >>> from_binary('10110110.11111001.11001101.1001101')
    '182.249.205.77'
    >>> from_binary('00110110.00000001.00001101.0001101')
    '54.1.13.13'
    >>> from_binary('11111111.11111111.11111111.11111111')
    '255.255.255.255'
    """

    numbers = [str(int(i, 2)) for i in number.split(".")]
    return '.'.join(numbers)


def creat_ip(number):
    """str -> str
    Returns a binary number as an ip address

    >>> creat_ip('1011011011111001110011011001101')
    '1011011.01111100.11100110.11001101'
    >>> creat_ip('0011011000000001000011010001101')
    '0011011.00000000.10000110.10001101'
    >>> creat_ip('11111111111111111111111111111111')
    '11111111.11111111.11111111.11111111'
    """

    return number[:-24] + '.' + number[-24:-16] + '.' + number[-16:-8] + '.' + number[-8:]


def get_ip_from_raw_address(raw_address):
    """str -> str
    Returns an ip address from a raw_address

    >>> get_ip_from_raw_address('192.168.1.15/24')
    '192.168.1.15'
    >>> get_ip_from_raw_address('252.8.1.255/4')
    '252.8.1.255'
    """

    return raw_address.split('/')[0]


def get_network_address_from_raw_address(raw_address):
    """str -> str
    Returns an network address from a raw_address

    >>> get_network_address_from_raw_address('192.168.1.15/24')
    '192.168.1.0'
    >>> get_network_address_from_raw_address('252.8.1.255/4')
    '240.0.0.0'
    """

    binary_address = in_binary(get_ip_from_raw_address(raw_address))
    maska = int(raw_address.split('/')[1])
    bin_addr = ''.join(binary_address.split('.'))[:maska] + '0' * (32 - maska)
    return from_binary(creat_ip(bin_addr))


def get_broadcast_address_from_raw_address(raw_address):
    """str -> str
    Returns a broadcast address from a raw_address

    >>> get_broadcast_address_from_raw_address('192.168.1.15/24')
    '192.168.1.255'
    >>> get_broadcast_address_from_raw_address('252.8.1.255/4')
    '255.255.255.255'
    """

    binary_address = in_binary(get_ip_from_raw_address(raw_address))
    maska = int(raw_address.split('/')[1])
    bin_addr = ''.join(binary_address.split('.'))[:maska] + '1' * (32 - maska)
    return from_binary(creat_ip(bin_addr))


def get_binary_mask_from_raw_address(raw_address):
    """str -> str
    Returns a binary mask from a raw_address

    >>> get_binary_mask_from_raw_address('192.168.1.15/24')
    '11111111.11111111.11111111.00000000'
    >>> get_binary_mask_from_raw_address('252.8.1.255/4')
    '11110000.00000000.00000000.00000000'
    """

    number_of_one = int(raw_address.split('/')[1])
    binary = number_of_one * '1' + (32-number_of_one) * '0'
    return creat_ip(binary)


def get_first_usable_ip_address_from_raw_address(raw_address):
    """str -> str
    Returns the first usable ip address from a raw_address

    >>> get_first_usable_ip_address_from_raw_address('192.168.1.15/24')
    '192.168.1.1'
    >>> get_first_usable_ip_address_from_raw_address('252.8.1.255/4')
    '240.0.0.1'
    """

    binary_number = ''.join(
        in_binary(get_network_address_from_raw_address(raw_address)).split('.'))
    return from_binary(creat_ip(bin(int(binary_number, 2) + 1)[2:]))


def get_penultimate_usable_ip_address_from_raw_address(raw_address):
    """str -> str
    Returns a penultimate usable ip address from a raw_address

    >>> get_penultimate_usable_ip_address_from_raw_address('192.168.1.15/24')
    '192.168.1.253'
    >>> get_penultimate_usable_ip_address_from_raw_address('252.8.1.255/4')
    '255.255.255.253'    
    """

    binary_number = ''.join(
        in_binary(get_broadcast_address_from_raw_address(raw_address)).split('.'))
    return from_binary(creat_ip(bin(int(binary_number, 2) - 2)[2:]))


def get_number_of_usable_hosts_from_raw_address(raw_address):
    """str -> int
    Returns a number of usable hosts from a raw_address

    >>> get_number_of_usable_hosts_from_raw_address('192.168.1.15/24')
    254
    >>> get_number_of_usable_hosts_from_raw_address('252.8.1.255/4')
    268435454
    """

    return 2**(32 - int(raw_address.split('/')[1])) - 2


def get_ip_class_from_raw_address(raw_address):
    """str -> str
    Returns an ip class from a raw_address

    >>> get_ip_class_from_raw_address('192.168.1.15/24')
    'C'
    >>> get_ip_class_from_raw_address('252.8.1.255/4')
    'E'    
    """

    first_byte = int(raw_address.split('.')[0])
    if 1 <= first_byte <= 126:
        return 'A'
    elif 128 <= first_byte <= 191:
        return 'B'
    elif 192 <= first_byte <= 223:
        return 'C'
    elif 224 <= first_byte <= 239:
        return 'D'
    else:
        return 'E'


def check_private_ip_address_from_raw_address(raw_address):
    """ str -> bool
    Returns True if an ip address from a raw_address is private and returns False if it isn't

    >>> check_private_ip_address_from_raw_address('192.168.1.15/24')
    True
    >>> check_private_ip_address_from_raw_address('252.8.1.255/4')
    False
    """

    raw = ''.join(in_binary(get_ip_from_raw_address(raw_address)).split('.'))
    return raw[:8] == '00001010' or raw[:12] == '101011001' or raw[:16] == '1100000010101000'


try:
    raw_address = input()
    if len(raw_address.split('.')) != 4:
        print('Error')
    elif len(raw_address.split('/')) != 2:
        print('Missing prefix')
    else:
        network_address = get_network_address_from_raw_address(raw_address)
        print('IP address:', get_ip_from_raw_address(raw_address))
        print('Network Address:', network_address)
        print('Broadcast Address:',
              get_broadcast_address_from_raw_address(raw_address))
        print('Binary Subnet Mask:', get_binary_mask_from_raw_address(raw_address))
        print('First usable host IP:',
              get_first_usable_ip_address_from_raw_address(raw_address))
        print('Penultimate usable host IP:',
              get_penultimate_usable_ip_address_from_raw_address(raw_address))
        print('Number of usable Hosts:',
              get_number_of_usable_hosts_from_raw_address(raw_address))
        print('IP class:', get_ip_class_from_raw_address(raw_address))
        print('IP type private:',
              check_private_ip_address_from_raw_address(raw_address))
except IndexError:
    print('Missing prefix')
except:
    print('Error')
