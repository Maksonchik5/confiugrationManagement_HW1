# Virtual File System Shell Emulator

This project provides a Python-based shell emulator that operates on a virtual file system within a `.tar` archive. The shell supports basic file system operations such as listing directory contents, changing directories, copying files, and running startup scripts.

## Features

- **List directory contents** (`ls`)
- **Change directory** (`cd`)
- **Copy files** within the virtual file system (`cp`)
- **Execute commands from a startup script** to initialize the virtual environment
- **Clear screen** (`clear`)
- **Exit** the shell (`exit`)

## File Structure

- `VirtualFileSystem`: The core class for managing file operations within a `.tar` archive.
- `ShellEmulator`: Provides a command-line interface for interacting with the virtual file system.
- `conf.json`: Configuration file for initializing the shell emulator.
- `startup_script`: Script with predefined commands that the shell will execute at startup.

## Configuration

The configuration is managed through a JSON file (`conf.json`) with the following structure:

```json
{
    "username": "maksim",
    "tar_path": "/path/to/your/tar_file.tar",
    "start_script": "/path/to/your/startup_script"
}

