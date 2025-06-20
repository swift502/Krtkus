import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

# Exec
msys_exe = r"C:\QMK_MSYS\usr\bin\bash.exe"

# Local
local_dir = Path(__file__).parent.resolve()
firmware_local = local_dir / "production" / "firmware"
qmk_local = local_dir / "source" / "qmk"

# Remote
firmware_remote = Path.home() / "qmk_firmware"
hex_remote = firmware_remote / "krtkus_default.hex"
qmk_remote = firmware_remote / "keyboards" / "krtkus"
config_remote = qmk_remote / "keyboard.json"

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-bl", "--bootloader")
    parser.add_argument("-l", "--legacy", action = "store_true", default = False)

    return parser.parse_args()

def copy_qmk_folder():
    # Remove existing
    if qmk_remote.exists():
        shutil.rmtree(qmk_remote)
        print(f"Removed existing folder '{qmk_remote}'.")

    # Create qmk firmware keyboard folder
    shutil.copytree(qmk_local, qmk_remote)
    print(f"Copied '{qmk_local}' to '{qmk_remote}'.")

def override_config(args: argparse.Namespace):
    # Read
    with open(config_remote, "r") as file:
        data: dict = json.load(file)

    # Bootloader
    # https://docs.qmk.fm/config_options#avr-mcu-options
    if args.bootloader:
        data["bootloader"] = args.bootloader

    # Legacy ks-33 matrix pinout
    if args.legacy:
        data["matrix_pins"] = {
            "cols": ["D2", "D3", "F4", "F5", "F6", "F7", "B1", "B4", "B5", "B3", "B2", "B6"],
            "rows": ["C6", "D7", "E6", "D4", "D0", "D1"]
        }

    # Write
    with open(config_remote, "w") as file:
        json.dump(data, file)

    print(f"Modified '{config_remote}'.")

    return data

def run_qmk_compile():
    # Environment
    # https://docs.qmk.fm/other_vscode#msys2-setup
    env = os.environ.copy()
    env["MSYSTEM"] = "MINGW64"

    # Args
    command = "qmk compile -kb krtkus -km default"
    args = [msys_exe, "--login", "-c", command]

    # Run
    print()
    subprocess.run(args, env=env, check=True)
    print()

def obtain_hex_file(args: argparse.Namespace, config: dict):
    # Hex file name
    bootloader = config["bootloader"].replace("-", "_")
    name_parts = ["krtkus", bootloader]
    if args.legacy:
        name_parts.append("legacy")
    hex_name = "_".join(name_parts) + ".hex"

    # Run
    hex_local = firmware_local / hex_name
    shutil.move(hex_remote, hex_local)
    print(f"Moved '{hex_remote}' to '{hex_local}'.")

def clean_up():
    shutil.rmtree(qmk_remote)
    print(f"Cleaned up '{qmk_remote}'.")

def main():
    # Setup
    args = get_arguments()
    copy_qmk_folder()
    config = override_config(args)

    # Process
    run_qmk_compile()
    obtain_hex_file(args, config)
    clean_up()

if __name__ == "__main__":
    main()