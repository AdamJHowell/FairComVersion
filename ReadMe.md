# FairCom Version

## This script checks the version of a running Windows process.

This will be able to check nearly any Windows executable and return the version information stored in the file.  This means it will not be able to report some system processes like `System`, `System Idle Process`, or `Registry`.  It searches process list by the executable name.

I use it along with [BGInfo](https://learn.microsoft.com/en-us/sysinternals/downloads/bginfo) to display on the desktop the running FairCom server version.

### Steps to automate:

TL/DR: Automate check_version.py using -o to output to a file, then automate BGInfo to read from that file for one of the fields.

1. Run `check_version.py` once to create the output file in a location where it is safe for your account to store data:
   `python check_version.py faircom.exe -t -o C:\temp\faircom_version.txt`  Note the name of the output file.
2. Launch BGinfo64.exe
3. Under the `Fields` list on the right, create a `Custom` field.
4. Set it to `Contents of a file` and set the `Path` to the location of the output file from step 1.
5. Click `<-Add` to add the custom field to the desktop.
6. Adjust other fields to suit your preferences.
7. Use `File->Save As...` to save that configuration to a .bgi file.  Note the name of this file.
8. Launch Task Scheduler.
9. Click `Create Task...` in the right pane.
10. On the `General` tab give it a name and select `Run only when user is logged on` so it updates the displayed desktop.
11. On the `Triggers` tab check the `Repeat task every:` checkbox and set it to an interval you prefer.  Click `OK`.
12. On the `Actions` tab click `New...`.
13. Leave it on `Start a program` and Browse to `pythonw.exe` for the Python version you wish to use.
14. For the arguments, use this: `C:\<full path>\check_version.py faircom.exe -o C:\temp\faircom_version.txt -t`, but adjusted for the full path to `check_version.py` and the output file from step 1.  If any path has spaces in it, you must wrap it in double-quotes.
15. For the Start in path, use the directory that `check_version.py` is located in.  Click `OK`.
16. Click `New...` again.
17. Leave it on `Start a program` and Browse to `Bginfo64.exe`.
18. For the arguments, use this: `C:\temp\faircom_bginfo.bgi /timer:0 /silent /nolicprompt`, but adjusted for the path from step 7.  Click `OK`.
19. Click `OK` to save the task.
20. Locate the task in the middle pane, right-click on it and select `Run`.  The desktop should update to show the most recent time checked.

## ToDo:

* Standardize the FairCom server version to FCDB (e.g., Edge v5.1.0.95 would return 13.1.0.95)
* Linux version
