"""
The operations are two levels deep and denoted by two characters.

First character denotes whether it is a note or file (n, f)
Second character denotes whether read, write or delete (r, w, d)
"""

from . import Fernet

from . import SLASH


def execute(menu_name: str, **params) -> str:
    internal_local_scope = {}
    exec(
        f"menu = menu_{menu_name}",
        globals(),
        internal_local_scope,
    )
    menu = internal_local_scope["menu"]
    return menu(**params)


def menu_n(fernet: Fernet, vault_dir: str, files: list[str]) -> str:
    print("Notes present in the vault :\n")
    for file in files:
        decrypted_note_name = fernet.decrypt(f"{vault_dir}{SLASH}{file}"[:-8]).decode()
        print(f"\t{decrypted_note_name}")

    option = input("Do you want to read/write or delete (r, w, d) : ")
    if option == "!":
        return ""

    match option:
        case "r":
            return "nr"
        case "w":
            return "nw"
        case "d":
            return "nd"
        case _:
            print("Invalid option")
            return "n"


def menu_f(fernet: Fernet, vault_dir: str, files: list[str]) -> str:
    print("Files present in the vault :\n")
    for file in files:
        decrypted_file_name = fernet.decrypt(f"{vault_dir}{SLASH}{file}"[:-8]).decode()
        print(f"\t{decrypted_file_name}")

    option = input("Do you want to read/write or delete (r, w, d) : ")
    if option == "!":
        return ""

    match option:
        case "r":
            return "fr"
        case "w":
            return "fw"
        case "d":
            return "fd"
        case _:
            print("Invalid option")
            return "f"


def menu_nr(fernet: Fernet, vault_dir: str, files: list[str]) -> str:
    return "n"


def menu_nw(fernet: Fernet, vault_dir: str, files: list[str]) -> str:
    return "n"


def menu_nd(fernet: Fernet, vault_dir: str, files: list[str]) -> str:
    return "n"


def menu_fr(fernet: Fernet, vault_dir: str, files: list[str]) -> str:
    return "f"


def menu_fw(fernet: Fernet, vault_dir: str, files: list[str]) -> str:
    return "f"


def menu_fd(fernet: Fernet, vault_dir: str, files: list[str]) -> str:
    return "f"
