import os
import time
import uuid
import platform
import psutil
from colorama import Fore

magenta = Fore.LIGHTMAGENTA_EX
red = Fore.LIGHTRED_EX
green = Fore.LIGHTGREEN_EX

banner = '''
███████╗██╗   ██╗██╗   ██╗██╗   ██╗    ██████╗  █████╗ ████████╗ ██████╗██╗  ██╗
██╔════╝██║   ██║╚██╗ ██╔╝██║   ██║    ██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║  ██║
███████╗██║   ██║ ╚████╔╝ ██║   ██║    ██████╔╝███████║   ██║   ██║     ███████║
╚════██║██║   ██║  ╚██╔╝  ██║   ██║    ██╔═══╝ ██╔══██║   ██║   ██║     ██╔══██║
███████║╚██████╔╝   ██║   ╚██████╔╝    ██║     ██║  ██║   ██║   ╚██████╗██║  ██║
╚══════╝ ╚═════╝    ╚═╝    ╚═════╝     ╚═╝     ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝
              * SUYU Multiplayer Patcher | By WeepingAngel * 
    GitHub: https://github.com/Crafttino21 | Leave a Star if you like it!                                                                        
'''


def generate_random_token():
    """Generates a random UUID token."""
    return str(uuid.uuid4())


def check_problematic_process(process_name="suyu.exe" or "suyu"):
    """Checks if a problematic process is running, stops it, and outputs a message."""
    process_detected = False
    for proc in psutil.process_iter(attrs=["pid", "name"]):
        try:
            if proc.info["name"] == process_name:
                proc.kill()
                print(f"{red}[!] Suyu Detected! Stop Process. {proc.info['pid']}")
                process_detected = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if not process_detected:
        print(f"{green}[+] No Suyu detected! Start Patching...")


def update_config_file(username, config_path):
    """Updates the config file by replacing the [WebService] section with new values."""
    if not os.path.exists(config_path):
        print(f"{red}[-] Config file not found at {config_path}.")
        return

    new_token = generate_random_token()

    # New [WebService] section content
    web_service_content = f"""[WebService]
enable_telemetry\\default=false
enable_telemetry=false
web_api_url\\default=false
web_api_url=api.ynet-fun.xyz
suyu_username\\default=false
suyu_username={username}
suyu_token\\default=false
suyu_token={new_token}


"""

    # Read the file and replace [WebService] section
    with open(config_path, 'r') as file:
        lines = file.readlines()

    # Flag to check if inside [WebService] section
    in_web_service_section = False
    updated_lines = []

    for line in lines:
        if line.strip() == "[WebService]":
            in_web_service_section = True
            updated_lines.append(web_service_content)
            continue

        if in_web_service_section:
            if line.startswith("[") and line.strip() != "[WebService]":
                in_web_service_section = False
                updated_lines.append(line)
        else:
            updated_lines.append(line)

    with open(config_path, 'w') as file:
        file.writelines(updated_lines)

    print(f"{green}[+] Multiplayer Fixed! New username: {username}, new token: {new_token}")


# Main logic
if __name__ == "__main__":
    print(magenta + banner)
    print(magenta + "[+] Preparing Fix...")
    check_problematic_process()

    # Windows and Linux path setup for config file
    if platform.system() == "Windows":
        config_path = os.path.join("C:", os.sep, "Users", os.getenv("USERNAME"), "AppData", "Roaming", "suyu", "config",
                                   "qt-config.ini")
    else:
        config_path = os.path.expanduser("~/.suyu/config/qt-config.ini")

    username = input(magenta + "[+] Enter your Username: ")
    time.sleep(4)
    update_config_file(username, config_path)
    time.sleep(3)

    print(green + "[+] Fix and Patching Successfully! Thanks for Using!")
    time.sleep(5)
