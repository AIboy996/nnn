import os
import lzma
import pickle
from hashlib import md5


def save_model(obj, save_path, file_name: str = "model"):
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    dumpped_bytes = pickle.dumps(obj)
    checksum = md5(dumpped_bytes).hexdigest()
    with lzma.open(os.path.join(save_path, file_name + ".xz"), "wb") as f:
        pickle.dump(obj, f)
    with open(os.path.join(save_path, file_name + ".md5"), "w+") as f:
        f.write(checksum)
    return os.path.join(save_path, file_name + ".xz")


def load_model(file_path):
    with lzma.open(file_path, "rb") as f:
        s = f.read()
    try:
        with open(file_path.replace(".xz", ".md5"), "r") as f:
            checksum = f.read()
    except FileNotFoundError:
        print("Checksum not found.")
    except Exception as e:
        print(repr(e))
    assert md5(s).hexdigest() == checksum, "Checksum wrong."
    return pickle.loads(s)
