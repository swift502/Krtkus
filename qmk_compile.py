import json
import os
import shutil
import subprocess
import argparse

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

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-bl", "--bootloader")
    parser.add_argument("-l", "--legacy", action = "store_true", default = False)

    return parser.parse_args()

def copy_qmk_folder():
    # Remove existing
    if os.path.exists(qmk_remote):
        shutil.rmtree(qmk_remote)
        print(f"Removed existing folder '{qmk_remote}'.")

    # Create qmk firmware keyboard folder
    shutil.copytree(qmk_local, qmk_remote)
    print(f"Copied '{qmk_local}' to '{qmk_remote}'.")

def override_config(args):
    # Read
    with open(qmk_config, "r") as file:
        data = json.loads(file.read())

    # Bootloader
    # https://docs.qmk.fm/config_options#avr-mcu-options
    if args.bootloader is not None:
        data["bootloader"] = args.bootloader

    # Legacy ks-33 matrix pinout
    if args.legacy:
        data["matrix_pins"] = {
            "cols": ["D2", "D3", "F4", "F5", "F6", "F7", "B1", "B4", "B5", "B3", "B2", "B6"],
            "rows": ["C6", "D7", "E6", "D4", "D0", "D1"]
        }

    # Write
    with open(qmk_config, "w") as file:
        json.dump(data, file)

    print(f"Modified '{qmk_config}'.")

    return data

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

    print()
    for line in process.stdout:
        print(line, end="")

    process.wait()
    print()

def obtain_hex_file(args, config):
    # Hex file name
    name_parts = ["krtkus"]
    name_parts.append(config["bootloader"].replace("-", "_"))
    if args.legacy: name_parts.append("legacy")

    # Run
    hex_local = os.path.join(firmware_local, "_".join(name_parts) + ".hex")
    shutil.copy2(hex_remote, hex_local)
    print(f"Moved '{hex_remote}' to '{hex_local}'.")

def clean_up():
    shutil.rmtree(qmk_remote)
    print(f"Cleaned up '{qmk_remote}'.")

if __name__ == "__main__":
    # Setup
    args = get_arguments()
    copy_qmk_folder()
    config = override_config(args)

    # Process
    run_qmk_compile()
    obtain_hex_file(args, config)
    clean_up()
