import winreg
import itertools

root = "SOFTWARE"
hKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, root)
access = winreg.KEY_ALL_ACCESS
target = "백준영"


def iterkeys(key):
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
                yield from iterkeys(winreg.OpenKey(key, out))
            except OSError as err_:
                return

        else:
            yield out


counter = 1
for idx, (name, val, type_) in enumerate(iterkeys(hKey)):
    try:
        if target in name or target in str(val):
            print(counter, idx, name, val)
            counter += 1
    except TypeError:
        pass

