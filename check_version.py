#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script checks the embedded version of a running Windows process.

I use it along with BGInfo to display the running FairCom server version on the desktop.

It can be automated with a batch file similar to this:

@echo off
"C:\\Users\\adam.howell\\AppData\\Roaming\\Python\\Scripts\\uv.exe" run "C:\\Source\\GitHub\\FairComVersion\\.venv\\Scripts\\python.exe" "C:\\Source\\GitHub\\FairComVersion\\check_version.py" faircom.exe -o "C:\\temp\\faircom_version.txt" -t
"C:\\Util\\BGInfo\\Bginfo64.exe" "C:\\temp\\faircom_bginfo.bgi" /timer:0 /silent /nolicprompt

Then run that batch script in Task Scheduler, set to "Run only when user is logged on" so it updates the displayed desktop.
"""

import argparse
import datetime
import logging
import pathlib

import psutil
from win32api import GetFileVersionInfo, LOWORD, HIWORD

logger = logging.getLogger( __name__ )
logger.setLevel( logging.DEBUG )


def get_process_exe( process_name: str ) -> pathlib.Path | None:
    """
    Check if a process is running and return its executable path.

    :param process_name: The name of the process to look for.
    :return: The executable path of the process if found, None otherwise.
    """
    for process in psutil.process_iter( attrs = ["name", "exe"] ):
        try:
            if process.info["name"] == process_name:
                return pathlib.Path( process.info["exe"] )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None


def get_windows_file_version( exe_path: pathlib.Path ) -> str:
    """
    Reads the embedded FileVersion property from a Windows executable.
    Does not run the executable, avoiding hangs and server start-ups.

    :param exe_path: The path to the executable to look for.
    :return: The version of the executable to look for.
    """
    if not exe_path.is_file():
        return "Executable path not found."

    try:
        logger.debug( f"Attempting to read version info from: {exe_path}" )
        # Get the embedded version info from the .exe
        info = GetFileVersionInfo( str( exe_path ), "\\" )
        logger.debug( f"Retrieved version info for {exe_path.name}: {info}" )
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return f"{HIWORD( ms )}.{LOWORD( ms )}.{HIWORD( ls )}.{LOWORD( ls )}"
    except Exception as exception:
        logger.exception( f"Could not read version metadata from {exe_path}: {exception}", exception )
    return "Version info not found."


def check_process_version( process_name: str, output_file: pathlib.Path | None = None, add_timestamp: bool = False ) -> None:
    """
    Find the process, format the output, and optionally save it.

    :param process_name: The name of the process to look for.
    :param output_file: The path to write the output to.
    :param add_timestamp: Add the current time to the output string.
    """
    exe_path = get_process_exe( process_name )

    if exe_path and exe_path.is_file():
        version_output = get_windows_file_version( exe_path )
        status_text = f"Running v{version_output}"
    else:
        status_text = "Not Running"
        logger.debug( f"Could not find the process: {process_name}" )

    # Append the timestamp if requested.
    if add_timestamp:
        now = datetime.datetime.now().strftime( "%H:%M" )
        status_text += f" - {now}"
    logger.debug( f"Status: {status_text}" )

    # Write to file if requested.
    if output_file:
        # Create the directory if needed.
        check_create_directory( output_file.parent )
        try:
            with open( output_file, "w" ) as f:
                f.write( status_text )
            logger.debug( f"Successfully wrote status to: {output_file}" )
        except Exception as exception:
            logger.exception( f"Failed to write to {output_file}: {exception}", exception )


def check_create_directory( directory: pathlib.Path ) -> bool:
    """
    This will check for the existence of a directory and create it if it does not exist.
    This will also create any intermediate directories that do not exist.

    :param directory: The directory to check and create.
    :return: True if the directory was created or if it already existed.
    """
    try:
        if not directory.is_dir():
            # The inclusion of exist_ok=True should not be necessary in this case but clarifies this code.
            directory.mkdir( parents = True, exist_ok = True )
    except OSError as os_error:
        logger.exception( f"Error: Could not create the directory '{directory}': {os_error}", os_error )
        return False
    return directory.is_dir()


if __name__ == "__main__":
    # Set up the argument parser.
    parser = argparse.ArgumentParser( description = "Check the embedded version of a running Windows process." )
    parser.add_argument( "process_name", type = str, help = "The name of the process to check (e.g., faircom.exe)" )
    parser.add_argument( "-o", "--output", type = pathlib.Path, help = "Filepath to write the output to", default = None )
    parser.add_argument( "-t", "--timestamp", action = "store_true", help = "Append the current time to the output string" )

    # Parse the arguments passed from the command line.
    args = parser.parse_args()

    # Run the check with the provided argument.
    check_process_version( args.process_name, args.output, args.timestamp )
