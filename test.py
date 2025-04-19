import time
import socket
import threading
import queue
import random

# Shared queue to simulate integration
data_queue = queue.Queue()

# Simulated friend's code: prints (but actually stores) output dictionaries
def simulate_friend_output():
    while True:
        info = {
            "lat": random.uniform(-90, 90),
            "lon": random.uniform(-180, 180),
            "geo_height": random.randint(10000, 40000),
            "baro_rate": random.uniform(-100, 100),
            "mag_heading": random.uniform(0, 360),
            "target_addr": random.randint(0x000000, 0xFFFFFF)
        }
        print("Friend Output:", info)  # simulate print only
        data_queue.put(info)  # store in shared queue
        time.sleep(random.uniform(0.3, 1.0))  # simulate 2-3 per second

def generate_fspec_from_fields(fields_present):
    max_id = max(fields_present)
    num_bytes = (max_id + 6) // 7
    fspec_bits = ["0"] * (num_bytes * 8)
    for field_id in fields_present:
        bit_index = field_id - 1
        byte_index = bit_index // 7
        bit_in_byte = bit_index % 7
        fspec_bits[byte_index * 8 + bit_in_byte] = "1"
    for i in range(num_bytes - 1):
        fspec_bits[(i + 1) * 8 - 1] = "1"
    fspec_bytes = bytearray()
    for i in range(num_bytes):
        byte_bits = fspec_bits[i * 8:(i + 1) * 8]
        fspec_bytes.append(int("".join(byte_bits), 2))
    return bytes(fspec_bytes)

# Your code: packet creation and sending
def process_and_send_packets():
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5101

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton("192.168.1.57"))

    track_map = {}
    track_counter = 1

    while True:
        if not data_queue.empty():
            entry = data_queue.get()
            try:
                fields_present = []
                packet=b''
                cat=21
                cat_byte=cat.to_bytes(1,byteorder='big',signed=False)
                # print(cat_byte)
                sac=0x14
                sic=0x13
                ds_iden_bytes=(sac.to_bytes(1,byteorder='big',signed=False))+(sic.to_bytes(1,byteorder='big',signed=False))
                fields_present.append(1)
                # print("ds_iden_bytes :",ds_iden_bytes)
                target_addr = entry["target_addr"]
                if target_addr not in track_map:
                    track_map[target_addr] = track_counter
                    track_counter += 1
                tracknum = track_map[target_addr]
                tracknum_byte=tracknum.to_bytes(2,byteorder='big',signed=False)
                fields_present.append(3)
                # print(tracknum_byte)
                timeof_appli_position=(time.time()) % 86400 
                timeof_appli_position_byte=(round(timeof_appli_position/(1/128))).to_bytes(3,byteorder='big',signed=False)
                fields_present.append(5)
                # print( timeof_appli_position_byte)
                lat=entry["lat"]
                long = entry["lon"]
                position_byte=(round(lat/(180/2**30))).to_bytes(4,byteorder='big',signed=True)+(round(long/(180/2**30))).to_bytes(4,byteorder='big',signed=True)
                fields_present.append(7)
                # print(position_byte)
                timeof_appli_velocity=(time.time()) % 86400 
                timeof_appli_velocity_byte=(round(timeof_appli_velocity/(1/128))).to_bytes(3,byteorder='big',signed=False)
                fields_present.append(8)
                # print( timeof_appli_velocity_byte)
                # Assign or reuse track number
                target_addr_byte=target_addr.to_bytes(3,byteorder='big',signed=False)
                fields_present.append(11)
                # print("target_addr_byte :",target_addr_byte)
                timeof_receptn_position=(time.time()) % 86400 
                timeof_receptn_position_byte=(round(timeof_receptn_position/(1/128))).to_bytes(3,byteorder='big',signed=False)
                fields_present.append(12)
                # print( timeof_receptn_position_byte)
                geoheight = entry["geo_height"]
                geoheight_byte=(round(geoheight/6.25)).to_bytes(2,byteorder='big',signed=False)
                fields_present.append(16)
                # print(geoheight_byte)
                flight_lvl=int(geoheight/100)
                flight_lvl_byte=(round(flight_lvl/(1/4))).to_bytes(2,byteorder='big',signed=False)
                fields_present.append(21)
                # print(flight_lvl_byte)
                mag_heading = entry["mag_heading"]
                mag_heading_byte=(round(mag_heading/(360/2**16))).to_bytes(2,byteorder='big',signed=False)
                fields_present.append(22)
                # print(mag_heading_byte)
                baro_ver_rate = entry["baro_rate"]
                baro_ver_rate_byte=((round(baro_ver_rate/6.25))&0x7fff).to_bytes(2,byteorder='big',signed=True)
                fields_present.append(24)
                # print(baro_ver_rate_byte)
                geo_ver_rate=baro_ver_rate
                geo_ver_rate_byte=((round(geo_ver_rate/6.25))&0x7fff).to_bytes(2,byteorder='big',signed=True)
                fields_present.append(25)
                # print("geo_ver_rate_byte :",geo_ver_rate_byte)
                msg_amp=81
                msg_amp_byte=msg_amp.to_bytes(1,byteorder='big',signed=False)
                fields_present.append(38)
                # print(msg_amp_byte)
                packet_body=ds_iden_bytes+tracknum_byte+timeof_appli_position_byte+position_byte+timeof_appli_velocity_byte+target_addr_byte+timeof_receptn_position_byte+geoheight_byte+flight_lvl_byte+mag_heading_byte+baro_ver_rate_byte+geo_ver_rate_byte+msg_amp_byte
                # print(packet_body)
                fspec_bytes= generate_fspec_from_fields(fields_present)
                print(fspec_bytes.hex())
                length = len(packet_body) + len(fspec_bytes)
                print(length)
                length_bytes=length.to_bytes(2,byteorder='big',signed=False)


                packet=cat_byte+length_bytes+fspec_bytes+packet_body
                print(packet)
                print("Hex Packet:", ' '.join(f'{byte:02x}' for byte in packet))

                sock.sendto(packet, (UDP_IP, UDP_PORT))
                print("Packet sent!")

            except Exception as e:
                print(f"Error while sending: {e}")
        else:
            time.sleep(0.01)  # reduce CPU usage when queue is empty

# Start both threads
threading.Thread(target=simulate_friend_output, daemon=True).start()
threading.Thread(target=process_and_send_packets, daemon=True).start()

# Keep main thread alive
while True:
    time.sleep(1)

            