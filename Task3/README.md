"# Task 3" 
# Task 3: Effect of Nagle’s Algorithm on TCP/IP Performance

## Overview
This task analyzes the impact of Nagle’s Algorithm and Delayed-ACK on TCP/IP performance by transmitting a 4 KB file over a TCP connection for approximately 2 minutes at a transfer rate of 40 bytes/second. The experiment involves four different configurations by enabling/disabling Nagle’s Algorithm and Delayed-ACK on both the sender and receiver.

## Experimental Setup
- A single VM is used with two terminal windows: one for the receiver and one for the sender.
- Packet transfers are captured using `tcpdump` and analyzed in Wireshark.

## Commands Used
### **Step 1: Create a 4 KB File**
```bash
 dd if=/dev/urandom of=file_to_send bs=1024 count=4
```

### **Step 2: Start Receiver (Listening for Incoming File)**
```bash
nc -l -p 12345 > received_file
```

### **Step 3: Start Sender (Transfer File at 40 Bytes/sec)**
```bash
pv -L 40 file_to_send | nc 127.0.0.1 12345
```

### **Step 4: Capture Packet Transfers**
```bash
sudo tcpdump -i lo port 12345 -w tcpdump_caseX.pcap
```
Replace `X` with the corresponding case number (1, 2, 3, or 4).

---
## Configurations for Four Cases

### **1. Nagle’s Algorithm Enabled, Delayed-ACK Enabled**
```bash
# Enable Nagle's Algorithm
sudo sysctl -w net.ipv4.tcp_low_latency=0

# Enable Delayed ACK
sudo sysctl -w net.ipv4.tcp_backlog_ack_defer=1
```

### **2. Nagle’s Algorithm Enabled, Delayed-ACK Disabled**
```bash
# Enable Nagle's Algorithm
sudo sysctl -w net.ipv4.tcp_low_latency=0

# Disable Delayed ACK
sudo sysctl -w net.ipv4.tcp_backlog_ack_defer=0
```

### **3. Nagle’s Algorithm Disabled, Delayed-ACK Enabled**
```bash
# Disable Nagle's Algorithm
sudo sysctl -w net.ipv4.tcp_low_latency=1

# Enable Delayed ACK
sudo sysctl -w net.ipv4.tcp_backlog_ack_defer=1
```

### **4. Nagle’s Algorithm Disabled, Delayed-ACK Disabled**
```bash
# Disable Nagle's Algorithm
sudo sysctl -w net.ipv4.tcp_low_latency=1

# Disable Delayed ACK
sudo sysctl -w net.ipv4.tcp_backlog_ack_defer=0
```

---
## **Performance Metrics Measured**
For each configuration, the following performance metrics are analyzed:
1. **Throughput** – The rate of successful data transfer.
2. **Goodput** – The useful application-level data successfully transmitted.
3. **Packet Loss Rate** – The percentage of lost packets during transmission.
4. **Maximum Packet Size Achieved** – The largest TCP segment transmitted without fragmentation.

---
## **Expected Observations**
- **Case 1 (Both Enabled)**: More efficient transmission, but increased latency due to waiting for delayed ACKs.
- **Case 2 (Nagle Enabled, Delayed-ACK Disabled)**: Small packets might accumulate, leading to occasional bursts of transmission.
- **Case 3 (Nagle Disabled, Delayed-ACK Enabled)**: Frequent transmission of small packets, potentially lowering efficiency.
- **Case 4 (Both Disabled)**: Minimal latency, but increased overhead due to more frequent transmissions.

Captured packet data (`.pcap` files) can be analyzed using Wireshark to validate results.

---
## **Conclusion**
By comparing throughput, goodput, and packet loss across all four cases, we gain insights into how Nagle’s Algorithm and Delayed-ACK affect TCP/IP performance under different conditions. The results highlight trade-offs between efficiency, latency, and network overhead.

