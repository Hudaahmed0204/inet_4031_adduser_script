#!/usr/bin/python3
import os
import sys

# Read each line from STDIN (the input file)
for line in sys.stdin:
    # Remove newline characters and spaces
    line = line.strip()
    if not line:
        continue

    # Skip commented lines (lines starting with #)
    if line.startswith("#"):
        print("[SKIP] Comment line detected.")
        continue

    # Split each line into fields separated by colons
    fields = line.split(":")
    if len(fields) < 5:
        print("[ERROR] Not enough fields ->", line)
        continue

    username = fields[0]
    password = fields[1]
    lastname = fields[2]
    firstname = fields[3]
    groups = fields[4]

    # Display what the program will do (for Dry-Run)
    print(f"\n[INFO] Creating user: {username}")
    print(f"Full Name: {firstname} {lastname}")
    print(f"Groups: {groups}")

    # OS commands to create users and groups
    # Comment these out for Dry-Run mode
    os.system(f"sudo useradd -m -c '{firstname} {lastname}' {username}")
    os.system(f"echo '{username}:{password}' | sudo chpasswd")

    # If groups are listed, add user to them
    if groups != "-":
        for g in groups.split(","):
            os.system(f"sudo groupadd -f {g}")
            os.system(f"sudo usermod -aG {g} {username}")
