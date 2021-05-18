import sys
from crypto import Crypto

if len(sys.argv) >= 3:
    option = sys.argv[1]
    file = sys.argv[2]
    crypto = Crypto(file=file)

    if option == "encrypt":
        crypto.encrypt()

    elif option == "decrypt":
        try:
            key = sys.argv[3]
        except IndexError:
            print(
                "Please provide key file.\n\n"
                "usage:\n"
                "python main.py [encrypt|decrypt] <file> <key file>\n"
                "key file: Optional. if you want to decrypt a file, you must provide it.\n"
            )
            sys.exit()
        crypto.decrypt(key_file=key)

else:
    print(
        "You can also use:\n"
        "python main.py [encrypt|decrypt] <file> <key file>\n"
        "key file: Optional. if you want to decrypt a file, you must provide it.\n"
    )

    option = input("Choose an option [encrypt|decrypt]: ")
    file = input("Enter file path: ")
    crypto = Crypto(file)

    if option == "encrypt":
        crypto.encrypt()

    elif option == "decrypt":
        key = input("Enter key file path: ")
        crypto.decrypt(key_file=key)
