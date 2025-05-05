# UNPLUGGED
| | | | | |
| | | |_ **_** *_* *_* | | ___ * *___
| | | | '_ \ / * \ '*_| '_ \| |/ * \| | | / *_|
| |__| | | | | __/ | | |_) | | (_) | |_| \__ \
\____/|*_| |_*|\___|*_| | .***__/|***_|\___***/ \__,***_|_***__***/*
*| |*
*|_*| v1.0 - Ubuntu Wi-Fi Deauth Script

## About
Simple Python script for Ubuntu that disconnects devices from Wi-Fi networks using deauthentication packets.

**WARNING:** Educational purposes only. Unauthorized use is illegal.

## Features
- Auto-detects wireless adapter
- Changes MAC address for privacy
- Scans Wi-Fi networks and connected devices
- Sends deauth packets to disconnect targets

## Required Setup

```bash
# Install driver if using RTL8812AU
sudo apt install dkms
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install

# Enable monitor mode
sudo systemctl stop NetworkManager
sudo airmon-ng check kill
sudo airmon-ng start wlan0  # Replace wlan0 with your interface
```

## Usage

```bash
# Clone and run
git clone https://github.com/purposewalks9/unplugged.git
cd unplugged
chmod +x unplugged.py
sudo python3 unplugged.py

# After using, restore network
sudo airmon-ng stop wlan0mon  # Your monitor interface
sudo systemctl start NetworkManager
```

## Script Process
1. Installs dependencies (aircrack-ng, macchanger, net-tools)
2. Finds wireless adapter
3. Changes MAC to 00:11:22:33:44:55
4. Scans networks for 20 seconds → Data-01.csv
5. Asks for target network (BSSID + channel)
6. Scans for connected devices → targets_devices-01.csv
7. Asks which device to deauth
8. Sends deauth packets

## Compatible Adapters
- Realtek RTL8812AU
- Alfa AWUS036ACH
- TP-Link Archer T2U Plus
- Any with monitor mode + packet injection

## Contact
github.com/purposewalks9/unplugged