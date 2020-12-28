import winreg
import itertools
from textwrap import shorten


root = "SOFTWARE"
target_root = winreg.HKEY_LOCAL_MACHINE
h_key_main = winreg.OpenKey(target_root, root)
AUTO_FIX = False


def get_keyword():
    target = input("Keyword >> ")
    if input("Confirm? (y/n) >> ") == "y":
        return target

    return get_keyword()


def iterkeys(key, root_path=root):
    """
    Recursively iterates thru keys, revealing all keys.
    returns absolute path relative to root, and EnumValue result.
    """

    for i in itertools.count():
        try:
            out = winreg.EnumValue(key, i)
        except OSError as err:
            try:
                out = winreg.EnumKey(key, i)
            except OSError as err:  # end of key
                return

            # else it's likely to be a folder. recursively opens it.
            try:
                yield from iterkeys(winreg.OpenKey(key, out), f"{root_path}\\{out}")
            except OSError as err_:
                return

        else:
            yield root_path, out


def fetch_list(search_target):
    counter = 1
    convert_list = []

    for idx, (path_, (name, val, type_)) in enumerate(iterkeys(h_key_main)):
        if search_target in name or search_target in str(val):
            try:
                val_short = val[:50]
            except TypeError:
                val_short = val

            print(f"Match: {counter:<7} Total: {idx:<10} | {path_[:50]} | {name[:50]} | {val_short}")
            counter += 1
            convert_list.append((path_, name, val))

    return convert_list


def fetch_reg_type_table():
    """
    >>> import winreg

    >>> def a():
    ...     for n_ in [name_ for name_ in dir(winreg) if name_.startswith("REG")]:
    ...         yield n_, getattr(winreg, n_)
    ...

    >>> l = list(a())

    >>> for n_, v in sorted(l, key=lambda x: x[1]):
    ...     print(f"{v}: "{n_}",")
    ...
    """
    table = {0: "REG_NONE",
             1: "REG_SZ",
             3: "REG_BINARY",
             4: "REG_DWORD",
             # 4: "REG_DWORD_LITTLE_ENDIAN",
             5: "REG_DWORD_BIG_ENDIAN",
             6: "REG_LINK",
             7: "REG_MULTI_SZ",
             8: "REG_RESOURCE_LIST",
             9: "REG_FULL_RESOURCE_DESCRIPTOR",
             10: "REG_RESOURCE_REQUIREMENTS_LIST",
             11: "REG_QWORD",
             # 11: "REG_QWORD_LITTLE_ENDIAN",
             }

    return table


def convert_interactively(old_str, new_str, conversion_list, registry_table):
    for idx, (path_, name, val) in enumerate(conversion_list, 1):
        try:
            context = winreg.OpenKey(target_root, path_, 0, winreg.KEY_ALL_ACCESS)
        except PermissionError:
            print(f"Permission error on {path_}, {name}!")
            continue

        with context as h_key:

            value, type_ = winreg.QueryValueEx(h_key, name)

            print(f"\n{idx} / {len(conversion_list)}\n"
                  f"Path: {path_}\n"
                  f"Type: {registry_table[type_]}\n"
                  f"From: {val}")

            try:
                converted = value.replace(old_str, new_str)
            except (AttributeError, TypeError) as err:
                print(err)
                print(f"Passing {name}, {val}")
                continue

            print(f"To  : {converted}\n")

            if not AUTO_FIX:
                input(f"Press enter to convert this key, or press Ctrl+C to stop.")

            winreg.SetValueEx(h_key, name, 0, type_, value.replace(old_str, new_str))


def main():
    # \\keyword\\ is expected for directory search
    print("\nIf you are trying to convert directory, then it's recommended to add reverse slash around them.\n")
    keyword = get_keyword()

    fetched = fetch_list(keyword)
    print(f"Fetched {len(fetched)} entries.")

    print(f"\nSpecify keyword to replace {keyword}.\n")
    keyword_conv = get_keyword()

    fetch_reg_types = fetch_reg_type_table()

    convert_interactively(keyword, keyword_conv, fetched, fetch_reg_types)


if __name__ == '__main__':
    main()
