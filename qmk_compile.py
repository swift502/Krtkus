import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

# Exec
msys_exe = r"C:\QMK_MSYS\usr\bin\bash.exe"

# Local
root_local = Path(__file__).parent.resolve()
firmware_local = root_local / "production" / "firmware"
kb_local = root_local / "source" / "qmk"

# Remote
root_remote = Path.home() / "qmk_firmware"
hex_remote = root_remote / "krtkus_default.hex"
kb_remote = root_remote / "keyboards" / "krtkus"
kb_config = kb_remote / "keyboard.json"

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-bl", "--bootloader")
    parser.add_argument("-l", "--legacy", action = "store_true", default = False)

    return parser.parse_args()

def copy_qmk_folder():
    # Remove existing
    if kb_remote.exists():
        shutil.rmtree(kb_remote)
        print(f"Removed existing folder '{kb_remote}'.")

    # Setup qmk keyboard folder
    shutil.copytree(kb_local, kb_remote)
    print(f"Copied '{kb_local}' to '{kb_remote}'.")

def override_config(args: argparse.Namespace):
    # Read
    with open(kb_config, "r") as file:
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
    with open(kb_config, "w") as file:
        json.dump(data, file)

    print(f"Modified '{kb_config}'.")

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
    shutil.rmtree(kb_remote)
    print(f"Cleaned up '{kb_remote}'.")

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