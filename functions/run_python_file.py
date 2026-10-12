
import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a Python file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the Python file to run, relative to the working directory",
                },
            },
        },
    },
}


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:

    try:
            absolute_directory = os.path.abspath(working_directory)
            target_file = os.path.normpath(os.path.join(absolute_directory, file_path))
            valid_target_path = os.path.commonpath([absolute_directory, target_file]) == absolute_directory 
    
            if not valid_target_path:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
            if not os.path.isfile(target_file):
                return f'Error: "{file_path}" does not exist or is not a regular file'

            if not file_path.endswith(".py"):
                return f'Error: "{file_path}" is not a Python file'

            command = ["python", target_file]
            if args:
                command.extend(args)

            completed_process = subprocess.run(command, cwd=absolute_directory, capture_output=True, text=True, timeout=30)

            output_string = ""
            if completed_process.returncode != 0:
                output_string += f"Error: Process exited with code {completed_process.returncode}"
            if not completed_process.stdout and not completed_process.stderr:
                output_string += "Error: No output produced"

            output_string += f"\nSTDOUT:\n{completed_process.stdout}\nSTDERR:\n{completed_process.stderr}"

            return output_string.strip()
    
    except (ValueError, OSError) as e:
        return f"Error: executing Python file: {e}"

