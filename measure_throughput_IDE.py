# Author: Daryl Allen
#
#

# Import necessary libraries
import dpkt
import datetime

# Define function to calculate throughput
def calculate_throughput(pcap_file, interval):
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

# Set the time interval in seconds
interval = 1 
# Calculate the throughput and print the results
throughput, start_time, end_time, duration = calculate_throughput('ookla_speed_test.pcap', interval)
print(f"The average throughput of data in this file is {throughput} Megabits per second.")
print(f"The packet capture started at {datetime.datetime.fromtimestamp(start_time)} and ended at {datetime.datetime.fromtimestamp(end_time)}.")
print(f"The total duration of the packet capture was {duration} seconds.")
