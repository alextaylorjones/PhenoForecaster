from pandas import read_csv
import Tkinter
from os import getcwd

MinSamples = 100
speciesNum = 99999
crossValNum = 25
varListName = 'SeasonOnly'

#coeffs = pd.read_csv('C:\Users\IWP_Canopy/Dropbox/Herbarium_2017/Pheno_Assessed_3/Model_App/Model/Analysis_Results/elastic_Coeffs' + str(MinSamples) + '_' + varListName + "_" + str(crossValNum) + 'Fold_AngiospermOnly_VariableSeasons_3vars.csv')
basePath = getcwd()
ModelData = read_csv(basePath + '/PhenoPredict_Ancillary_Files/Data_ForModel.csv')
ModelData = ModelData.set_index(['Species'])
speciesList = list(ModelData.index)
ModelData.head()


# In[2]:


def click_runner_ManualEntry():
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
        win.bell()
        output_cell.set('Non-Numeric Values Detected')

    output_Val = (BFFP_input * bFFP_Selected) + (NFFD_wt_in_input * NFFD_wt_Selected)     + (NFFD_sp_in_input * NFFD_sp_Selected) + (PAS_wt_input * PAS_wt_Selected)     + (PAS_sp_in_input * PAS_sp_Selected) + intercept_Selected


    output_cell.set(output_Val)


    MAE_Selected = ModelData.loc[species_Selected, 'MAE']
    MAE_cell.set(MAE_Selected)
   #output_cell.set('trht')


# In[ ]:




def predCalc_File(row):  #definition to pply atan to all rows
    return (row['bFFP'] * bFFP_Selected) + (row['NFFD_wt'] * NFFD_wt_Selected)     + (row['NFFD_sp'] * NFFD_sp_Selected) + (row['PAS_wt'] * PAS_wt_Selected)     + (row['PAS_sp'] * PAS_sp_Selected) + intercept_Selected


def click_runner_File():
    global species_Selected
    species_Selected = str(species.get())

    global bFFP_Selected
    bFFP_Selected = ModelData.loc[species_Selected, 'bFFP_Annual']

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
        outData.to_csv(str(filename_out))
    except:
        msg.showerror('PhenoPredict Data Processing Error', 'Fatal Error: Input Data does not match required Format')



# In[ ]:



import Tkinter as tk
import ttk
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename



################## GUI ################
# Create instance
win = tk.Tk()

# Add a title
win.title("PhenoPredict 1.0")


#disable resizing the GUI by passing in False/False - x, y
win.resizable(False, False)


# Adding a Label
#ttk.Label(win, text = "A Label").grid(column=0, row=3)

speciesFrame = ttk.LabelFrame(win, text = "Species Selection")
speciesFrame.grid(column = 0, row = 0, padx = 5, pady = 5, sticky= tk.W)



#Button click event function

def click_input():
    global filename_in
    filename_in = 'Fnord'
    filename_in = askopenfilename()
    print filename_in
    #action_inFile.configure(text =  filename_in)




def click_output():
    global filename_out
    filename_out = 'DOY_Prediction.csv'
    filename_out = asksaveasfilename(defaultextension=".csv")
    #action_outFile.configure(text = filename_out)



# add in a dropdown to select species
ttk.Label(speciesFrame, text="Species:", font = "helvetica 11 bold").grid(column=0, row=0, pady = 5)
species = tk.StringVar()
species_chosen = ttk.Combobox(speciesFrame, width=20, textvariable=species, font = "helvetica 10 bold")
species_chosen['values'] = speciesList
species_chosen.grid(column=1, row=0, pady = 10)                         # <= Combobox in column 1
species_chosen.current(0)


#Frame For entry of climate variables
ClimVars_Frame = ttk.LabelFrame(win, text = "Climate Variables: Single Record")
ClimVars_Frame.grid(columnspan  = 3, row = 1, padx = 5, pady = 5, sticky= tk.W)

