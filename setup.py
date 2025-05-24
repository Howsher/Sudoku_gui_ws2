from cx_Freeze import setup, Executable
import sys
import os
import PySide6
import numpy
import shutil

# Get paths
pyside6_dir = os.path.dirname(PySide6.__file__)
print(f"PySide6 directory: {pyside6_dir}")
conda_env_path = os.environ.get('CONDA_PREFIX')

# Create qt.conf file for Qt plugin paths
with open('qt.conf', 'w') as f:
    f.write("""[Paths]
Prefix = .
Plugins = .
Binaries = .
Libraries = .
""")

# Collect core app files
include_files = [
    ("puzzles.py", "puzzles.py"),
    ("rules.py", "rules.py"),
    ("solver_by_rules.py", "solver_by_rules.py"),
    ("qt.conf", "qt.conf")
]

# Find qwindows.dll in standard locations
qwindows_paths = [
    os.path.join(conda_env_path, "Library", "lib", "qt6", "plugins", "platforms", "qwindows.dll"),
    os.path.join(conda_env_path, "Library", "plugins", "platforms", "qwindows.dll"),
    os.path.join(pyside6_dir, "plugins", "platforms", "qwindows.dll"),
    os.path.join(pyside6_dir, "Qt6", "plugins", "platforms", "qwindows.dll")
]

for qwindows_path in qwindows_paths:
    if os.path.exists(qwindows_path):
        print(f"Found qwindows.dll at: {qwindows_path}")
        include_files.append((qwindows_path, os.path.join("platforms", "qwindows.dll")))
        break
else:
    print("WARNING: Could not find qwindows.dll, application may not run properly")

# Add Qt DLLs
qt_dlls = ["Qt6Core.dll", "Qt6Gui.dll", "Qt6Widgets.dll", "Qt6Network.dll"]
qt_dll_dirs = [
    os.path.join(conda_env_path, "Library", "bin"),
    os.path.join(os.path.dirname(pyside6_dir), "Qt", "bin")
]

for dll in qt_dlls:
    for dll_dir in qt_dll_dirs:
        dll_path = os.path.join(dll_dir, dll)
        if os.path.exists(dll_path):
            print(f"Found {dll} at: {dll_path}")
            include_files.append((dll_path, dll))
            break


# Also check for imageformats plugins that might be needed
imageformats_paths = [
    os.path.join(conda_env_path, "Library", "lib", "qt6", "plugins", "imageformats"),
    os.path.join(conda_env_path, "Library", "plugins", "imageformats"),
    os.path.join(pyside6_dir, "plugins", "imageformats")
]

# Try to include some common image format plugins if available
for imageformats_path in imageformats_paths:
    if os.path.exists(imageformats_path):
        print(f"Found imageformats directory: {imageformats_path}")
        for img_plugin in ["qjpeg.dll", "qgif.dll", "qico.dll"]:
            img_path = os.path.join(imageformats_path, img_plugin)
            if os.path.exists(img_path):
                include_files.append((img_path, os.path.join("imageformats", img_plugin)))
                print(f"Adding {img_plugin} from {imageformats_path}")
        break

# Create a helper file to ensure numpy modules are included
with open('numpy_fix.py', 'w') as f:
    f.write("""
# Helper file to ensure numpy modules are included
import numpy
import numpy.core._methods
import numpy.lib.format
import numpy.core._dtype_ctypes
import numpy.core._asarray
import numpy.random
import numpy.linalg
""")

# Include the helper file
include_files.append("numpy_fix.py")

build_exe_options = {
    "packages": [
        "PySide6",
        "PySide6.QtWidgets",
        "PySide6.QtCore",
        "PySide6.QtGui",
        "numpy",
        "numpy.core",
        "numpy.lib",
        "numpy.random",
        "numpy.linalg"
    ],
    "includes": ["numpy_fix"],
    "include_files": include_files,
    "excludes": [
        "tkinter",
        "PySide6.QtAsyncio",
        "PySide6.QtAsyncio.events",
        "numpy.distutils",
        "numpy.f2py",
        "numpy.testing",
        "numpy.ma",
        "curses",
        "psutil"
    ],
    "include_msvcr": True,
    "bin_path_includes": [os.path.join(conda_env_path, "Library", "bin")],
    "optimize": 2
}



# Helper function to print build info to the console
def print_build_info():
    print("\nBuild Configuration:")
    print("=============================")
    print(f"Include files count: {len(include_files)}")
    print("Key include files:")
    for item in include_files:
        if isinstance(item, tuple) and len(item) == 2:
            src, dest = item
            if isinstance(src, str) and ("dll" in src.lower() or "platforms" in src.lower()):
                print(f"  - {src} \u2192 {dest}")
        elif isinstance(item, str):
            print(f"  - {item}")
    print("\nAfter building, check if these files exist in the build directory:")
    print("  - platforms/qwindows.dll")
    print("  - Qt6Core.dll, Qt6Gui.dll, Qt6Widgets.dll")
    print("  - qt.conf")
    print("=============================")

# Print build info
print_build_info()

# Define MSI installer options
shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "Sudoku Solver",          # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]SudokuSolver.exe",   # Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     "TARGETDIR"               # WkDir
     ),
    
    ("ProgramMenuShortcut",    # Shortcut
     "ProgramMenuFolder",      # Directory_
     "Sudoku Solver",          # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]SudokuSolver.exe",   # Target
     None,                     # Arguments
     "Sudoku Puzzle Application",    # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     "TARGETDIR"               # WkDir
     )
]

msi_data = {
    "Shortcut": shortcut_table
}

# Define setup options for MSI
bdist_msi_options = {
    "data": msi_data,
    "add_to_path": False,
    "initial_target_dir": r"[ProgramFilesFolder]\SudokuSolver"
}

setup(
    name="Sudoku Solver",
    version="1.0",
    description="Sudoku Solver Application with Qt platform support",
    author="Your Name",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options
    },
    executables=[
        Executable(
            "sudoku_solver.py",
            base="Win32GUI",  # Prevents console window from appearing
            target_name="SudokuSolver.exe",
            icon=None,  # You can add an icon file here if you have one
            shortcut_name="Sudoku Solver",
            shortcut_dir="ProgramMenuFolder",
            copyright="Copyright (c) 2025 Your Name"
        )
    ]
)
