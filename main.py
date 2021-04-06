import sys
from crypto import Crypto
from colorama import Fore

if len(sys.argv) >= 3:
    option = sys.argv[1]
    file = sys.argv[2]

else:
    print(
        f"{Fore.GREEN}usage{Fore.WHITE}:\n"
        f"{Fore.GREEN}python main.py "
        f"{Fore.WHITE}[{Fore.CYAN}encrypt{Fore.WHITE}|{Fore.CYAN}decrypt{Fore.WHITE}]{Fore.GREEN} "
        f"{Fore.WHITE}<{Fore.CYAN}file{Fore.WHITE}>{Fore.RESET}"
    )
