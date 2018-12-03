# PhenoForecaster

PhenoForecaster is the first standalone package to make phenological modelling directly accessible to users without the need for in depth phenological observations.

## How to Use

Using Windows installer: 
* Installation: 
* Download the MSI installer ````PhenoForecaster-1.0-amd64.msi````.
* Calculate SHA512 hash of installer (e.g. ```certUtil -hashfile PhenoPredict\PhenoForecaster-amd64.msi SHA512``` ) and verify that it is 
```` f435a69991c4a42f03368f4e1202893c5f85ad3b8d8288180406037f440b1c3f5c83dbe56e1cd68d2f17f9c8ddd9a28932ec7d400cc431dba9233acd9ddda2ee ````
* Run installer.
* Run PhenoForecaster.exe in target folder.

* [cx Freeze](https://anthony-tuininga.github.io/cx_Freeze/). Source code is included as PhenoForecaster.py. Note: numpy, pandas, Tkinter must be installed for this to work. Current installation using Python 2.7.x.
