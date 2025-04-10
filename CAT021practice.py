import socket
import time

# Setup socket once (outside the loop)
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    try:
        # Static values (fixed ones)
        cat = 21
        cat_byte = cat.to_bytes(1, byteorder='big', signed=False)
        fspec = 0xab9943b10120
        fspec_bytes = fspec.to_bytes(6, byteorder='big', signed=False)
        sac = 0x14
        sic = 0x13
        ds_iden_bytes = sac.to_bytes(1, 'big') + sic.to_bytes(1, 'big')

        # Dynamic inputs (simulate now, receive from your friend later)
        tracknum = 2004
        tracknum_byte = tracknum.to_bytes(2, 'big')

        time_val = 43574.94531
        timeof_appli_position_byte = round(time_val / (1/128)).to_bytes(3, 'big')

        lat = 39.134628307043
        long = -7.33791181817651
        position_byte = (round(lat / (180/(2**30))).to_bytes(4, 'big', signed=True) +
                         round(long / (180/(2**30))).to_bytes(4, 'big', signed=True))

        timeof_appli_velocity_byte = round(time_val / (1/128)).to_bytes(3, 'big')

        target_addr = 0x40797a
        target_addr_byte = target_addr.to_bytes(3, 'big')

        timeof_receptn_position_byte = round(time_val / (1/128)).to_bytes(3, 'big')

        geoheight = 35950
        geoheight_byte = round(geoheight / 6.25).to_bytes(2, 'big')

        flight_lvl = int(geoheight / 100)
        flight_lvl_byte = round(flight_lvl / 0.25).to_bytes(2, 'big')

        mag_heading = 243.98
        mag_heading_byte = round(mag_heading / (360 / (2**16))).to_bytes(2, 'big')

        baro_ver_rate = -62.5
        baro_ver_rate_byte = ((round(baro_ver_rate / 6.25)) & 0x7FFF).to_bytes(2, 'big', signed=False)

        geo_ver_rate = -62.5
        geo_ver_rate_byte = ((round(geo_ver_rate / 6.25)) & 0x7FFF).to_bytes(2, 'big', signed=False)

        msg_amp = 81
        msg_amp_byte = msg_amp.to_bytes(1, 'big')

        # Combine all parts
        data_part = (
            ds_iden_bytes + tracknum_byte + timeof_appli_position_byte +
            position_byte + timeof_appli_velocity_byte + target_addr_byte +
            timeof_receptn_position_byte + geoheight_byte + flight_lvl_byte +
            mag_heading_byte + baro_ver_rate_byte + geo_ver_rate_byte +
            msg_amp_byte
        )

        length = len(data_part)
        length_bytes = length.to_bytes(2, 'big')

        # Final packet
        packet = cat_byte + length_bytes + fspec_bytes + data_part

        # Send packet
        sock.sendto(packet, (UDP_IP, UDP_PORT))
        print("Packet sent:", packet.hex().upper())

        time.sleep(1)  # Send 1 packet per second (adjust if needed)

    except KeyboardInterrupt:
        print("\nStopped sending.")
        break