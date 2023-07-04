from PIL import Image, ImageGrab
import PIL
import pytesseract as pt
import numpy as np
import scipy as sp
import PySimpleGUI as sg
import json
import pyautogui as pag
import os
import sys
import cv2 as cv
import threading as td
import itertools as it
import time as t
import keyboard as k

### Setting active folder to where the script file is located

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
botFolderPath = os.path.dirname(os.path.abspath(sys.argv[0]))
pag.FAILSAFE = False

### Setting path to macro folder, creating macro folder if it doesnt exist

macroFolderPath = os.path.join(botFolderPath, "Macros")

isExist = os.path.exists(macroFolderPath)

if not isExist:
    os.mkdir(os.path.join(botFolderPath, "Macros"))

### Global variables

stop = None
stuckCounter = 0
selectedMacro = "None"

### Colors that are used for OCR

colors = {
    "DeepRed" : {"minValue" : np.array([0, 151, 191]), "maxValue" : np.array([10, 225, 255])},
    "Red" : {"minValue" : np.array([0, 71, 207]), "maxValue" : np.array([8, 90, 255])},
    "White" : {"minValue" : np.array([0, 0, 216]), "maxValue" : np.array([112, 15, 255])},
    "RealLightBlue" : {"minValue" : np.array([109, 53, 209]), "maxValue" : np.array([119, 92, 255])},
    "LightBlue" : {"minValue" : np.array([109, 30, 166]), "maxValue" : np.array([116, 140, 255])},
    "DarkBlue" : {"minValue" : np.array([115, 163, 154]), "maxValue" : np.array([125, 239, 211])},
    "Gray" : {"minValue" : np.array([0, 0, 182]), "maxValue" : np.array([74, 20, 190])}
    
}

### OCR and Macro function

def imageGrab():
    global image
    chosenColor = window1["-COLORS-"].get()     ### Taking a screenshot and then modifying it with opencv
    src = PIL.ImageGrab.grab()
    src.save("test.png")
    imagePath = os.path.join(botFolderPath, "test.png")
    image = cv.imread(imagePath)
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, (colors[chosenColor]["minValue"]), (colors[chosenColor]["maxValue"]))        ### Selected color is the only one that is going to be left on the image, easier for the ocr to read the font
    imask = mask>0
    done = np.zeros_like(image, np.uint8)
    done[imask] = image[imask]
    data = pt.image_to_data(done, output_type="dict")       ### Using pytesseract to OCR the image and put the data from it into a dictionary
    boxes = len(data["level"])
    searchWord = window1["-DIGIMONCOMBO-"].get()        ### Selected in main window
    for i in range(boxes):      ### Extract all box ids
        if data["text"][i] == searchWord:       ### Looks for the word we are looking for inside the data dictionary
            print(data["left"][i], data["top"][i], data["text"][i])     ### Prints the X and Y position of the bounding box that contains the word we are looking for
            pag.moveTo(data["left"][i]+10, data["top"][i]+55)       ### Moves mouse to that bounding box, generic pyautogui actions
            pag.mouseDown(button="left")
            pag.mouseUp(button="left")
            t.sleep(2)
            pag.press("tab")        ### Targets mob
            imgCrop = PIL.ImageGrab.grab()      ### Taking a screenshot and modifying it with opencv again to check if we are targeting the right mob
            imgCrop.save("imagetocrop.png")
            imgCrop = cv.imread("imagetocrop.png")
            croppedImage = imgCrop[0:50, 1100:1440]
            hsvCrop = cv.cvtColor(imgCrop, cv.COLOR_BGR2HSV)
            maskCrop = cv.inRange(hsvCrop, np.array([0, 0, 135]), np.array([128, 45, 255]))     ### Color values here are constant, since the color doesnt change based on different mobs
            croppedMask = maskCrop[0:50, 1100:1440]
            imaskCrop = croppedMask>0
            doneCrop = np.zeros_like(croppedImage, np.uint8)
            doneCrop[imaskCrop] = croppedImage[imaskCrop]
            dataCrop = pt.image_to_data(doneCrop, output_type="dict")
            boxesCrop = len(dataCrop["level"])
            for i in range(boxesCrop):      ### Extract all box ids
                if dataCrop["text"][i] == searchWord:       ### Looks for the word we are looking for inside the dataCrop dictionary, generic pyautogui actions
                    pag.press("1")
                    t.sleep(5)
                if dataCrop["text"][i] == "(leader)" + searchWord:       ### Looks for the word we are looking for inside the dataCrop dictionary, with the (leader) prefix, generic pyautogui actions  
                    pag.press("1")
                    t.sleep(5) 
    else:       ### If searchWord is not on screen, executes this to rotate the screen and try to find the searchWord
        pag.drag(15, 0, 1, button="right")
        global stuckCounter
        stuckCounter = stuckCounter + 1
        print(stuckCounter)
        if stuckCounter == 3:       # If it rotated 3 times, itll rotate 180 degrees and click at given X and Y coordinates
            stuckCounter = 0
            pag.drag(45, 0, 1, button="right")
            pag.moveTo(1280, 1080)
            pag.mouseDown(button="left")
            pag.mouseUp(button="left")
            t.sleep(2)

        


