import os
import shutil
import subprocess
import argparse
import json

class KeyboardConfig:

    config_path = r"source\qmk\keyboard.json"
    original_content: str
    data: dict

    def __init__(self):
        # Read the JSON file
        with open(KeyboardConfig.config_path, "r") as file:
            self.original_content = file.read()
            self.data = json.loads(self.original_content)

    def override(self, args):
        # Set direct overrides
        for key, value in vars(args).items():
            if key in self.data:
                self.data[key] = value
                print(f"\"{key}\" is set to \"{value}\"")
        print()

        # Legacy Ks-33 matrix pin layout
        if args.legacy:
            self.data["matrix_pins"] = {
                "cols": ["D2", "D3", "F4", "F5", "F6", "F7", "B1", "B4", "B5", "B3", "B2", "B6"],
                "rows": ["C6", "D7", "E6", "D4", "D0", "D1"]
            }

        # Write overrides
        with open(KeyboardConfig.config_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def restore(self):
        with open(KeyboardConfig.config_path, "w") as file:
            file.write(self.original_content)

def get_arguments():
    parser = argparse.ArgumentParser()
    # https://docs.qmk.fm/config_options#avr-mcu-options
    parser.add_argument("-bl", "--bootloader", default = "caterina",
        choices = [
            "atmel-dfu",
            "lufa-dfu",
            "qmk-dfu",
            "halfkay",
            "caterina",
            "bootloadhid",
            "usbasploader"
        ]
    )
    parser.add_argument("-l", "--legacy", action = "store_true", default = False, help = "use legacy matrix pin layout")
    args = parser.parse_args()

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
        print(f"Error copying folder: {e}")

def run_qmk_compile():
    # Command
    msys = r"C:\QMK_MSYS\usr\bin\bash.exe"
    args = ["--login", "-c", "qmk compile -kb krtkus -km default"]

    # Environment variables
    # https://docs.qmk.fm/other_vscode#msys2-setup
    env = os.environ.copy()
    env["MSYSTEM"] = "MINGW64"
    env["CHERE_INVOKING"] = "1"

    # Run
    try:
        process = subprocess.Popen([msys] + args, env=env, stdout=subprocess.PIPE, text=True)

        # Print output
        for line in process.stdout:
            print(line, end="")

        process.wait()
        print()

    except Exception as e:
        print(f"Error running QMK compile: {e}")

def obtain_hex_file(args):
    # Name
    bootloader = args.bootloader.replace("-", "_")
    legacy = "_legacy" if args.legacy else ""
    hex_name = f"krtkus_{bootloader}{legacy}.hex"

    # Paths
    hex_source = os.path.join(os.environ.get("USERPROFILE"), "qmk_firmware", "krtkus_default.hex")
    hex_dist = os.path.join("production", "firmware", hex_name)
    qmk_dest = os.path.join(os.environ.get("USERPROFILE"), "qmk_firmware", "keyboards", "krtkus")

    # Run
    try:
        shutil.copy2(hex_source, hex_dist)
        print(f"Moved '{hex_source}' to '{hex_dist}'.")
        
        shutil.rmtree(qmk_dest)
        print(f"Cleaned up '{qmk_dest}'.")
    except Exception as e:
        print(f"Error getting hex file: {e}")

if __name__ == "__main__":
    # Args
    args = get_arguments()
    
    # Copy folder to QMK
    config = KeyboardConfig()
    config.override(args)
    copy_folder_to_qmk()
    config.restore()

    # Compile
    run_qmk_compile()

    # Get HEX file
    obtain_hex_file(args)
