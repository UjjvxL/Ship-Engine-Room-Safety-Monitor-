import serial
import time
import csv
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import re
import datetime

# --- CONFIGURATION ---
COM_PORT = 'COM16'  # CHANGE THIS to your STM32 COM port (e.g., '/dev/ttyUSB0' on Linux/Mac)
BAUD_RATE = 115200

# --- GLOBAL VARIABLES ---
logging_enabled = False
csv_filename = ""

# Deques store the last 50 data points for rolling graphs
time_data = deque(maxlen=50)
dist_data = deque(maxlen=50)
temp_data = deque(maxlen=50)

latest_gas = "WAIT"
latest_mode = "WAIT"
start_time = time.time()

# --- THREAD 1: SERIAL READER & LOGGER ---
def serial_thread():
    global latest_gas, latest_mode, logging_enabled
    
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {COM_PORT} at {BAUD_RATE} baud.")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                # Print human-readable output to terminal
                print(f"Received: {line}")
                
                # Regex to extract data from [DIST:x|TEMP:x|GAS:x|MODE:x]
                match = re.search(r'\[DIST:(\d+)\|TEMP:([\d\.]+)\|GAS:(\w+)\|MODE:(\w+)\]', line)
                if match:
                    dist_val = int(match.group(1))
                    temp_val = float(match.group(2))
                    latest_gas = match.group(3)
                    latest_mode = match.group(4)
                    
                    current_t = time.time() - start_time
                    
                    # Update arrays for the plot
                    time_data.append(current_t)
                    dist_data.append(dist_val)
                    temp_data.append(temp_val)
                    
                    # Log to CSV if enabled
                    if logging_enabled:
                        with open(csv_filename, mode='a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([datetime.datetime.now().strftime("%H:%M:%S.%f"), dist_val, temp_val, latest_gas, latest_mode])
        except Exception as e:
            pass

# --- THREAD 2: TERMINAL INPUT LISTENER ---
def input_thread():
    global logging_enabled, csv_filename
    print("\n--- Type 'LOG' to start/stop saving data to CSV ---")
    
    while True:
        user_input = input().strip().upper()
        if user_input == "LOG":
            logging_enabled = not logging_enabled
            if logging_enabled:
                csv_filename = f"sensor_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                # Write CSV header
                with open(csv_filename, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Timestamp", "Distance_cm", "Temp_C", "Gas_Status", "System_Mode"])
                print(f"\n[!] LOGGING STARTED: Saving to {csv_filename}")
            else:
                print(f"\n[!] LOGGING STOPPED.")

# --- MAIN: MATPLOTLIB DASHBOARD ---
def update_plot(frame):
    # Clear the subplots
    ax1.cla()
    ax2.cla()

    # Plot Distance
    ax1.plot(time_data, dist_data, color='cyan', linewidth=2)
    ax1.set_title("Ultrasonic Distance (cm)", color='white')
    ax1.set_ylim(0, 200) # Adjust max distance if needed
    
    # Plot Temperature
    ax2.plot(time_data, temp_data, color='orange', linewidth=2)
    ax2.set_title("DS18B20 Temperature (°C)", color='white')
    # ax2.set_ylim(20, 50) # Uncomment to fix Y axis for temp

    # Style the plots for a dark dashboard look
    for ax in [ax1, ax2]:
        ax.set_facecolor('#222222')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        for spine in ax.spines.values():
            spine.set_color('#555555')

    # Update Text Labels for Gas and Mode
    fig.suptitle(f"ENGINE ROOM DASHBOARD\nMODE: {latest_mode} | GAS: {latest_gas}", 
                 color='red' if latest_mode == 'EMERGENCY' else ('yellow' if latest_mode == 'HAZARD' else 'lightgreen'), 
                 fontsize=16, fontweight='bold')

# Setup Dashboard Figure
plt.style.use('dark_background')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
fig.canvas.manager.set_window_title('Engine Room Live Telemetry')
plt.subplots_adjust(hspace=0.4, top=0.85)

# Start background threads
t_serial = threading.Thread(target=serial_thread, daemon=True)
t_input = threading.Thread(target=input_thread, daemon=True)
t_serial.start()
t_input.start()

# Start Matplotlib animation (must run in main thread)
ani = FuncAnimation(fig, update_plot, interval=250, cache_frame_data=False)
plt.show()