### Function for looping the imageGrab() function a set amount of times

def timeLoop():
    if infiniteLoop is False:
        for i in it.repeat(None, loopNumber):
            imageGrab()
            if k.is_pressed("o"):       ### Emergency stop hotkey
                global stop
                stop = True
                if stop == True:
                    stop = None
                    break  
      
### Function for looping the imageGrab() function infinite amount of times

def timeLoopInf():
    if infiniteLoop is True:
        for i in it.repeat(None):
            imageGrab()
            if k.is_pressed("o"):       ### Emergency stop hotkey
                global stop
                stop = True
                if stop == True:
                    stop = None
                    break       

   
### Function for opening the editMacro window, unused

"""def editMacro():
    os.chdir(macroFolderPath)
    with open (f"{macroToEdit}") as mFile:
        macroFile = mFile.read()
        
        

    buttonColumn = [[sg.Button("text")], 
                    [sg.Button("text")], 
                    [sg.Button("text")], 
                    [sg.Button("text")], 
                    [sg.Button("text")], 
                    [sg.Button("text")]
                    ]
                    
    macroScript = [[sg.Multiline(size = (80, 20), default_text=macroFile, background_color="white", text_color="black", key="-MACROSCRIPT-")]]

    layout = [
        [
        sg.Column(macroScript),
        sg.VSeparator(),
        sg.Column(buttonColumn),
        ]    
    ]

    global window4
    window4 = sg.Window("Macro Editing", layout, modal=True)

    while True:
        event, values = window4.read()
        if event == "-MACROEDITEXIT-" or event == sg.WIN_CLOSED:
            window4.close()
            break"""

### Function that refreshes the macro list window whenever its called

def refreshMacroList():
    currentFolder = window2["-MACROFOLDER-"].get()
    file_list = os.listdir(os.path.join(botFolderPath, currentFolder))
                
    fnames = [
            f for f in file_list
                if os.path.isfile(os.path.join(window2["-MACROFOLDER-"].get(), f)) and f.lower().endswith((".py"))
            ]    
    window2["-MACROLIST-"].update(fnames)  

### Function that opens the creating macro window

def createNewMacro():

    layout = [

            [sg.Input("", enable_events=True, focus=True, key="-INPUTMACRONAME-")],
            [sg.Button("Confirm", key="-CONFIRMMACRONAME-"), sg.Button("Cancel", key="-CANCELMACROCREATION-")]
        ]
    
    global window3
    window3 = sg.Window("Macro creation", layout, modal=True)

    while True:
        event, values = window3.read()
        if event == "-CANCELMACROCREATION-" or event == sg.WIN_CLOSED:
            window3.close()
            break
        if event == "-CONFIRMMACRONAME-":
            macroName = values["-INPUTMACRONAME-"]
            os.chdir(window2["-MACROFOLDER-"].get())
            open(f'{macroName}.py', "w")
            os.chdir(botFolderPath)

            window3.close()
            break
    
    window3.close()

### Function that opens the macro window

