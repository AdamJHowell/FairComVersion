## This script checks the embedded version of a running Windows process.

I use it along with [BGInfo](https://learn.microsoft.com/en-us/sysinternals/downloads/bginfo) to display the running FairCom server version on the desktop.

### Steps to automate:

1. Run `check_version.py` once to create the output file in a location where it is safe for your account to store data:
   `python check_version.py faircom.exe -o C:\temp\faircom_version.txt`
2. Launch BGinfo64.exe
3. Under the `Fields` list on the right, create a `Custom` field.
4. Set it to `Contents of a file` and set the `Path` to a path and filename in a location where it is safe for your account to store data.  Note this filepath.
5. Click `<-Add` to add the custom field to the desktop.
6. Adjust other fields to suit your preferences.
7. Use `File->Save As...` to save that configuration to a .bgi file.  Note this filepath.

```cmd
@echo off
"C:\Users\adam.howell\AppData\Roaming\Python\Scripts\uv.exe" run "C:\Source\GitHub\FairComVersion\.venv\Scripts\python.exe" "C:\Source\GitHub\FairComVersion\check_version.py" faircom.exe -o "C:\temp\faircom_version.txt" -t
"C:\Util\BGInfo\Bginfo64.exe" "C:\temp\faircom_bginfo.bgi" /timer:0 /silent /nolicprompt
```

Then run that batch script in Task Scheduler, set to `Run only when user is logged on` so it updates the displayed desktop.
