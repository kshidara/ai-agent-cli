import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_directory = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_directory, directory))
        # Will be True or False
        valid_target_dir = os.path.commonpath([absolute_directory, target_dir]) == absolute_directory  

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        items = os.listdir(target_dir)

        result = []
        
        for item in items:
            item_path = os.path.join(target_dir, item)
            file_size = os.path.getsize(item_path)
            is_directory = os.path.isdir(item_path)
            result.append(f"- {item}: file_size={file_size} bytes, is_dir={is_directory}"
)

        return "\n".join(result)

            
    except (ValueError, OSError) as e:
        return f"Error: {str(e)}"

    

    

        