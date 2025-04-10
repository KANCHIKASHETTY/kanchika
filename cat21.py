import struct

cat21 = "15"
length = "0023"
fspec = "AB9943B10120"
data_source_identification = "1413"
track_number = int(input("Enter Track Number (Decimal): "))
time_applicability_position = float(input("Enter Time of Applicability for Position (Seconds): "))
latitude = float(input("Enter High-Resolution Latitude in WGS84 (Decimal): "))
longitude = float(input("Enter High-Resolution Longitude in WGS84 (Decimal): "))
time_applicability_velocity = time_message_reception = time_applicability_position
target_address = input("Enter Target Address (HEX): ")
geometric_height = int(input("Enter Geometric Height (Feet): "))
barometric_vertical_rate = float(input("Enter Barometric Vertical Rate (Feet per Minute): "))
geometric_vertical_rate = barometric_vertical_rate
message_amplitude = int(input("Enter Message Amplitude (Decimal): "))
flight_level = geometric_height // 100

# Function to convert values to hex using LSB
def convert_to_hex(value, lsb, length, signed=False):
    scaled_value = round(value / lsb) 
    if signed:
        if length==1:
            fmt=">b"
        elif length==2:
            fmt=">h"
        else:
             fmt = ">i"  
    else:
        if length==1:
            fmt=">B"
        elif length==2:
            if not(0<=scaled_value<=65535):
                fmt=">I"
                fmt=">H"
        else:
             fmt = ">I"
    return struct.pack(fmt, scaled_value).hex().upper()

# Convert inputs to hex format
track_hex = f"{track_number:04X}"
time_pos_hex = convert_to_hex(time_applicability_position, 1/128, 3)
lat_hex = convert_to_hex(latitude, 180/(2**30), 4, signed=True)
lon_hex = convert_to_hex(longitude, 180/(2**30), 4, signed=True)
time_vel_hex = convert_to_hex(time_applicability_velocity, 1/128, 3)
geo_alt_hex = convert_to_hex(geometric_height, 25, 2, signed=True)
flight_level_hex = convert_to_hex(flight_level, 1, 2)  # Direct mapping
baro_vert_rate_hex = convert_to_hex(barometric_vertical_rate, 6.25, 2, signed=True)
geo_vert_rate_hex = convert_to_hex(geometric_vertical_rate, 6.25, 2, signed=True)
msg_amp_hex = f"{message_amplitude:02X}"

# Fixed Magnetic Heading (243.98 degrees → AD 7F)
magnetic_heading_hex = "AD7F"

# Assemble the final CAT21 packet
final_packet = (
    cat21 + length + fspec + data_source_identification + track_hex + time_pos_hex +
    lat_hex + lon_hex + time_vel_hex + target_address + time_message_reception + 
    geo_alt_hex + flight_level_hex + baro_vert_rate_hex + geo_vert_rate_hex +
    magnetic_heading_hex + msg_amp_hex
)

# Print final hex packet
print("\nFinal CAT 21 Packet (Hex):")
print(" ".join(final_packet[i:i+2] for i in range(0, len(final_packet), 2)))
