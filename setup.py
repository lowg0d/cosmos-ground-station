from cx_Freeze import setup, Executable

# Define constants
APP_NAME = "cosmos"
VERSION = "1.0.0"
DEV_STATUS = "alpha"
AUTHOR = "Martin Ortiz"
DESCRIPTION = "asdasdasda"
COPYRIGHT = "Don't Copy"

# Print application information
print(f"[+] App: {APP_NAME}")
print(f"[+] Version: {DEV_STATUS}-{VERSION}")
print("[+] COOKING...")

# Define file paths
FILES = ['./src']
SCRIPT = "launcher.py"
BASE = "Win32GUI"
ICON_PATH = "./src/ui/resources/app.ico"
UPGRADE_CODE = '{017efcd7-1115-4248-a806-c75a182e2876}'
INCLUDE_PACKAGES = ["numpy", "numpy.core", "numpy.core.multiarray", "PyQt5"]
EXCLUDE_PACKAGES = []

# Define the executable target
TARGET = Executable(
    script=SCRIPT,
    base=BASE,
    icon=ICON_PATH,
    target_name=APP_NAME,
    shortcut_name=APP_NAME,
    shortcut_dir="DesktopFolder",
    copyright=COPYRIGHT
)

# Define data for installer
MSI_DATA = {
    "ProgId": [
        ("Prog.Id", None, None, f"{APP_NAME} installer", "IconId", None),
    ],
    "Icon": [
        ("IconId", ICON_PATH),
    ]
}

# Define exe options
EXE_OPTIONS = {
    'include_msvcr': True,
    'include_files': FILES,
    'packages': INCLUDE_PACKAGES,
    'excludes': EXCLUDE_PACKAGES
}

# Define bdist options
BDIST_OPTIONS = {
    'data': MSI_DATA,
    'upgrade_code': UPGRADE_CODE,
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\%s' % (APP_NAME),
    'install_icon': ICON_PATH
}

# Set up the application
setup(
    name=APP_NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    options={'build_exe': EXE_OPTIONS, 'bdist_msi': BDIST_OPTIONS},
    executables=[TARGET]
)
