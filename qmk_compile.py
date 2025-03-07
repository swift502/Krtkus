import os
import shutil
import subprocess
import argparse

def get_output_argument():
    parser = argparse.ArgumentParser(description="Process some arguments.")
    parser.add_argument("output", type=str, help="Output hex file name")
    args = parser.parse_args()

    if not args.output:
        print("Error: No hex file name provided.")
        exit()

    return args.output

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

def copy_hex_to_script_root(output_file):
    # Paths
    hex_source = os.path.join(os.environ.get("USERPROFILE"), "qmk_firmware", "krtkus_default.hex")
    hex_dist = os.path.join("production", "firmware", output_file)

    # Run
    try:
        shutil.copy2(hex_source, hex_dist)
        print(f"Copied '{hex_source}' to '{hex_dist}'.")
    except Exception as e:
        print(f"Error copying HEX file: {e}")

if __name__ == "__main__":
    # Args
    output_file = get_output_argument()
    
    # Run
    copy_folder_to_qmk()
    run_qmk_compile()
    copy_hex_to_script_root(output_file)
