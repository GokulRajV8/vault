import base64
import os
import sys

from . import Fernet
from . import InvalidToken
from . import Scrypt

from . import SLASH
from . import operations

# salt used in the application
salt = b"\x18\xec7$\xd9\x85\xc87$i\xa3\xfeZ-\xd49\xe2\xb1$\x11\xc3C\xe5\xf1\xc0\xf8\x136%\xd7\xcd!"

vault_dir = f"{os.getenv("USERPROFILE")}{SLASH}Vault"

# checking if vault is present
if not os.path.isdir(vault_dir):
    print(
        "Vault directory is not present at your home directory.\n"
        "Kindly create ~/Vault directory before starting me.\n"
    )
    sys.exit(0)

vault_verifier_file = f"{vault_dir}{SLASH}verifier"
vault_notes = list(
    filter(
        lambda file_name: file_name.endswith(".encnote")
        and os.path.isfile(f"{vault_dir}{SLASH}{file_name}"),
        os.listdir(vault_dir),
    )
)
vault_files = list(
    filter(
        lambda file_name: file_name.endswith(".encfile")
        and os.path.isfile(f"{vault_dir}{SLASH}{file_name}"),
        os.listdir(vault_dir),
    )
)

password_verified = False

if not os.path.isfile(vault_verifier_file):
    if len(vault_notes) + len(vault_files) > 0:
        print(
            "Vault cannot be verified and is not empty, hence all data are lost forever.\n"
            "Kindly delete all data present in ~/Vault and restart me.\n"
        )
        sys.exit(0)
    else:
        print("Vault is empty, initializing new vault ...")
        kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)

        password = input("Enter the password for vault : ")
        fernet = Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode())))

        with open(vault_verifier_file, "wb") as verifier_file:
            verifier_file.write(fernet.encrypt("success".encode()))
        print("Vault initialization completed.\n")

        # no need to take password again
        password_verified = True

if not password_verified:
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)

    password = input("Enter the password for vault : ")
    fernet = Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode())))

    with open(vault_verifier_file, "rb") as verifier_file:
        try:
            verifier_file_decrypted = fernet.decrypt(verifier_file.read()).decode()
            if verifier_file_decrypted == "success":
                print("Password verified successfully.\n")
            else:
                raise InvalidToken
        except InvalidToken:
            print(
                "Password verification failed.\n"
                "Either password is incorrect or vault is tampered.\n"
            )
            sys.exit(0)

# welcome prompt
print("Welcome to your personal Vault !!!\nEnter ! to go back at any point\n")

while True:
    option = input("Do you want to process notes or files (n, f) : ")
    if option == "!":
        print("Thank you for using Vault !!!")
        break
    elif option in ("n", "f"):
        menu_name = option
        while menu_name != "":
            if option == "n":
                menu_name = operations.execute(
                    menu_name, fernet=fernet, vault_dir=vault_dir, files=vault_notes
                )
            else:
                menu_name = operations.execute(
                    menu_name, fernet=fernet, vault_dir=vault_dir, files=vault_files
                )
    else:
        print("Invalid option")
