from scapy.all import *
from collections import defaultdict
import statistics
from scapy.layers.http import HTTP
from scapy.contrib.lldp import *
import pandas as pd

import sys


def get_app_protocol(pkt):
    # Check for known protocols first
    if hex(pkt[Ether].type) == 0x88CC:
        return "LLDP"
    if pkt.haslayer(HTTP):
        return "HTTP"
    elif pkt.haslayer(DNS):
        return "DNS"
    elif pkt.haslayer(TCP) and pkt[TCP].dport == 25:
        return "SMTP"
    elif pkt.haslayer(TCP) and (pkt[TCP].dport == 22 or pkt[TCP].sport == 22 ) :
        return "SSH"
    elif pkt.haslayer(TCP) and (pkt[TCP].dport == 21 or pkt[TCP].sport == 21):
        return "FTP"
    else:
        # Fall back to the last layer's name if no known protocol is found
        return pkt.lastlayer().name

def analyze_bidirectional_flows(pcap_file, max_packets_per_flow=80):
    # Read the PCAP file
    packets = rdpcap(pcap_file)
    
    # Dictionary to store bidirectional flows
    flows = defaultdict(list)


    # Iterate through packets and group them into bidirectional flows
    for packet in packets:
    #    if Ether in packet and IP in packet:
        src_mac = packet[Ether].src
        dst_mac = packet[Ether].dst
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
        else:
            src_ip = "NO"
            dst_ip = "NO"
        protocol = get_app_protocol(packet)
        # Create a unique flow identifier
        flow_id = tuple(sorted([(src_mac, src_ip), (dst_mac, dst_ip)]) + [protocol])
        
        flows[flow_id].append(packet)
        
        if (protocol == "Raw"):
            print (packet.show())

            # If we have max_packets_per_flow packets in this flow, yield it
        if len(flows[flow_id]) == max_packets_per_flow:
            yield flows[flow_id]
            del flows[flow_id]

    # Yield any remaining flows
    for flow_packets in flows.values():
        if flow_packets:
            yield flow_packets

# file to analize
pcap_file = sys.argv[0]
#pcap_file = "syn_flood_capture.pcap"
# Process flows
flow_data = list(analyze_bidirectional_flows(pcap_file))

# Print results
print(f"Number of bidirectional flows: {len(flow_data)}")

df = pd.DataFrame(columns = ['fw_packets','bk_packets', 'protocol',
              'src_MAC', 'dst_MAC', 'src_IP', 'dst_IP', 
              'fw_bytes', 'bk_bytes', 'fw_bytes_mean', 'fw_bytes_median',
              'fw_bytes_stddev',  'bk_bytes_mean', 'bk_bytes_median',
              'bk_bytes_stddev'])


# Print information about each flow
for i, flow_packets in enumerate(flow_data):
    print(f"\nFlow {i+1}:")
    
    # Separate packets by direction
    first_src_eth = flow_packets[0][Ether].src
    forward_packets = [p for p in flow_packets if p[Ether].src == first_src_eth]
    backward_packets = [p for p in flow_packets if p[Ether].src != first_src_eth]
    
    # Calculate byte statistics
    forward_bytes = [len(p) for p in forward_packets]
    backward_bytes = [len(p) for p in backward_packets]
    
    print(f"  Protocol: {get_app_protocol(flow_packets[0])}")
    print(f"  Number of packets: {len(flow_packets)} (Forward: {len(forward_packets)}, Backward: {len(backward_packets)})")
    print(f"  Source MAC: {flow_packets[0][Ether].src}, Destination MAC: {flow_packets[0][Ether].dst}")
    
    df.loc[i, "protocol"]=get_app_protocol(flow_packets[0])
    df.loc[i,"fw_packets"]=len(forward_packets)
    df.loc[i,"bk_packets"]=len(backward_packets) 
    df.loc[i,"dst_MAC"]=len(flow_packets[0][Ether].dst) 
    df.loc[i,"src_MAC"]=len(flow_packets[0][Ether].src) 

    try: 
        df.loc[i, "src_IP"]=flow_packets[0][IP].src
        df.loc[i, "dst_IP"]=flow_packets[0][IP].dst
        print(f"  Source IP: {flow_packets[0][IP].src}, Destination IP: {flow_packets[0][IP].dst}")
    except:
        df.loc[i, "src_IP"]='0'
        df.loc[i, "dst_IP"]='0'
        print("No ip address")

    print("  Byte statistics:")
    if len(forward_bytes) > 1:
        print(f"    Forward - Total: {sum(forward_bytes)}, Mean: {statistics.mean(forward_bytes):.2f}, Median: {statistics.median(forward_bytes):.2f}")
        print(f"               Std Dev: {statistics.stdev(forward_bytes):.2f}")
        df.loc[i, "fw_bytes"]=sum(forward_bytes)
        df.loc[i, "fw_bytes_mean"]=statistics.mean(forward_bytes)
        df.loc[i, "fw_bytes_median"]=statistics.median(forward_bytes)
        df.loc[i, "fw_bytes_stddev"]=statistics.stdev(forward_bytes)
    else:
        df.loc[i, "fw_bytes"]='0'
        df.loc[i, "fw_bytes_mean"]='0'
        df.loc[i, "fw_bytes_median"]='0'
        df.loc[i, "fw_bytes_stddev"]='0'


    
    if len(backward_bytes) > 1:
        print(f"    Backward - Total: {sum(backward_bytes)}, Mean: {statistics.mean(backward_bytes):.2f}, Median: {statistics.median(backward_bytes):.2f}")
        print(f"                Std Dev: {statistics.stdev(backward_bytes):.2f}")
        df.loc[i, "bk_bytes"]=sum(backward_bytes)
        df.loc[i, "bk_bytes_mean"]=statistics.mean(backward_bytes)
        df.loc[i, "bk_bytes_median"]=statistics.median(backward_bytes)
        df.loc[i, "bk_bytes_stddev"]=statistics.stdev(backward_bytes)
    else:
        df.loc[i, "bk_bytes"]='0'
        df.loc[i, "bk_bytes_mean"]='0'
        df.loc[i, "bk_bytes_median"]='0'
        df.loc[i, "bk_bytes_stddev"]='0'

    
    
    

# Print total number of Ethernet frames
total_frames = sum(len(flow) for flow in flow_data)
print(f"\nTotal Ethernet frames: {total_frames}")
df.to_csv('flows.csv')