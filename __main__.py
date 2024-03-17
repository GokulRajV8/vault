import base64
import os
import sys

from . import Fernet
from . import InvalidToken
from . import Scrypt

from . import Constants
from . import Messages

from . import database
from . import operations

VAULT_DIR = f"{os.getenv("USERPROFILE")}{Constants.SLASH}Vault"

# checking if vault is present
if not os.path.isdir(VAULT_DIR):
    print(Messages.VAULT_NOT_PRESENT)
    sys.exit(0)

vault_notes = list(
    filter(
        lambda file_name: file_name.endswith(Constants.FILE_FORMAT_NOTE)
        and os.path.isfile(f"{VAULT_DIR}{Constants.SLASH}{file_name}"),
        os.listdir(VAULT_DIR),
    )
)
vault_files = list(
    filter(
        lambda file_name: file_name.endswith(Constants.FILE_FORMAT_FILE)
        and os.path.isfile(f"{VAULT_DIR}{Constants.SLASH}{file_name}"),
        os.listdir(VAULT_DIR),
    )
)

password_verified = False

if not os.path.isfile(database.DB_FILE):
    if len(vault_notes) + len(vault_files) > 0:
        print(Messages.VAULT_NOT_EMPTY)
        sys.exit(0)

    print(Messages.INITIALIZING_VAULT)
    kdf = Scrypt(salt=Constants.SALT, length=32, n=2**16, r=8, p=1)
    password = input(Messages.ENTER_PASSWORD)
    fernet = Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode())))

    database.create_db(fernet.encrypt("success".encode()).decode())
    print(Messages.VAULT_INITIALIZED)

    # no need to take password again
    password_verified = True

if not password_verified:
    if not database.verify_db():
        print(Messages.VAULT_NOT_EMPTY)
        sys.exit(0)

    kdf = Scrypt(salt=Constants.SALT, length=32, n=2**16, r=8, p=1)
    password = input(Messages.ENTER_PASSWORD)
    fernet = Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode())))

    try:
        verifier_string_decrypted = fernet.decrypt(
            database.get_verifier_string().encode()
        ).decode()
        if verifier_string_decrypted == "success":
            # clearing screen to prevent password peeping
            os.system(Constants.CLEAR_COMMAND)
        else:
            raise InvalidToken

    except InvalidToken:
        print(Messages.PASSWORD_VERIFICATION_FAILURE)
        sys.exit(0)

# welcome prompt
print(Messages.WELCOME)

while True:
    option = input(Messages.NOTES_OR_FILES)
    if option == "!":
        print(Messages.EXIT_VAULT)
        break
    elif option in ("n", "f"):
        menu_name = option
        while menu_name != "":
            if option == "n":
                menu_name = operations.execute(
                    menu_name, fernet=fernet, vault_dir=VAULT_DIR, files=vault_notes
                )
            else:
                menu_name = operations.execute(
                    menu_name, fernet=fernet, vault_dir=VAULT_DIR, files=vault_files
                )
    else:
        print(Messages.INVALID_OPTION)
