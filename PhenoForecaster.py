from pandas import read_csv
import Tkinter as tk
from os import getcwd as getcwd


################### Basic Files ##################
import ttk
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename
import tkFont
import sys


#read in model coefficients
basePath = getcwd()
ModelData = read_csv(basePath + '/PhenoForecaster_Ancillary_Files/Data_ForModel_NoMAECull.csv')
ModelData = ModelData.set_index(['Species'])
speciesList = list(ModelData.index)
ModelData.head()


# In[2]:



def speciesCheck(): #button press to update species count based on chosen MAE
    tempModelData = ModelData[ModelData['MAE']<=float(maxMAE.get())]
    speciesList = list(tempModelData.index)
    ttk.Label(MAESET_Frame, text="                                  ", font = "helvetica 14 bold").grid(column=0, row=2, pady = 5)
    ttk.Label(MAESET_Frame, text="# Species: " +  str(len(speciesList)), font = "helvetica 14 bold").grid(column=0, row=2, pady = 5)

def click_input(): #button press to select input file
    global filename_in
    filename_in = 'Fnord'
    filename_in = askopenfilename()
    print filename_in
    #action_inFile.configure(text =  filename_in)

def click_output(): #button press to select output file name
    global filename_out
    filename_out = 'DOY_Prediction.csv'
    filename_out = asksaveasfilename(defaultextension=".csv")
    #action_outFile.configure(text = filename_out)  
    
def click_runner_ManualEntry(): #button press to run phenological model with manually entered data
    species_Selected = str(species.get())
    bFFP_Selected = ModelData.loc[species_Selected, 'bFFP_Annual']

    NFFD_wt_Selected = ModelData.loc[species_Selected, 'NFFD_wt_Annual']
    
    NFFD_sp_Selected = ModelData.loc[species_Selected, 'NFFD_sp_Annual']

    PAS_wt_Selected = ModelData.loc[species_Selected, 'PAS_wt_Annual']

    PAS_sp_Selected = ModelData.loc[species_Selected, 'PAS_sp_Annual']
    
    intercept_Selected = ModelData.loc[species_Selected, 'Intercept']

    try: 
        BFFP_input = float(BFFP.get())
        PAS_wt_input = float(PAS_wt_in.get())
        PAS_sp_in_input = float(PAS_sp_in.get())
        NFFD_wt_in_input = float(NFFD_wt_in.get())
        NFFD_sp_in_input = float(NFFD_sp_in.get())
    except: 
        model_Window.bell() 
        output_cell.set('Non-Numeric Values Detected')
    
    output_Val = (BFFP_input * bFFP_Selected) + (NFFD_wt_in_input * NFFD_wt_Selected)     + (NFFD_sp_in_input * NFFD_sp_Selected) + (PAS_wt_input * PAS_wt_Selected)     + (PAS_sp_in_input * PAS_sp_Selected) + intercept_Selected

    
    output_cell.set(output_Val)
    

def predCalc_File(row):  #definition to calculate MFD to all rows
    return (row['bFFP'] * BFFP_Selected) + (row['NFFD_wt'] * NFFD_wt_Selected)     + (row['NFFD_sp'] * NFFD_sp_Selected) + (row['PAS_wt'] * PAS_wt_Selected)     + (row['PAS_sp'] * PAS_sp_Selected) + intercept_Selected


def click_runner_File(): #Button click to run model from csv
    global species_Selected
    species_Selected = str(species.get())
    
    global BFFP_Selected
    BFFP_Selected = ModelData.loc[species_Selected, 'bFFP_Annual']
    
    global NFFD_wt_Selected
    NFFD_wt_Selected = ModelData.loc[species_Selected, 'NFFD_wt_Annual']
    
    global NFFD_sp_Selected
    NFFD_sp_Selected = ModelData.loc[species_Selected, 'NFFD_sp_Annual']
    
    global PAS_wt_Selected
    PAS_wt_Selected = ModelData.loc[species_Selected, 'PAS_wt_Annual']
    
    global PAS_sp_Selected
    PAS_sp_Selected = ModelData.loc[species_Selected, 'PAS_sp_Annual']
    
    global intercept_Selected
    intercept_Selected = ModelData.loc[species_Selected, 'Intercept']

    global MAE_Selected
    MAE_Selected = ModelData.loc[species_Selected, 'MAE']
    
    inFile_init = read_csv(str(filename_in))
    inFile = inFile_init.dropna(subset = ['ID1', 'ID2', 'bFFP', 'NFFD_wt', 'PAS_wt', 'NFFD_sp'])
    inFile = inFile.reset_index(drop=True)
    lenDiff = 0
    if len(inFile_init) != len(inFile):
        lenDiff = len(inFile_init) - len(inFile)
        errorstring = 'Missing Data Detected: ' +  str(lenDiff) +  ' Rows deleted'
        
        msg.showwarning('PhenoPredict Data Processing Warning', errorstring)
    
    if outputType.get() == 0:
        outData = inFile.loc[:, ['ID1', 'ID2']]

    else:
        outData = inFile
        
    try: 
        outData['Expected_MAE'] = MAE_Selected
        outData['DOY_Predicted'] = inFile.apply(predCalc_File, axis=1)
        outData.to_csv(str(filename_out), index=False)
    except: 
        msg.showerror('PhenoPredict Data Processing Error', 'Fatal Error: Input Data does not match required Format')
    


