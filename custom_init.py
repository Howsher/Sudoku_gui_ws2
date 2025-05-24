
# Custom initialization script
import os
import sys
import importlib.util

# Add the current directory to the path
dir_path = os.path.dirname(os.path.realpath(__file__))
if dir_path not in sys.path:
    sys.path.insert(0, dir_path)

# Try to import and run the copy_qt_plugins script
try:
    copy_plugins_spec = importlib.util.spec_from_file_location("copy_qt_plugins", 
                                               os.path.join(dir_path, "copy_qt_plugins.py"))
    copy_plugins_module = importlib.util.module_from_spec(copy_plugins_spec)
    copy_plugins_spec.loader.exec_module(copy_plugins_module)
    copy_plugins_module.copy_qt_plugins()
except Exception as e:
    print(f"Error setting up Qt plugins: {e}")
