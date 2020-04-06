@ECHO OFF 
:: This batch file reveals OS, hardware, and networking configuration.
TITLE Creating Python exec
ECHO Please wait...
:: Section 1: OS information.
ECHO ============================
ECHO PyInstaller specs 
ECHO ============================
pyi-makespec --debug=imports --onefile -n TrinamGUI --paths=G:\Developpement_de_Programmes\Programmes\octo-trigui\TMCM TrinamGUI.py
ECHO ============================
ECHO Building Executable
ECHO ============================
pyinstaller --onefile TrinamGUI.py --noconsole
ECHO ============================
ECHO Done
ECHO ============================