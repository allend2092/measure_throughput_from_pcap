# measure_throughput_from_pcap
measure_throughput_from_pcap


Includes two python scripts that measure network throughput based on a packet capture file read into the script. One version of the script is made to be run in an IDE where you can edit the variables. The other version is made to be run at the command line. It accepts two variables, the pcap file and the time interval of packet data. 

You'll need to pip install the following packages:
import dpkt
import datetime
import argparse

dpkt only works on .pcap files, not .pcapng (packet capture next generation)

If you're running a linux system you can convert pcapng to pcap with the following command:
editcap -F libpcap input.pcapng output.pcap

To run the tool at the CLI:
python3 measure_throughput_cli.py [file name].pcap 1
