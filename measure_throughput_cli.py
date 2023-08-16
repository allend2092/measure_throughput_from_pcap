# Author: Daryl Allen
# This code is meant to be run in the CLI and takes two parameters. First, the packet capture file, second, the time interval.

# Import necessary libraries
import dpkt
import datetime
import argparse
import sys

# Define function to calculate throughput
def calculate_throughput(pcap_file, interval):
    try:
        # Open the pcap file
        with open(pcap_file, 'rb') as f:
            pcap = dpkt.pcap.Reader(f)
            # Initialize variables
            start_time = None
            end_time = None
            total_bytes = 0
            interval_start_time = None
            interval_bytes = 0

            # Iterate over each packet in the pcap file
            for ts, buf in pcap:
                # If this is the first packet, set the start time
                if start_time is None:
                    start_time = ts
                    interval_start_time = ts

                # Update the end time and total bytes
                end_time = ts
                total_bytes += len(buf)

                # If the current time minus the interval start time is greater than or equal to the interval
                if ts - interval_start_time >= interval:
                    # Calculate the throughput for the interval
                    interval_throughput = (interval_bytes * 8) / (1024 * 1024)  # Megabits per second
                    # Print the throughput
                    print(f"The throughput from {datetime.datetime.fromtimestamp(interval_start_time)} to {datetime.datetime.fromtimestamp(ts)} is {interval_throughput} Megabits per {interval} second(s).")
                    # Reset the interval start time and interval bytes
                    interval_start_time = ts
                    interval_bytes = 0
                else:
                    # If the current time minus the interval start time is less than the interval, add the bytes of the current packet to the interval bytes
                    interval_bytes += len(buf)

            # Calculate the total time delta and the average throughput
            time_delta = end_time - start_time
            throughput = (total_bytes * 8) / (1024 * 1024) / time_delta  # Megabits per second

            # Return the throughput, start time, end time, and duration
            return throughput, start_time, end_time, time_delta
    except FileNotFoundError:
        print(f"Error: The file '{pcap_file}' was not found.")
        sys.exit(1)
    except dpkt.dpkt.NeedData:
        print("Error: The pcap file appears to be corrupted or incomplete.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

# Set up argument parser
parser = argparse.ArgumentParser(description='Calculate network throughput from a pcap file.')
# Add arguments for the pcap file and the interval
parser.add_argument('pcap_file', type=str, help='The name of the pcap file.')
parser.add_argument('interval', type=int, help='The time interval in seconds at which to calculate the throughput.')

# Parse the arguments
try:
    args = parser.parse_args()
except argparse.ArgumentError as e:
    print(f"Error: {e}")
    sys.exit(1)

# Calculate the throughput and print the results
throughput, start_time, end_time, duration = calculate_throughput(args.pcap_file, args.interval)
if throughput:
    print(f"The average throughput of data in this file is {throughput} Megabits per second.")
    print(f"The packet capture started at {datetime.datetime.fromtimestamp(start_time)} and ended at {datetime.datetime.fromtimestamp(end_time)}.")
    print(f"The total duration of the packet capture was {duration} seconds.")
