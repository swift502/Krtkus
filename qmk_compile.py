import os
import shutil
import subprocess
import argparse
import json

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-bl", "--bootloader",
        choices=["atmel-dfu", "lufa-dfu", "qmk-dfu", "halfkay", "caterina", "bootloadhid", "usbasploader"],
        default="caterina"
    )
    args = parser.parse_args()

    return args

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
        # Set overrides
        for key, value in vars(args).items():
            self.data[key] = value

        # Write overrides
        with open(KeyboardConfig.config_path, "w") as file:
            json.dump(self.data, file, indent=4)

        for key, value in vars(args).items():
            print(f"\"{key}\" is set to \"{value}\"")
        print()

    def restore(self):
        with open(KeyboardConfig.config_path, "w") as file:
            file.write(self.original_content)
    
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

# https://docs.qmk.fm/other_vscode#msys2-setup
def run_qmk_compile():
    # Commands
    msys = r"C:\QMK_MSYS\usr\bin\bash.exe"
    args = ["--login", "-c", "qmk compile -kb krtkus -km default"]

    # Environment variables
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

def copy_hex_to_script_root(args):
    # Paths
    hex_source = os.path.join(os.environ.get("USERPROFILE"), "qmk_firmware", "krtkus_default.hex")
    hex_dist = os.path.join("production", "firmware", f"krtkus_{args.bootloader.replace("-", "_")}.hex")

    # Run
    try:
        shutil.copy2(hex_source, hex_dist)
        print(f"Copied '{hex_source}' to '{hex_dist}'.")
    except Exception as e:
        print(f"Error copying HEX file: {e}")

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
    copy_hex_to_script_root(args)