# In[3]:


def model_reject(): #go back to species selection
    model_Window.destroy()
    species_window()


def model_open(): # open model window
    global model_Window
    
    global species_Selected
    species_Selected = str(species.get())
    
    global BFFP_Selected
    BFFP_Selected = ModelData.loc[species_Selected, 'bFFP_Annual']
    
    global NFFD_wt_Selected
    NFFD_wt_Selected = ModelData.loc[species_Selected, 'NFFD_wt_Annual']
    
    global NFFD_sp_Selected
    NFFD_sp_Selected = ModelData.loc[species_Selected, 'NFFD_sp_Annual']
    
    global PAS_wt_Selected
    PAS_wt_Selected = ModelData.loc[species_Selected, 'PAS_wt_Annual']
    
    global PAS_sp_Selected
    PAS_sp_Selected = ModelData.loc[species_Selected, 'PAS_sp_Annual']
    
    global intercept_Selected
    intercept_Selected = ModelData.loc[species_Selected, 'Intercept']

    global MAE_Selected
    MAE_Selected = ModelData.loc[species_Selected, 'MAE']
    
    model_Window = tk.Tk()

    # Add a title
    model_Window.title("Phenoclimate Model: " + str(species.get()))


    #disable resizing the GUI by passing in False/False - x, y
    model_Window.resizable(False, False)



    Button_Frame = ttk.LabelFrame(model_Window, text = "Alter Species Selection")
    Button_Frame.grid(column = 0, row = 0, padx = 5, pady = 5, sticky= tk.W)
    SpeciesChange = ttk.Button(Button_Frame, text = "Change Species", command = model_reject)
    SpeciesChange.grid(column = 0, row = 0, padx = 5, pady = 5, sticky = tk.E)



    #Frame For entry of climate variables
    ClimVars_Frame = ttk.LabelFrame(model_Window, text = "Climate Variables: Single Record")
    ClimVars_Frame.grid(columnspan  = 3, row = 1, padx = 5, pady = 5, sticky= tk.W)

    # Adding Label & Textbox Entry for climate data
    global PAS_wt_in
    PAS_wt_in = tk.DoubleVar()
    PAS_wt_in.set(0.0)
    PAS_wt_Label = ttk.Label(ClimVars_Frame, width=15, text = 'Winter PAS (mm)').grid(column = 0, row = 1, padx = 5, pady = 5)
    if PAS_wt_Selected!=0.0:
        PAS_wt_entry = ttk.Entry(ClimVars_Frame, width=12, textvariable=PAS_wt_in).grid(column = 1, row = 1, padx = 5, pady = 5)
    elif PAS_wt_Selected==0.0:
        PAS_wt_Label = ttk.Label(ClimVars_Frame, width=12, text = 'Not Required').grid(column = 1, row = 1, padx = 5, pady = 5)
    
    global PAS_sp_in
    PAS_sp_in = tk.DoubleVar()
    PAS_sp_in.set(0.0)
    PAS_sp_Label = ttk.Label(ClimVars_Frame, width=15, text = 'Spring PAS (mm)').grid(column = 0, row = 2, padx = 5, pady = 5)
    if PAS_sp_Selected!=0.0:
        PAS_sp_entry = ttk.Entry(ClimVars_Frame, width=12, textvariable=PAS_sp_in).grid(column = 1, row = 2, padx = 5, pady = 5)
    elif PAS_sp_Selected==0.0:
        PAS_wt_Label = ttk.Label(ClimVars_Frame, width=12, text = 'Not Required').grid(column = 1, row = 2, padx = 5, pady = 5)
    
        
    global NFFD_wt_in
    NFFD_wt_in = tk.DoubleVar()
    NFFD_wt_in.set(0.0)
    NFFD_wt_Label = ttk.Label(ClimVars_Frame, width=12, text = 'Winter NFFD').grid(column = 2, row = 1, padx = 5, pady = 5)
    if NFFD_wt_Selected!=0.0:
        NFFD_wt_entry = ttk.Entry(ClimVars_Frame, width=12, textvariable=NFFD_wt_in).grid(column = 3, row = 1, padx = 5, pady = 5)
    elif NFFD_wt_Selected==0.0:
        NFFD_wt_entry = ttk.Label(ClimVars_Frame, width=12, text = 'Not Required').grid(column = 3, row = 1, padx = 5, pady = 5)
    
        
    global NFFD_sp_in    
    NFFD_sp_in = tk.DoubleVar()
    NFFD_sp_in.set(0.0)
    NFFD_sp_Label = ttk.Label(ClimVars_Frame, width=12, text = 'Spring NFFD').grid(column = 2, row = 2, padx = 5, pady = 5)
    if NFFD_sp_Selected!=0.0:
        NFFD_sp_entry = ttk.Entry(ClimVars_Frame, width=12, textvariable=NFFD_sp_in).grid(column = 3, row = 2, padx = 5, pady = 5)
    elif NFFD_wt_Selected==0.0:
        NFFD_wt_entry = ttk.Label(ClimVars_Frame, width=12, text = 'Not Required').grid(column = 3, row = 2, padx = 5, pady = 5)
    
    global BFFP
    BFFP = tk.DoubleVar()
    BFFP.set(0.0)
    BFFP_Label = ttk.Label(ClimVars_Frame, width=12, text = 'DOY of BFFP').grid(column = 4, row = 1, padx = 5, pady = 5)
    if BFFP_Selected!=0.0:
        BFFP_entry = ttk.Entry(ClimVars_Frame, width=12, textvariable=BFFP).grid(column = 5, row = 1, padx = 5, pady = 5)
    elif BFFP_Selected==0.0:
        BFFP_entry = ttk.Label(ClimVars_Frame, width=12, text = 'Not Required').grid(column = 5, row = 1, padx = 5, pady = 5)
    
    
    runner_Manual = ttk.Button(ClimVars_Frame, text = "Calculate", command = click_runner_ManualEntry)
    runner_Manual.grid(column = 5, row = 2, padx = 5, pady = 5)

    #Frame For Output Display
    Output_Frame = ttk.LabelFrame(model_Window,text = 'Output')
    Output_Frame.grid(column = 1, row = 0, padx = 5, pady = 5, sticky= tk.W)

    #Field for Output Display
    nffd_sp_Label = ttk.Label(Output_Frame, text = 'Estimated DOY: ').grid(column = 0, row = 0, padx = 5, pady = 5)
    global output_cell
    output_cell = tk.StringVar()
    output_Entry = ttk.Entry(Output_Frame, width=28, textvariable = output_cell).grid(column = 1, row = 0, padx = 5, pady = 5)

    MAE_sp_Label = ttk.Label(Output_Frame, text = 'Expected Mean Absolute Error: '+ str(MAE_Selected) + ' Days').grid(column = 0, row = 1, padx = 5, pady = 5)


    #Frame For input Data
    File_Frame = ttk.LabelFrame(model_Window, text = "Climate Variables: Multiple Records")
    File_Frame.grid(columnspan = 5, row = 3, padx = 5, pady = 5, sticky= tk.W)

    #Adding a Label &  button for file input
    #File_In_Label = ttk.Label(File_in_Frame, width=12, text = 'Input File: ').grid(column = 0, row = 0, padx = 5, pady = 5)
    action_inFile = ttk.Button(File_Frame, text = "Select Climate Data File", command = click_input)
    action_inFile.grid(column = 0, row = 0, padx = 5, pady = 5, sticky = tk.E)


    #Adding a Label &  button for file output
    action_outFile = ttk.Button(File_Frame, text = "Specify Output Location", command = click_output)
    action_outFile.grid(column = 4, row = 0, padx = 5, pady = 5, sticky = tk.E)

    #Adding Button to Run File-based prediction
    runner_File = ttk.Button(File_Frame, text = "Calculate", command = click_runner_File)
    runner_File.grid(column = 5, row = 0, padx = 5, pady = 5, sticky = tk.E)

    #checkbutton to choose output type
    global outputType
    outputType = tk.IntVar()
    typeChecker = tk.Checkbutton(File_Frame, text="Retain All Input Data", variable=outputType)
    typeChecker.deselect()
    typeChecker.grid(column=0, row=2,  padx = 5, pady = 5, sticky=tk.W)  

    #========
    #Start GUI
    #========
    model_Window.mainloop()


