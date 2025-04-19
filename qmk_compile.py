import json
import os
import shutil
import subprocess
import sys
from types import SimpleNamespace

import questionary

class KeyboardConfig:

    config_path = r"source\qmk\keyboard.json"
    original_content: str
    data: dict

    def __init__(self):
        # Load default keyboard json
        with open(KeyboardConfig.config_path, "r") as file:
            self.original_content = file.read()
            self.data = json.loads(self.original_content)

    def override(self, args):
        # Bootloader
        self.data["bootloader"] = args.bootloader

        # Legacy ks-33 matrix pinout
        if args.pinout == "legacy":
            self.data["matrix_pins"] = {
                "cols": ["D2", "D3", "F4", "F5", "F6", "F7", "B1", "B4", "B5", "B3", "B2", "B6"],
                "rows": ["C6", "D7", "E6", "D4", "D0", "D1"]
            }

        # Write overrides into the json file so
        # it can be copied into the qmk folder
        with open(KeyboardConfig.config_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def restore(self):
        with open(KeyboardConfig.config_path, "w") as file:
            file.write(self.original_content)

def print_error(message):
    print(f"\033[91m{message}\033[0m")

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

def copy_folder_to_qmk():
    # Paths
    qmk_source = os.path.join("source", "qmk")
    qmk_dest = os.path.join(os.environ.get("USERPROFILE"), "qmk_firmware", "keyboards", "krtkus")

    # Run
    try:
        if os.path.exists(qmk_dest):
            shutil.rmtree(qmk_dest)
            print(f"Removed existing folder '{qmk_dest}'.")
            
        shutil.copytree(qmk_source, qmk_dest)
        print(f"Copied '{qmk_source}' to '{qmk_dest}'.")
        print()
    except Exception as e:
        print_error(f"Error copying folder: {e}")
        sys.exit(1)

def run_qmk_compile():
    # Command
    msys_exe = r"C:\QMK_MSYS\usr\bin\bash.exe"
    args = [msys_exe, "-l", "-c", "qmk compile -kb krtkus -km default"]

    # Environment variables
    # https://docs.qmk.fm/other_vscode#msys2-setup
    env = os.environ.copy()
    env["MSYSTEM"] = "MINGW64"

    # Run
    try:
        process = subprocess.Popen(args, env=env, stdout=subprocess.PIPE, text=True)

        # Print output
        for line in process.stdout:
            print(line, end="")

        process.wait()
        print()

    except Exception as e:
        print_error(f"Error running QMK compile: {e}")
        sys.exit(1)

def obtain_hex_file(args):
    # Name
    name_parts = ["krtkus"]
    name_parts += [args.bootloader.replace("-", "_")]
    if args.pinout == "legacy": name_parts += ["legacy"]

    # Paths
    hex_source = os.path.join(os.environ.get("USERPROFILE"), "qmk_firmware", "krtkus_default.hex")
    hex_dest = os.path.join("production", "firmware", "_".join(name_parts) + ".hex")

    # Run
    try:
        shutil.copy2(hex_source, hex_dest)
        print(f"Moved '{hex_source}' to '{hex_dest}'.")
    except Exception as e:
        print_error(f"Error obtaining hex file: {e}")
        sys.exit(1)

def clean_up():
    # Paths
    qmk_dest = os.path.join(os.environ.get("USERPROFILE"), "qmk_firmware", "keyboards", "krtkus")

    # Run
    try:
        shutil.rmtree(qmk_dest)
        print(f"Cleaned up '{qmk_dest}'.")
    except Exception as e:
        print_error(f"Error cleaning up: {e}")
        sys.exit(1)

if __name__ == "__main__":
    args = get_arguments()
    
    # Modify config
    config = KeyboardConfig()
    config.override(args)
    copy_folder_to_qmk()
    config.restore()

    # Process
    run_qmk_compile()
    obtain_hex_file(args)
    clean_up()
