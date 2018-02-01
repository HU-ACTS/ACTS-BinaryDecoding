#!/usr/bin/env python3
import argparse
import struct
import csv
import os
from timeit import default_timer as timer

argstring = argparse.ArgumentParser(description='Decode Binary measurements file into CSV output.')
argstring.add_argument('-i', '--path_in', help='input path with binary files. (SD card)')
argstring.add_argument('-o', '--path_out', help='Output folder for decoded CSV files.')

args = vars(argstring.parse_args())

input_path = args["path_in"]
output_path = args["path_out"]

if not os.path.exists(output_path):
    os.mkdir(output_path)

filenames = []
for file in os.listdir(input_path):
    if file.endswith(".bin"):
        filenames.append(file)

print('Input folder:', input_path)
print('Output folder:', output_path)
print('Decoding measurements, please wait...')
print(len(filenames), " bin files found")

start = timer()

for file_count in range(0, len(filenames)):

    print("Progress: file", file_count+1, "/", len(filenames))

    input_file = os.path.join(input_path, filenames[file_count])
    output_file = os.path.join(output_path, os.path.splitext(filenames[file_count])[0])
    output_file += '.csv'
#    output_file = "C:\DecodedACTS\measurements.csv"

    try:
        open(output_file, 'w').close()  # empty file before writing
    except PermissionError:
        print("Error: Output file is in use by another program!")
        exit(1)

    try:
        binfile = open(input_file, "rb")
    except IOError:
        print("Error opening input file!")
        exit(1)

    csvfile = open(output_file, 'a', newline='')
    wr = csv.writer(csvfile, dialect='excel')
    csvRow = ["time", "accX", "accY", "accZ", "gyrX", "gyrY", "gyrZ", "magX", "magY", "magZ", "temp", "pres"]
    wr.writerow(csvRow)  # Write csv header

    while True:
        bytes_time = binfile.read(8)
        bytes_accX = binfile.read(2)
        bytes_accY = binfile.read(2)
        bytes_accZ = binfile.read(2)
        bytes_gyrX = binfile.read(2)
        bytes_gyrY = binfile.read(2)
        bytes_gyrZ = binfile.read(2)
        bytes_magX = binfile.read(2)
        bytes_magY = binfile.read(2)
        bytes_magZ = binfile.read(2)
        bytes_temp = binfile.read(4)
        bytes_pres = binfile.read(4)
        binfile.read(6)

        if len(bytes_time) == 0:
            break

        time = struct.unpack("<q", bytes_time)[0]
        accX = struct.unpack("<h", bytes_accX)[0]
        accY = struct.unpack("<h", bytes_accY)[0]
        accZ = struct.unpack("<h", bytes_accZ)[0]
        gyrX = struct.unpack("<h", bytes_gyrX)[0]
        gyrY = struct.unpack("<h", bytes_gyrY)[0]
        gyrZ = struct.unpack("<h", bytes_gyrZ)[0]
        magX = struct.unpack("<h", bytes_magX)[0]
        magY = struct.unpack("<h", bytes_magY)[0]
        magZ = struct.unpack("<h", bytes_magZ)[0]
        temp = struct.unpack("<I", bytes_temp)[0]
        pres = struct.unpack("<I", bytes_pres)[0]

        # print("Time:", time)
        # print("accX:", accX)
        # print("accY:", accY)
        # print("accZ:", accZ)
        # print("gyrX:", gyrX)
        # print("gyrY:", gyrY)
        # print("gyrZ:", gyrZ)
        # print("magX:", magX)
        # print("magY:", magY)
        # print("magZ:", magZ)
        # print("Temp:", temp)
        # print("Pres:", pres)

        csvRow = [time, accX, accY, accZ, gyrX, gyrY, gyrZ, magX, magY, magZ, temp, pres]
        wr.writerow(csvRow)

    binfile.close()
    csvfile.close()

end = timer()
print('Execution time: ', round(end - start, 1), "s")
print('Finished!')
exit(0)