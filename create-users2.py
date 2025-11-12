#!/usr/bin/python3
import os
import sys

# NOTE: We must prompt from the real keyboard even when STDIN is redirected
# so we read the Y/N answer from /dev/tty (the terminal) instead of STDIN.
def ask_dry_run() -> bool:
    try:
        with open("/dev/tty", "r") as tty:
            print("Run in dry-run mode? (Y to dry-run, N to run normally): ", end="", flush=True)
            ans = tty.readline().strip().lower()
            return ans.startswith("y")
    except Exception:
        # Fallback: if /dev/tty not available, default to dry-run for safety
        return True

DRY_RUN = ask_dry_run()

for raw in sys.stdin:
    line = raw.strip()
    if not line:
        continue

    # Skip commented lines
    if line.startswith("#"):
        if DRY_RUN:
            print("[SKIP] Comment line detected.")
        # In normal mode, silently skip (per requirements)
        continue

    # Expect 5 colon-delimited fields: username:password:last:first:groups
    parts = line.split(":")
    if len(parts) < 5:
        if DRY_RUN:
            print(f"[ERROR] Not enough fields -> {line!r}")
        # In normal mode, silently skip (per requirements)
        continue

    username, password, lastname, firstname, groups_field = parts[:5]

    if DRY_RUN:
        # Print what WOULD run
        print(f"\n[DRY-RUN] Creating user: {username}")
        print(f"$ sudo useradd -m -c '{firstname} {lastname}' {username}")
        print(f"$ echo '<hidden>' | sudo chpasswd")
        if groups_field != "-":
            for g in [x.strip() for x in groups_field.split(",") if x.strip()]:
                print(f"$ sudo groupadd -f {g}")
                print(f"$ sudo usermod -aG {g} {username}")
        continue

    # ---- Normal run (no extra error/skip messages) ----
    # Create user with home and comment = "First Last"
    os.system(f"sudo useradd -m -c '{firstname} {lastname}' {username}")
    # Set password
    os.system(f"echo '{username}:{password}' | sudo chpasswd")

    # Add to groups if provided (and ensure groups exist)
    if groups_field != "-":
        for g in [x.strip() for x in groups_field.split(",") if x.strip()]:
            os.system(f"sudo groupadd -f {g}")
            os.system(f"sudo usermod -aG {g} {username}")