# In[4]:


################## MAE_Select ################
# create MAE selection window
def MAE_Window():
    #set all global objects as global
    global MAESET_Frame
    global maxMAE
    global tempModelData
    global speciesList
    global MAE_Set
    
    MAE_Set = tk.Tk()

    # Add a title
    MAE_Set.title("PhenoForecaster 1.0")
    MAESET_Frame = ttk.LabelFrame(MAE_Set)
    MAESET_Frame.grid(column = 0, row = 0, padx = 5, pady = 5, sticky= tk.W)
      
    
    #disable resizing the GUI by passing in False/False - x, y
    MAE_Set.resizable(False, False)

    # Adding a Label
    ttk.Label(MAESET_Frame, text="Restrict Species Based on Required Model Accuracy:", font = "helvetica 14 bold").grid(column=0, row=0, pady = 5)

    ttk.Label(MAESET_Frame, text="Maximum Expected Mean Absolute Error (in days):", font = "helvetica 14 bold", ).grid(column=0, row=1, pady = 5)
    

    maxMAE = tk.IntVar()
    
    maxMAE_chosen = ttk.Entry(MAESET_Frame, width=12, textvariable=maxMAE).grid(column=1, row=1, pady = 10)
    maxMAE.set(15)
    print dummy
    
    tempModelData = ModelData[ModelData['MAE']<=float(maxMAE.get())]
    speciesList = list(tempModelData.index)
    

    ttk.Label(MAESET_Frame, text="# Species: " + str(len(speciesList)), font = "helvetica 14 bold").grid(column=0, row=2, pady = 5)

    speciesCheck_Button = ttk.Button(MAESET_Frame, text = "Check # Species", command = speciesCheck).grid(column=0, row=3, pady = 10)

    
    #Adding Button to acccept accuracy
    MAE_Accept = ttk.Button(MAESET_Frame, text = "Accept", command = species_open).grid(column=1, row=3, pady = 10)
    MAE_Set.mainloop()

    
