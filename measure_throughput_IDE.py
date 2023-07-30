import dpkt
import datetime

def calculate_throughput(pcap_file, interval):
    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        start_time = None
        end_time = None
        total_bytes = 0
        interval_start_time = None
        interval_bytes = 0

        for ts, buf in pcap:
            if start_time is None:
                start_time = ts
                interval_start_time = ts

            end_time = ts
            total_bytes += len(buf)

            if ts - interval_start_time >= interval:
                interval_throughput = (interval_bytes * 8) / (1024 * 1024)  # Megabits per second
                print(f"The throughput from {datetime.datetime.fromtimestamp(interval_start_time)} to {datetime.datetime.fromtimestamp(ts)} is {interval_throughput} Megabits per {interval} second(s).")
                interval_start_time = ts
                interval_bytes = 0
            else:
                interval_bytes += len(buf)

        time_delta = end_time - start_time
        throughput = (total_bytes * 8) / (1024 * 1024) / time_delta  # Megabits per second

        return throughput, start_time, end_time, time_delta

interval = 1 # Time interval in seconds
throughput, start_time, end_time, duration = calculate_throughput('ookla_speed_test.pcap', interval)
print(f"The average throughput of data in this file is {throughput} Megabits per second.")
print(f"The packet capture started at {datetime.datetime.fromtimestamp(start_time)} and ended at {datetime.datetime.fromtimestamp(end_time)}.")
print(f"The total duration of the packet capture was {duration} seconds.")
