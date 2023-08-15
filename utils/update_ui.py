import os

ui_files_dir = "./src/ui/desing_files"
ui_scripts_dir = "./src/ui/generated_files"
pyuic5_command = "pyuic5"
pyrcc5_command = "pyrcc5"


def convert_ui():
    total_files = 0
    
    # Get a list of all .ui files in the ui_files directory
    ui_files = [file for file in os.listdir(ui_files_dir) if file.endswith(".ui")]
    # Loop through each .ui file and generate the corresponding .py file
    for ui_file in ui_files:
        ui_file_path = os.path.join(ui_files_dir, ui_file)
        base_name = os.path.splitext(ui_file)[0]
        py_script_path = os.path.join(ui_scripts_dir, f"{base_name}.py")

        # Construct the pyuic5 command
        command = f"{pyuic5_command} {ui_file_path} -o {py_script_path}"

        # Run the command
        os.system(command)

        # Modify the generated .py file
        modified_lines = []
        with open(py_script_path, "r") as py_file:
            for line in py_file:
                if "import src_rc_rc" in line:
                    modified_lines.append(
                        line.replace("import src_rc_rc", "from ..generated_files import src_rc")
                    )
                else:
                    modified_lines.append(line)

        with open(py_script_path, "w") as py_file:
            py_file.writelines(modified_lines)

        total_files += 1
    return total_files


def convert_qrc():
    # Get a list of all .ui files in the ui_files directory
    qrc_files = [file for file in os.listdir(ui_files_dir) if file.endswith(".ui")]
    # Loop through each .ui file and generate the corresponding .py file
    for qrc_file in qrc_files:
        ui_file_path = os.path.join(ui_files_dir, qrc_file)
        base_name = os.path.splitext(qrc_file)[0]
        py_script_path = os.path.join(ui_scripts_dir, f"{base_name}.py")

        # Construct the pyuic5 command
        command = f"{pyrcc5_command} {ui_file_path} -o {py_script_path}"
        
        os.system(command)


if __name__ == "__main__":
    print(f"[+] Converting... UI files.")
    try:
        total_files = convert_ui()
    except Exception as e:
        print("[-] error updating Ui files")
        exit(e)

    print(f"[+] Converted {total_files} UI files.")
    print(f"[+] Converting... QRC file")

    try:
        convert_qrc()
    except Exception as e:
        print("[-] error convertin QRC files")
        exit(e)

    print(f"[+] Converted QRC file.")
