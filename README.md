# HDR-gdmomacro
Simple macro recorder for the mmo game GDMO that uses tesseract/pytesseract for OCR.
Created as a simple project to learn how to create GUIs with PySimpleGui and how to work with OCR.
Project has some other unused functionalities, like selecting a macro, or editing one, 
where selecting a macro(py script file) is required to start the macro recorder, 
but whats in that py script file doesnt matter, 
leftover feature for wanting to expand the project into other games, 
might help out others that are looking to create a similar looking gui etc 

Macro recorder does work inside of the game, you need a digimon.json inside the folder which the script file is in.
Simply choose what digimon you want to target after modifying the digimon.json file and then choose the color that its name uses (based on level)

Issues:
-Sometimes get stuck
-Sometimes doesnt recognize the mob you are searching for if it has a (leader) prefix
-Has a bit of a delay that stems from opencv operations/ocr

Modules used:
-pytesseract
-numpy
-scipy
-PySimpleGui
-json
-pyautogui
-os
-sys
-cv2
-threading
-itertools
-time
-keyboard


I am not responsible for any bans/kicks/warns etc inside GDMO or any other MMO, for using this "macro recorder", or any modified version of it.
