import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('connections.csv')

# Convert timestamp to datetime
df['frame.time_epoch'] = pd.to_datetime(df['frame.time_epoch'], unit=>

# Group by unique connections
connections = df.groupby(['ip.src', 'ip.dst', 'tcp.srcport', 'tcp.dst>

# Initialize a list to store connection durations
connection_durations = []

# Calculate connection durations
for name, group in connections:
    syn_time = group[group['tcp.flags.syn'] == 1]['frame.time_epoch']>
    fin_time = group[group['tcp.flags.fin'] == 1]['frame.time_epoch']>
    rst_time = group[group['tcp.flags.reset'] == 1]['frame.time_epoch>
    ack_time = group[group['tcp.flags.ack'] == 1]['frame.time_epoch']>

    if pd.notnull(fin_time) and pd.notnull(ack_time):
        duration = (ack_time - syn_time).total_seconds()
    elif pd.notnull(rst_time):
        duration = (rst_time - syn_time).total_seconds()
    else:
        duration = 100  # Default duration

    connection_durations.append({
        'start_time': syn_time,
        'duration': duration,
        'source_ip': name[0],
        'destination_ip': name[1],
        'source_port': name[2],
        'destination_port': name[3]
    })

# Create a DataFrame for connection durations
duration_df = pd.DataFrame(connection_durations)

# Define the experiment start time
experiment_start_time = duration_df['start_time'].min()

# Convert start_time to seconds since experiment start
duration_df['elapsed_time'] = (duration_df['start_time'] - experiment>

# Plot connection durations
plt.figure(figsize=(10, 6))
plt.scatter(duration_df['elapsed_time'], duration_df['duration'], lab>
plt.axvline(x=20, color='r', linestyle='--', label='Attack Start')
plt.axvline(x=120, color='g', linestyle='--', label='Attack End')
plt.xlabel('Elapsed Time (seconds)')
plt.ylabel('Connection Duration (seconds)')
plt.legend()
plt.title('Connection Duration vs. Elapsed Time')
plt.show()
