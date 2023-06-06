# Description of Healfy_diary_APP
This project will help you with your diet, to calculate your calories.

Now I'll connect Python program text with other program files, but you may compilate it in app with some Python libriares:)

## Confertate Into App
For example:
 1) Install the **pyinstaller** libriary by comand **pip install pyinstaller**
 2) Put all files in one folder with some name (This is necessary for your convenience and the correct operation of the program)
 3) Now you need open **CLI** (Win + R, CMD in Windows, Bash in Linux, I didn't work with MacOS:))
 4) Change directory, to folders with download files (in Windows and Linux you need to write comand **cd *full path to the directory***)
 5) Write the comand **pyinstaller --onefile --noconsole main.py** in **CLI** (--onefile compiles the program into a single exe file. This is convenient if the program is small, it has few graphics, audio and other files that are not related to the program code. --noconsole. If you do not write this modifier, then, in addition to the program window, the Python console will open. Sometimes, for example, for debugging, it is convenient to leave the command line to display system messages, but when transferring the program to the client, the console is usually hidden)
 6) Now **pyinstaller** create 2 directories. In **dist** folder you can find one .exe program. Now you need to copy all fails from directory in 
point 2, to **dist** folder. Now you can open .exe file and it will work.
That's all, thanks:)

## Support with some problems

If you encounter troubles and malfunctions in the application, and you have ideas for improvement, send your suggestions to me by mail **chemodanov.petr.06@gmail.com__. I will answer for all your questions
