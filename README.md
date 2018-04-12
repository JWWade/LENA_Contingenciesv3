# LENA_Contingencies - Version 3

GUI for computing contingency tables from .its and .csv files.

<img style="float:right;" src="./icon/LenaUI.jpg" height="400">

---
## For Users:

### How To Run

1. Install latest build from builds directory
    The build directory contains executables for MacOS,
    Linux, and Windows operating systems!
2. Run program from desktop shortcut
3. Setup input directory(for batch of .its files)
4. Setup output directory
5. Configure Analysis
6. Press Submit!

---
## For Developers:

###  How To Build The Program

####  Windows
  See:  

    windows_cmds.txt  

  in the root directory for full instructions on setting up pyinstaller and using the provided spec file to update the build for future developments.

####  MacOS & Unix
  To build the MacOS and Unix versions of the application for future releases, please install  

      pyinstaller  

  Once installed, execute the python script located in  

      ./buildScript/build_MacUnix.py  

  with  

      python build_MacUnix.py  

  This will bundle the app and place the executables in  

      ./builds/v3  
----
## Documentation & Manual

###  Doxygen

  This Project has been documented using Doxygen. To view the Doxygen documents generated from this project, see  

      ./manual/doxygen/index.html  

  Here you can see information about all related namespaces, classes, function, etc.

###  Manual

  A manual is available to users with step-by-step instructions and screenshots for using the program. To view, navigate to:  

    ./manual/manual.docx  

---    
## License

  This project is licensed under the MIT License

---
## Acknowledgments


* Program forked from https://github.com/kengbailey/LENA_Contingencies2  
and originally from https://github.com/HomeBankCode/LENA_contingencies
* Project completed Spring Semester 2018 @ MTSU CSCI Software Engineering
