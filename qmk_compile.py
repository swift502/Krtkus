import json
import os
import shutil
import subprocess
import sys
import questionary
from types import SimpleNamespace

# Local
firmware_local = os.path.join("production", "firmware")
qmk_local = os.path.join("source", "qmk")

# Remote
firmware_remote = os.path.join(os.environ.get("USERPROFILE"), "qmk_firmware")
qmk_remote = os.path.join(firmware_remote, "keyboards", "krtkus")
hex_remote = os.path.join(firmware_remote, "krtkus_default.hex")
qmk_config = os.path.join(qmk_remote, "keyboard.json")
msys_exe = r"C:\QMK_MSYS\usr\bin\bash.exe"

def get_arguments():
    args = SimpleNamespace()

    args.pinout = questionary.select(
        "Select pinout:",
        choices=[
            "standard",
            "legacy"
        ],
        default="standard"
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

    print()

def override_config(args):
    # Read
    with open(qmk_config, "r") as file:
        data = json.loads(file.read())

    # Bootloader
    data["bootloader"] = args.bootloader

    # Legacy ks-33 matrix pinout
    if args.pinout == "legacy":
        data["matrix_pins"] = {
            "cols": ["D2", "D3", "F4", "F5", "F6", "F7", "B1", "B4", "B5", "B3", "B2", "B6"],
            "rows": ["C6", "D7", "E6", "D4", "D0", "D1"]
        }

    # Write
    with open(qmk_config, "w") as file:
        json.dump(data, file)

def run_qmk_compile():
    # Environment
    # https://docs.qmk.fm/other_vscode#msys2-setup
    env = os.environ.copy()
    env["MSYSTEM"] = "MINGW64"

    # Run
    process = subprocess.Popen(
        [msys_exe, "-l", "-c", "qmk compile -kb krtkus -km default"],
        stdout=subprocess.PIPE,
        env=env,
        text=True
    )

    for line in process.stdout:
        print(line, end="")

    process.wait()
    print()

def obtain_hex_file(args):
    # Hex file name
    name_parts = ["krtkus"]
    name_parts += [args.bootloader.replace("-", "_")]
    if args.pinout == "legacy": name_parts += ["legacy"]

    # Run
    hex_local = os.path.join(firmware_local, "_".join(name_parts) + ".hex")
    shutil.copy2(hex_remote, hex_local)
    print(f"Moved '{hex_remote}' to '{hex_local}'.")

def clean_up():
    shutil.rmtree(qmk_remote)
    print(f"Cleaned up '{qmk_remote}'.")

if __name__ == "__main__":
    args = get_arguments()

    # Setup
    copy_qmk_folder()
    override_config(args)

    # Process
    run_qmk_compile()
    obtain_hex_file(args)
    clean_up()
