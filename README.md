# PhenoForecaster

PhenoForecaster is the first standalone package to make phenological modelling directly accessible to users without the need for in depth phenological observations.

## How to Use

Using Windows installer: 
* Installation: 
* Download the MSI installer ````PhenoForecaster-1.0-amd64.msi````.
* Calculate SHA512 hash using ```certUtil -hashfile PhenoPredict\PhenoForecaster-amd64.msi SHA512``` and match to 
```` ee473f7e44522b8e8285b946204fd1fac7de89278993bd1dfdcd866f38e2ea40b3fb45b97c40bd499cdd889bb05aa69c202d860462e52f1580e83022b7e4eaf2 ````
* Run installer.
* Run PhenoForecaster.exe in target folder.

* [cx Freeze](https://anthony-tuininga.github.io/cx_Freeze/). Source code is included as PhenoForecaster.py. Note: numpy, pandas, Tkinter must be installed for this to work. Current installation using Python 2.7.x.
