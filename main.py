import sys
from crypto import Crypto

if len(sys.argv) >= 3:
    option = sys.argv[1]
    file = sys.argv[2]
    crypto = Crypto(file)

    if option == "encrypt":
        crypto.encrypt()

    elif option == "decrypt":
        crypto.decrypt()

else:
    print(
        f"usage:\n"
        f"python main.py [encrypt|decrypt] <file>"
    )