# Adding Label & Textbox Entry for climate data
PAS_wt_in = tk.DoubleVar()
PAS_wt_in.set(0.0)
PAS_wt_Label = ttk.Label(ClimVars_Frame, width=15, text = 'Winter PAS (mm)').grid(column = 0, row = 1, padx = 5, pady = 5)
PAS_wt_entry = ttk.Entry(ClimVars_Frame, width=12, textvariable=PAS_wt_in).grid(column = 1, row = 1, padx = 5, pady = 5)


PAS_sp_in = tk.DoubleVar()
PAS_sp_in.set(0.0)
PAS_sp_Label = ttk.Label(ClimVars_Frame, width=15, text = 'Spring PAS (mm)').grid(column = 0, row = 2, padx = 5, pady = 5)
PAS_sp_entry = ttk.Entry(ClimVars_Frame, width=12, textvariable=PAS_sp_in).grid(column = 1, row = 2, padx = 5, pady = 5)


NFFD_wt_in = tk.DoubleVar()
NFFD_wt_in.set(0.0)
NFFD_wt_Label = ttk.Label(ClimVars_Frame, width=12, text = 'Winter NFFD').grid(column = 2, row = 1, padx = 5, pady = 5)
NFFD_wt_entry = ttk.Entry(ClimVars_Frame, width=12, textvariable=NFFD_wt_in).grid(column = 3, row = 1, padx = 5, pady = 5)

NFFD_sp_in = tk.DoubleVar()
NFFD_sp_in.set(0.0)
NFFD_sp_Label = ttk.Label(ClimVars_Frame, width=12, text = 'Spring NFFD').grid(column = 2, row = 2, padx = 5, pady = 5)
NFFD_sp_entry = ttk.Entry(ClimVars_Frame, width=12, textvariable=NFFD_sp_in).grid(column = 3, row = 2, padx = 5, pady = 5)

BFFP = tk.DoubleVar()
BFFP.set(0.0)
BFFP_sp_Label = ttk.Label(ClimVars_Frame, width=12, text = 'DOY of BFFP').grid(column = 4, row = 1, padx = 5, pady = 5)
BFFP_sp_entry = ttk.Entry(ClimVars_Frame, width=12, textvariable=BFFP).grid(column = 5, row = 1, padx = 5, pady = 5)

runner_Manual = ttk.Button(ClimVars_Frame, text = "Calculate", command = click_runner_ManualEntry)
runner_Manual.grid(column = 5, row = 2, padx = 5, pady = 5)

#Frame For Output Display
Output_Frame = ttk.LabelFrame(win,text = 'Output')
Output_Frame.grid(column = 1, row = 0, padx = 5, pady = 5, sticky= tk.W)

#Field for Output Display
nffd_sp_Label = ttk.Label(Output_Frame, text = 'Estimated DOY: ').grid(column = 0, row = 0, padx = 5, pady = 5)
output_cell = tk.StringVar()
output_Entry = ttk.Entry(Output_Frame, width=28, textvariable = output_cell).grid(column = 1, row = 0, padx = 5, pady = 5)

MAE_sp_Label = ttk.Label(Output_Frame, text = 'Expected Mean Absolute Error: ').grid(column = 0, row = 1, padx = 5, pady = 5)
MAE_cell = tk.StringVar()
MAE_Entry = ttk.Entry(Output_Frame, width=28, textvariable = MAE_cell).grid(column = 1, row = 1, padx = 5, pady = 5)



#Frame For input Data
File_Frame = ttk.LabelFrame(win, text = "Climate Variables: Multiple Records")
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
outputType = tk.IntVar()
typeChecker = tk.Checkbutton(File_Frame, text="Retain All Input Data", variable=outputType)
typeChecker.deselect()
typeChecker.grid(column=0, row=2,  padx = 5, pady = 5, sticky=tk.W)



#quitter_Frame = ttk.LabelFrame(win,)
#quitter_Frame.grid(column = 0, row = 4, padx = 5, pady = 5, sticky= tk.W)

#quitter = ttk.Button(quitter_Frame,text='Quit',command=win.destroy).grid(column=0, row = 4,sticky=tk.W,pady=4)

#========
#Start GUI
#========

win.mainloop()
