import os
import sys

UI_RESOURCES_DIR = "./src/ui/resources"
UI_FILES_DIR = "./src/ui/desing_files"
UI_SCRIPTS_DIR = "./src/ui/generated_files"
PYUIC5_COMMAND = "pyuic5"
PYRCC5_COMMAND = "pyrcc5"


def convert_ui():
    """
    Converts .ui files to .py files using pyuic5 command.
    Modifies generated .py files to fix import statements.
    Returns the total number of files converted.
    """
    total_files = 0
    ui_files = [file for file in os.listdir(UI_FILES_DIR) if file.endswith(".ui")]
    for ui_file in ui_files:
        ui_file_path = os.path.join(UI_FILES_DIR, ui_file)
        base_name = os.path.splitext(ui_file)[0]
        py_script_path = os.path.join(UI_SCRIPTS_DIR, f"{base_name}.py")

        command = f"{PYUIC5_COMMAND} {ui_file_path} -o {py_script_path}"
        os.system(command)

        modified_lines = []
        with open(py_script_path, "r") as py_file:
            for line in py_file:
                if "import src_rc" in line:
                    modified_lines.append(
                        line.replace(
                            "import src_rc", "from ..generated_files import src_rc"
                        )
                    )
                else:
                    modified_lines.append(line)

        with open(py_script_path, "w") as py_file:
            py_file.writelines(modified_lines)

        total_files += 1
    return total_files


def convert_qrc():
    """
    Converts .qrc files to _rc.py files using pyrcc5 command.
    """
    qrc_files = [file for file in os.listdir(UI_RESOURCES_DIR) if file.endswith(".qrc")]
    for qrc_file in qrc_files:
        ui_file_path = os.path.join(UI_RESOURCES_DIR, qrc_file)
        base_name = os.path.splitext(qrc_file)[0]
        py_script_path = os.path.join(UI_SCRIPTS_DIR, f"{base_name}_rc.py")

        command = f"{PYRCC5_COMMAND} {ui_file_path} -o {py_script_path}"
        os.system(command)


if __name__ == "__main__":
    print("[+] Converting UI files...")
    try:
        total_ui_files = convert_ui()
        print(f"[+] Converted {total_ui_files} UI files.")
    except Exception as e:
        print("[-] Error updating UI files")
        sys.exit(e)

    print(f"[+] Converting QRC files...")
    try:
        convert_qrc()
        print("[+] Converted QRC files.")
    except Exception as e:
        print("[-] Error converting QRC files")
        sys.exit(e)
