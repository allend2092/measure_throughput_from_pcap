# Author: Daryl Allen
# This code is designed to be run in an IDE.
# Set the pcap_file and interval variables below.

# Import necessary libraries
from scapy.all import rdpcap
import datetime
import sys

# Set the pcap_file and interval here
pcap_file = 'Four_merged_files_merged_last_part_slow.pcapng'  # Replace with your pcapng file name
interval = 1  # Replace with your desired interval in seconds

# Define function to calculate throughput
def calculate_throughput(pcap_file, interval):
    try:
        # Read the pcapng file using Scapy
        packets = rdpcap(pcap_file)
        # Initialize variables
        start_time = None
        end_time = None
        total_bytes = 0
        interval_start_time = None
        interval_bytes = 0

        # Iterate over each packet in the pcapng file
        for packet in packets:
            # Get the timestamp of the packet and convert to float
            ts = float(packet.time)
            # Get the length of the packet and convert to int
            pkt_len = int(len(packet))

            # If this is the first packet, set the start time
            if start_time is None:
                start_time = ts
                interval_start_time = ts

            # Update the end time and total bytes
            end_time = ts
            total_bytes += pkt_len
            interval_bytes += pkt_len

            # If the current time minus the interval start time is greater than or equal to the interval
            if ts - interval_start_time >= interval:
                # Calculate the interval duration
                interval_duration = ts - interval_start_time
                # Calculate the throughput for the interval
                interval_throughput = (interval_bytes * 8) / (interval_duration * 1_000_000)  # Megabits per second
                # Print the throughput
                print(f"The throughput from {datetime.datetime.fromtimestamp(interval_start_time)} to {datetime.datetime.fromtimestamp(ts)} is {interval_throughput:.2f} Megabits per second over {interval_duration:.2f} seconds.")
                # Reset the interval start time and interval bytes
                interval_start_time = ts
                interval_bytes = 0

        # Handle any remaining bytes in the last interval
        if interval_bytes > 0:
            interval_duration = end_time - interval_start_time
            interval_throughput = (interval_bytes * 8) / (interval_duration * 1_000_000)  # Megabits per second
            print(f"The throughput from {datetime.datetime.fromtimestamp(interval_start_time)} to {datetime.datetime.fromtimestamp(end_time)} is {interval_throughput:.2f} Megabits per second over {interval_duration:.2f} seconds.")

        # Calculate the total time delta and the average throughput
        time_delta = end_time - start_time
        throughput = (total_bytes * 8) / (time_delta * 1_000_000)  # Megabits per second

        # Return the throughput, start_time, end_time, and duration
        return throughput, start_time, end_time, time_delta
    except FileNotFoundError:
        print(f"Error: The file '{pcap_file}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while processing the pcapng file: {e}")
        sys.exit(1)

# Calculate the throughput and print the results
throughput, start_time, end_time, duration = calculate_throughput(pcap_file, interval)
if throughput:
    print(f"\nThe average throughput of data in this file is {throughput:.2f} Megabits per second.")
    print(f"The packet capture started at {datetime.datetime.fromtimestamp(start_time)} and ended at {datetime.datetime.fromtimestamp(end_time)}.")
    print(f"The total duration of the packet capture was {duration:.2f} seconds.")