def species_open():
    MAE_Set.destroy()
    species_window()


# In[5]:


def species_window(): #open species window
    global species
    global Species_Selector
    global dummy
    
    
    dummy = 1
    tempModelData = ModelData[ModelData['MAE']<=float(maxMAE.get())]
    speciesList = list(tempModelData.index)
    
    
    Species_Selector = tk.Tk()

    # Add a title
    Species_Selector.title("Species Selection")

    
    #disable resizing the GUI by passing in False/False - x, y
    Species_Selector.resizable(False, False)

    Species_Frame = ttk.LabelFrame(Species_Selector)
    Species_Frame.grid(column = 0, row = 0, padx = 5, pady = 5, sticky= tk.W)
    
    
    ttk.Label(Species_Frame, text="Species:", font = "helvetica 12 bold").grid(column=0, row=0, pady = 5)
    species = tk.StringVar()
    species.set('Please Select Species')
    species_chosen = ttk.Combobox(Species_Frame, width=21, textvariable=species, font = "helvetica 10 bold")
    species_chosen['values'] = speciesList
    species_chosen.grid(column=1, row=0, pady = 10)   
    
    Species_Accept = ttk.Button(Species_Frame, text = "Accept", command = species_accept).grid(column=1, row=1, pady = 10)
    Species_Reject = ttk.Button(Species_Frame, text = "Back", command = species_reject).grid(column=0, row=1, pady = 10)

def species_reject(): #go back to MAE selection window
    Species_Selector.destroy()
    MAE_Window()

def species_accept(): #accept chosen species, go to model window
    if species.get() != 'Please Select Species':
        Species_Selector.destroy()
        model_open()
    else:
        Species_Selector.bell()  
        


# In[6]:


#Run Program

global dummy
dummy = 0

MAE_Window()