def openMacroWindow():
    macroViewerColumn = [
        [       
            sg.Text("Macro Folder"),
            sg.In(size=(25,1), enable_events=True, key="-MACROFOLDER-"),
            sg.FolderBrowse(initial_folder=macroFolderPath, key="-MACROFOLDERBROWSE-"),
        ],
        [
            sg.Listbox(values=[], enable_events=True, size=(40,20), key="-MACROLIST-", select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)
        ],
    ]
    
    buttonColumn = [
        [sg.Button("New Macro", key="-NEWMACRO-",)],
        [sg.Button("Delete macro", key="-DELETEMACRO-")],
        [sg.Button("Select Macro", key="-SELECTMACRO-")],
        [sg.Button("Exit", key="-MACROEXIT-")],
        [sg.Button("Edit Macro", key="-EDITMACRO-", visible=False)]
    ]
    layout = [
        [
            sg.Column(macroViewerColumn),
            sg.VSeparator(),
            sg.Column(buttonColumn),
        ]
    ]
    global window2
    window2 = sg.Window("Macros", layout, modal=True)

    while True:
        event, values = window2.read()
        if event == "-MACROEXIT-" or event == sg.WIN_CLOSED:
            window2.close()
            break
        if event == "-MACROFOLDER-":
            refreshMacroList()     
        if event == "-NEWMACRO-":
            createNewMacro()
            refreshMacroList() 
        if event == "-SELECTMACRO-":
                global selectedMacro 
                selectedMacro = window2["-MACROLIST-"].get()
                selectedMacro = selectedMacro[0]
                global selectedMacroPath 
                selectedMacroPath = os.path.join(window2["-MACROFOLDER-"].get(), selectedMacro)
                print(selectedMacroPath)
                print(selectedMacro)
                
                window2.close()
                break
        if event == "-DELETEMACRO-":
            if window2["-MACROLIST-"]:
                macroToDelete = window2["-MACROLIST-"].get()
                macroToDelete = macroToDelete[0]
                macroToDeletePath = os.path.join(window2["-MACROFOLDER-"].get(), macroToDelete)
                os.remove(macroToDeletePath)
                refreshMacroList()
        if event == "-EDITMACRO-":
            if window2["-MACROLIST-"]:
                global macroToEdit
                macroToEdit = window2["-MACROLIST-"].get()
                macroToEdit = macroToEdit[0]
                global macroToEditPath
                macroToEditPath = os.path.join(window2["-MACROFOLDER-"].get(), macroToEdit)
                editMacro()



sg.theme('DarkAmber')

### digimon.json used to populate "-DIGIMONCOMBO-" combobox, value used for searchWord variable

with open("digimon.json") as json_file:
    digimonList = json.load(json_file)

digimonListForCombo = list(digimonList.values())

### Main layout

layout = [
    [sg.Text("Autofarm v1.0")],
    [sg.Combo(digimonListForCombo, size = (35, 1), key="-DIGIMONCOMBO-")],
    [sg.Combo(list(colors.keys()), size = (10, 1), key = "-COLORS-")],
    [sg.Button("None", enable_events=False, key="-SELECTEDMACROINFO-"), sg.Input("Loop amount", enable_events=True, size=(20, 1), key="-LOOPAMOUNT-"), sg.Checkbox("Infinite", key="-INFINITECHECKBOX-")],
    [sg.Button("Macro", key="-MACRO-"), sg.Button("Start", key="-START-"), sg.Push(), sg.Button("Exit", key="-EXIT-")],
    [sg.Button(visible=False)]

]

window1 = sg.Window("Demo", layout, finalize=True)

### Main event loop

while True:
    event, values = window1.read()
    if event == "-EXIT-" or event == sg.WIN_CLOSED:
        break
    if event == "-MACRO-":
        openMacroWindow()
        window1["-SELECTEDMACROINFO-"].update(selectedMacro)
    if event == "-START-":
        infiniteLoop = window1["-INFINITECHECKBOX-"].get()
        if infiniteLoop == False:
            loopNumber = window1["-LOOPAMOUNT-"].get()
            if loopNumber.isdigit():
                loopNumber = int(loopNumber)
                timeLoop()
            else:
                pass
        if infiniteLoop == True:
            timeLoopInf()

    


window1.close()