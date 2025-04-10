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
tracknum=2004
tracknum_byte=tracknum.to_bytes(2,byteorder='big',signed=False)
# print(tracknum_byte)
timeof_appli_position=43574.94531
timeof_appli_position_byte=(round(timeof_appli_position/(1/128))).to_bytes(3,byteorder='big',signed=False)
# print( timeof_appli_position_byte)
lat=39.134628307043
long=-7.33791181817651
position_byte=(round(lat/(180/2**30))).to_bytes(4,byteorder='big',signed=True)+(round(long/(180/2**30))).to_bytes(4,byteorder='big',signed=True)
# print(position_byte)
timeof_appli_velocity=43574.94531
timeof_appli_velocity_byte=(round(timeof_appli_velocity/(1/128))).to_bytes(3,byteorder='big',signed=False)
# print( timeof_appli_velocity_byte)
target_addr=0x40797a
target_addr_byte=target_addr.to_bytes(3,byteorder='big',signed=False)
# print("target_addr_byte :",target_addr_byte)
timeof_receptn_position=43574.94531
timeof_receptn_position_byte=(round(timeof_receptn_position/(1/128))).to_bytes(3,byteorder='big',signed=False)
# print( timeof_receptn_position_byte)
geoheight=35950
geoheight_byte=(round(geoheight/6.25)).to_bytes(2,byteorder='big',signed=False)
# print(geoheight_byte)
flight_lvl=int(geoheight/100)
flight_lvl_byte=(round(flight_lvl/(1/4))).to_bytes(2,byteorder='big',signed=False)
# print(flight_lvl_byte)
mag_heading=243.98
mag_heading_byte=(round(mag_heading/(360/2**16))).to_bytes(2,byteorder='big',signed=False)
# print(mag_heading_byte)
baro_ver_rate=-62.5
baro_ver_rate_byte=((round(baro_ver_rate/6.25))&0x7fff).to_bytes(2,byteorder='big',signed=True)
# print(baro_ver_rate_byte)
geo_ver_rate=-62.5
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

import socket

UDP_IP = "127.0.0.1"   # Change to receiver's IP if needed
UDP_PORT = 5005        # Any unused port number

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(packet, (UDP_IP, UDP_PORT))
print("Packet sent!")
