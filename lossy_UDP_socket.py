import socket as s
import random

from socket import AF_INET, AF_INET6, SOCK_DGRAM, SOCK_RAW, SOCK_STREAM, timeout

bitflip_probability = 0.03
drop_probability = 0.25

has_msg_methods = hasattr(s.socket, 'recvmsg')

bitflip_values = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80
]

def mangle_data(data: bytes) -> bytes:
    return bytes(mangle_byte(b) for b in data)

def mangle_byte(byte: int) -> int:
    if random.random() < bitflip_probability:
        flip_value = random.choice(bitflip_values)
        return byte ^ flip_value
    else:
        return byte

def mangle_into(buffers, nbytes: int):
    n = 0
    i = 0
    while n < nbytes and i < len(buffers):
        current_buffer = buffers[i]
        j = 0
        while n < nbytes and j < len(current_buffer):
            if random.random < bitflip_probability:
                flip_value = random.choice(bitflip_values)
                current_buffer[j] = current_buffer[j] ^ flip_value
            n += 1
            j += 1
        i += 1

def set_probabilities(bitflip: float, drop: float):
    global bitflip_probability, drop_probability
    bitflip_probability = bitflip
    drop_probability = drop

def unsupported_functionality(*args, **kwargs):
    raise NotImplementedError('This method is not supported in this task.')

class socket(s.socket):
    def __init__(self, family, type=s.SOCK_DGRAM, proto=0, fileno=None):
        # we only allow UDP sockets
        if type != s.SOCK_DGRAM:
            raise ValueError('Only UDP sockets are supported.')
        if fileno is not None:
            raise ValueError('Creating a socket from a file descriptor is not supported.')
        # create the real socket
        super().__init__(family, type, proto)

    def recv(self, bufsize, flags=0):
        data = super().recv(bufsize, flags)
        data = mangle_data(data)
        if random.random() < drop_probability:
            raise timeout('timed out')
        else:
            return data

    def recvfrom(self, bufsize, flags=0):
        data, addr = super().recvfrom(bufsize, flags)
        data = mangle_data(data)
        if random.random() < drop_probability:
            raise timeout('timed out')
        else:
            return data, addr

    if has_msg_methods:
        def recvmsg(bufsize, ancbufsize=0, flags=0):
            data, ancdata, msg_flags, address = super().recvmsg(bufsize, flags)
            data = mangle_data(data)
            if random.random() < drop_probability:
                raise timeout('timed out')
            else:
                return data, ancdata, msg_flags, address

        def recvmsg_into(self, buffers, ancbufsize=0, flags=0):
            if random.random() < drop_probability:
                # clear the recv buffer
                _ = super().recvmsg(4096)
                raise timeout('timed out')
            else:
                nbytes, ancdata, msg_flags, address = super().recvmsg_into(buffers, ancbufsize, flags)
                mangle_into(buffers, nbytes)
                return nbytes, ancdata, msg_flags, address

        def sendmsg(self, buffers, ancdata, flags, address):
            # mangle data
            buffers = [mangle_data(buf) for buf in buffers]
            # call the real send function
            if random.random() < drop_probability:
                return sum(len(buf) for buf in buffers)
            else:
                return super().sendmsg(buffers, ancdata, flags, address)

    def recvfrom_into(self, buffer, nbytes=0, flags=0):
        if random.random() < drop_probability:
            # clear the recv buffer
            _ = super().recvfrom(4096)
            raise timeout('timed out')
        else:
            nbytes, address = super().recvfrom_into(buffer, nbytes, flags)
            mangle_into([buffer], nbytes)
            return nbytes, address

    def recv_into(self, buffer, nbytes=0, flags=0):
        if random.random() < drop_probability:
            # clear the recv buffer
            _ = super().recv(4096)
            raise timeout('timed out')
        else:
            nbytes = super().recv_into(buffer, nbytes, flags)
            mangle_into([buffer], nbytes)
            return nbytes

    def send(self, buf, *args, **kwargs):
        # mangle data
        buf = mangle_data(buf)
        # call the real send function
        if random.random() < drop_probability:
            return len(buf)
        else:
            return super().send(buf, *args, **kwargs)

    def sendall(self, buf, *args, **kwargs):
        # mangle data
        buf = mangle_data(buf)
        # call the real send function
        if random.random() < drop_probability:
            return 
        else:
            return super().sendall(buf, *args, **kwargs)

    def sendto(self, buf, *args, **kwargs):
        # mangle data
        buf = mangle_data(buf)
        # call the real send function
        if random.random() < drop_probability:
            return len(buf)
        else:
            return super().sendto(buf, *args, **kwargs)

    # disable various TCP related methods.
    accept = unsupported_functionality
    connect = unsupported_functionality
    connect_ex = unsupported_functionality
    listen = unsupported_functionality


create_connection = unsupported_functionality
create_server = unsupported_functionality
fromfd = unsupported_functionality
fromshare = unsupported_functionality