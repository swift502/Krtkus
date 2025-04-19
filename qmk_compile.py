import json
import os
import shutil
import subprocess
import sys
from types import SimpleNamespace
import questionary

# Local
firmware_local = os.path.join("production", "firmware")
qmk_local = os.path.join("source", "qmk")
qmk_config = os.path.join(qmk_local, "keyboard.json")

# Remote
firmware_remote = os.path.join(os.environ.get("USERPROFILE"), "qmk_firmware")
qmk_remote = os.path.join(firmware_remote, "keyboards", "krtkus")
hex_remote = os.path.join(firmware_remote, "krtkus_default.hex")
msys_exe = r"C:\QMK_MSYS\usr\bin\bash.exe"

class KeyboardConfig:
    original_content: str
    data: dict

    def __init__(self):
        # Load default keyboard json
        with open(qmk_config, "r") as file:
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
        with open(qmk_config, "w") as file:
            json.dump(self.data, file, indent=4)

    def restore(self):
        with open(qmk_config, "w") as file:
            file.write(self.original_content)

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
    if os.path.exists(qmk_remote):
        shutil.rmtree(qmk_remote)
        print(f"Removed existing folder '{qmk_remote}'.")

    shutil.copytree(qmk_local, qmk_remote)
    print(f"Copied '{qmk_local}' to '{qmk_remote}'.")

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
    name_parts += [args.bootloader.replace("-", "_")]
    if args.pinout == "legacy": name_parts += ["legacy"]
    hex_local = os.path.join(firmware_local, "_".join(name_parts) + ".hex")

    # Run
    shutil.copy2(hex_remote, hex_local)
    print(f"Moved '{hex_remote}' to '{hex_local}'.")

def clean_up():
    shutil.rmtree(qmk_remote)
    print(f"Cleaned up '{qmk_remote}'.")

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
