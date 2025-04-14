import time
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005  # Destination port
SOURCE_PORT = 4000  # Fixed source port you choose (any unused one)

# Create socket once and bind to fixed source port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", SOURCE_PORT))  # "" = all interfaces

# Entry list (simulate different inputs)
entries = [
    {"lat": 39.134628307043, "lon": -7.33791181817651, "geo_height": 35950, "baro_rate": -62.5, "mag_heading": 243.98, "target_addr": 0x40797a},
    {"lat": 12.819580081245, "lon": 76.625944996951, "geo_height": 38000, "baro_rate": 30.0, "mag_heading": 165.93, "target_addr": 0x06a0f5},
    {"lat": 46.625944996954, "lon": 39.134628307043, "geo_height": 14440, "baro_rate": 0,"mag_heading": 148.92, "target_addr": 0x111a1b}
]

# For assigning track numbers
track_map = {}
track_counter = 1

try:
    while True:
        for entry in entries:
            packet=b''
            cat=21
            cat_byte=cat.to_bytes(1,byteorder='big',signed=False)
            # print(cat_byte)
            fspec=0xab9943b10120
            fspec_bytes=fspec.to_bytes(6,byteorder='big',signed=False)
            sac=0x14
            sic=0x13
            ds_iden_bytes=(sac.to_bytes(1,byteorder='big',signed=False))+(sic.to_bytes(1,byteorder='big',signed=False))
            # print("ds_iden_bytes :",ds_iden_bytes)
            # tracknum=2004
            target_addr = entry["target_addr"]
            if target_addr not in track_map:
                track_map[target_addr] = track_counter
                track_counter += 1
            tracknum = track_map[target_addr]
            tracknum_byte=tracknum.to_bytes(2,byteorder='big',signed=False)
            # print(tracknum_byte)
            timeof_appli_position=(time.time()) % 86400 
            timeof_appli_position_byte=(round(timeof_appli_position/(1/128))).to_bytes(3,byteorder='big',signed=False)
            # print( timeof_appli_position_byte)
            lat=entry["lat"]
            long = entry["lon"]
            position_byte=(round(lat/(180/2**30))).to_bytes(4,byteorder='big',signed=True)+(round(long/(180/2**30))).to_bytes(4,byteorder='big',signed=True)
            # print(position_byte)
            timeof_appli_velocity=(time.time()) % 86400 
            timeof_appli_velocity_byte=(round(timeof_appli_velocity/(1/128))).to_bytes(3,byteorder='big',signed=False)
            # print( timeof_appli_velocity_byte)
            # Assign or reuse track number
            target_addr_byte=target_addr.to_bytes(3,byteorder='big',signed=False)
            # print("target_addr_byte :",target_addr_byte)
            timeof_receptn_position=(time.time()) % 86400 
            timeof_receptn_position_byte=(round(timeof_receptn_position/(1/128))).to_bytes(3,byteorder='big',signed=False)
            # print( timeof_receptn_position_byte)
            geoheight = entry["geo_height"]
            geoheight_byte=(round(geoheight/6.25)).to_bytes(2,byteorder='big',signed=False)
            # print(geoheight_byte)
            flight_lvl=int(geoheight/100)
            flight_lvl_byte=(round(flight_lvl/(1/4))).to_bytes(2,byteorder='big',signed=False)
            # print(flight_lvl_byte)
            mag_heading = entry["mag_heading"]
            mag_heading_byte=(round(mag_heading/(360/2**16))).to_bytes(2,byteorder='big',signed=False)
            # print(mag_heading_byte)
            baro_ver_rate = entry["baro_rate"]
            baro_ver_rate_byte=((round(baro_ver_rate/6.25))&0x7fff).to_bytes(2,byteorder='big',signed=True)
            # print(baro_ver_rate_byte)
            geo_ver_rate=baro_ver_rate
            geo_ver_rate_byte=((round(geo_ver_rate/6.25))&0x7fff).to_bytes(2,byteorder='big',signed=True)
            # print("geo_ver_rate_byte :",geo_ver_rate_byte)
            msg_amp=81
            msg_amp_byte=msg_amp.to_bytes(1,byteorder='big',signed=False)
            # print(msg_amp_byte)
            packet=ds_iden_bytes+tracknum_byte+timeof_appli_position_byte+position_byte+timeof_appli_velocity_byte+target_addr_byte+timeof_receptn_position_byte+geoheight_byte+flight_lvl_byte+mag_heading_byte+baro_ver_rate_byte+geo_ver_rate_byte+msg_amp_byte
            print(packet)
            length=len(packet)
            # print(length)
            length_bytes=length.to_bytes(2,byteorder='big',signed=False)

            packet=cat_byte+length_bytes+fspec_bytes+ds_iden_bytes+tracknum_byte+timeof_appli_position_byte+position_byte+timeof_appli_velocity_byte+target_addr_byte+timeof_receptn_position_byte+geoheight_byte+flight_lvl_byte+mag_heading_byte+baro_ver_rate_byte+geo_ver_rate_byte+msg_amp_byte
            print(packet)
            # print("Hex Packet:", ' '.join(f'{byte:02x}' for byte in packet))

            sock.sendto(packet, (UDP_IP, UDP_PORT))
            print("Packet sent!")

            time.sleep(2)

except KeyboardInterrupt:
    print("\nStopped sending.")
    sock.close()
