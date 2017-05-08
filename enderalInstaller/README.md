# Alternative Enderal installer

This Python 3 script provides an alternative installation method for the Skyrim mod "Enderal". It is designed for advanced users who are used to use the command line. It is no general replacement for the original launcher which is much better suited for normal users. The script aims to provide a workaround in case of launcher problems and in the following special use cases:
- Installation of Enderal on Linux/Wine (this is hardly possible with the original launcher because it depends on the .NET Framework)
- Archivation of all required Enderal patches for offline installation

## Features
- No .NET Framework dependencies
- Download and save patches locally for archivation
- Offline installation from archived patches
- Simple INI generation with different detail levels

## Usage
- Install Skyrim normally via Steam
- Place the script in your SteamLibrary/steamapps/common directory
- Create a directory named \_\_cache\_\_ next to the script
- Download the Enderal installation package from <https://enderal.com/> and place it in the \_\_cache\_\_ directory
- Run this script from command line to install Enderal and download all required patches, a backup of the Skyrim directory is created in the \_Skyrim\_bak directory
- All missing patches are saved to the \_\_cache\_\_ directory and can be archived.

The most common command line on Linux would be:
```
WINEPREFIX=~/.wine/YOUR_WINE_PREFIX_HERE ./installEnderal.py --wine --config --install --language YOUR_LANGUAGE
```
or on Windows:
```
installEnderal.py --config --install --language YOUR_LANGUAGE
```

This script cannot update an existing installation yet. To do so, a clean reinstallation from the created backup directory is required.

To show all available command line options run the script without any arguments.

