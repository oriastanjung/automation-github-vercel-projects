import os
import stat

def on_rm_error(func, path, exc_info):
    """
    Handle permission errors during rmtree.
    Tries to chmod the file to be writable and retry.
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)