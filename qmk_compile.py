import json
import os
import shutil
import subprocess
import sys
import questionary
from enum import Enum
from types import SimpleNamespace

# Exec
msys_exe = r"C:\QMK_MSYS\usr\bin\bash.exe"

# Local
firmware_local = os.path.join("production", "firmware")
qmk_local = os.path.join("source", "qmk")

# Remote
firmware_remote = os.path.join(os.environ.get("USERPROFILE"), "qmk_firmware")
qmk_remote = os.path.join(firmware_remote, "keyboards", "krtkus")
hex_remote = os.path.join(firmware_remote, "krtkus_default.hex")
qmk_config = os.path.join(qmk_remote, "keyboard.json")

class Pinout(Enum):
    STANDARD = "standard"
    LEGACY = "legacy"

def get_arguments():
    args = SimpleNamespace()

    args.pinout = questionary.select(
        "Select pinout:",
        choices=[
            questionary.Choice(p.value, p) for p in Pinout
        ],
        default=Pinout.STANDARD
    ).ask()

    if args.pinout is None:
        sys.exit()

    # https://docs.qmk.fm/config_options#avr-mcu-options
    args.bootloader = questionary.select(
        "Select bootloader:",
        choices=[
            "atmel-dfu",
            "bootloadhid",
            "caterina",
            "halfkay",
            "lufa-dfu",
            "qmk-dfu",
            "qmk-hid",
            "usbasploader"
        ],
        default="caterina"
    ).ask()

    if args.bootloader is None:
        sys.exit()

    print()

    return args

def copy_qmk_folder():
    # Remove existing
    if os.path.exists(qmk_remote):
        shutil.rmtree(qmk_remote)
        print(f"Removed existing folder '{qmk_remote}'.")

    # Create qmk firmware keyboard folder
    shutil.copytree(qmk_local, qmk_remote)
    print(f"Copied '{qmk_local}' to '{qmk_remote}'.")

def modify_config(args):
    # Read
    with open(qmk_config, "r") as file:
        data = json.loads(file.read())

    # Bootloader
    data["bootloader"] = args.bootloader

    # Legacy ks-33 matrix pinout
    if args.pinout == Pinout.LEGACY:
        data["matrix_pins"] = {
            "cols": ["D2", "D3", "F4", "F5", "F6", "F7", "B1", "B4", "B5", "B3", "B2", "B6"],
            "rows": ["C6", "D7", "E6", "D4", "D0", "D1"]
        }

    # Write
    with open(qmk_config, "w") as file:
        json.dump(data, file)

    print(f"Modified '{qmk_config}'.")
    print()

def run_qmk_compile():
    # Environment
    # https://docs.qmk.fm/other_vscode#msys2-setup
    env = os.environ.copy()
    env["MSYSTEM"] = "MINGW64"

    # Run
    process = subprocess.Popen(
        [msys_exe, "-l", "-c", "qmk compile -kb krtkus -km default"],
        env=env,
        stdout=subprocess.PIPE,
        text=True
    )

    for line in process.stdout:
        print(line, end="")

    process.wait()
    print()

def obtain_hex_file(args):
    # Hex file name
    name_parts = ["krtkus"]
    name_parts.append(args.bootloader.replace("-", "_"))
    if args.pinout == Pinout.LEGACY:
        name_parts.append(Pinout.LEGACY.value)

    # Run
    hex_local = os.path.join(firmware_local, "_".join(name_parts) + ".hex")
    shutil.copy2(hex_remote, hex_local)
    print(f"Moved '{hex_remote}' to '{hex_local}'.")

def clean_up():
    shutil.rmtree(qmk_remote)
    print(f"Cleaned up '{qmk_remote}'.")

if __name__ == "__main__":
    # Args
    args = get_arguments()

    # Setup
    copy_qmk_folder()
    modify_config(args)

    # Process
    run_qmk_compile()
    obtain_hex_file(args)
    clean_up()
