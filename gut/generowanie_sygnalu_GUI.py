def crc4(message, nBytes, polynomial, init):
    remainder = init << 4  # LSBs are unused
    poly = polynomial << 4

    while nBytes:
        remainder ^= message[0]
        message = message[1:]

        for bit in range(8):
            if remainder & 0x80:
                remainder = (remainder << 1) ^ poly
            else:
                remainder = (remainder << 1)
        nBytes -= 1

    return (remainder >> 4) & 0x0F  # discard the LSBs


def generate_crc(msg):
    crc = crc4(msg, 4, 0x13, 0)  # Koopmann 0x9, CCITT-4; FP-4; ITU-T G.704
    crc ^= msg[4] >> 4
    return crc

def calc_temp(temp_c):
    temp_f = (temp_c * 9 / 5) + 32
    temp_raw = (temp_f / 0.1) + 900
    return hex(int(temp_raw))

# postac heksadecymalna
def generate_bin(temp_c, humidity, channel):
    bajt1 = 155  # 1 id

    temp = calc_temp(temp_c)

    bajt3 = temp[0:4]
    # if humidity == 20 or humidity == 21:
    #     humidity = 22
    if len(str(humidity)) == 1:
        humidity = "0" + str(humidity)
    else:
        humidity = str(humidity)
    bajt4 = "0x" + temp[-1] + humidity[0]
    bajt5 = "0x" + humidity[1] + str(channel)
    bajt2 = hex(channel) + str(2)

    data = [bajt1, hex2dec(bajt2), hex2dec(bajt3), hex2dec(bajt4), hex2dec(bajt5)]
    crc = generate_crc(data)

    bajt2 = bajt2.replace(bajt2[2], hex(crc)[2:], 1)
    data_dec = [bajt1, hex2dec(bajt2), hex2dec(bajt3), hex2dec(bajt4), hex2dec(bajt5)]

    data_bin = ""
    for x in data_dec:
        data_add = decimal_to_binary(x)
        data_bin += data_add

    return data_bin


def hex2dec(val):
    dec = int(val, base=16)
    return dec


def decimal_to_binary(val):
    return format(val, '08b').replace("0b", "")


def create_signal(data_bin):
    with open("bit1.raw", "rb") as file_bit1:
        bit1 = file_bit1.read()

    with open("bit0.raw", "rb") as file_bit0:
        bit0 = file_bit0.read()

    with open("preambula.raw", "rb") as file_preambula:
        preambula = file_preambula.read()

    signal_out = preambula

    for bit in data_bin:
        if bit == "1":
            signal_out = signal_out + bit1
        elif bit == "0":
            signal_out = signal_out + bit0

    signal_out = signal_out + bit1

    with open("../generated_signal.raw", "wb") as file_out:
        file_out.write(signal_out)

# 9B 32 8F C9 93


if __name__ == "__main__":
    # generate_bin(60, 99, 3)
    create_signal(generate_bin(-50, 120, 3))
    # nadawanieGNU.main()
