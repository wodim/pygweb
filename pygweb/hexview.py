def hexview(content):
    step = 16
    padding = (step * 2) + (step - 1)
    length = len(content)
    output = ''
    
    for interval in range(0, length, step):
        # address
        address = '%08x' % interval

        # bytearray and ascii
        bytearray = []
        ascii = ''
        for byte in content[interval:interval+step]:
            bytearray.append('%02x' % ord(byte))
            if ord(byte) > 32:
                try:
                    ascii += byte.decode('utf8')
                except:
                    ascii += '.'
            else:
                ascii += '.'

        bytearray = ' '.join(bytearray)
        output += '%s   %s   %s\n' % (address, bytearray.ljust(padding, ' '), ascii)

    return output