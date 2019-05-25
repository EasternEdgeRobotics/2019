#!/usr/bin/env bash
# Micro ROV network bridge

# Create a new network bridge named zero
sudo ip link add name zero type bridge

# Change state of bridge and interfaces to up
sudo ip link set zero up
sudo ip link set eth0 up
sudo ip link set usb0 up

# Add the two interfaces to the bridge
sudo ip link set eth0 master zero
sudo ip link set usb0 master zero

# Assign the bridge an ip address
sudo ip addr add dev zero 192.168.88.50/24
