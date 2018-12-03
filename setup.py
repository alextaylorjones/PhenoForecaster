from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])
#

build_exe_options = {"packages": ["os","pandas","Tkinter","numpy"],"excludes": ["notebook","PyQt4.QtNetwork","PyQt4.QtScript","sqlite3","PyQt4.QtSql","IPython", "matplotlibwidget","matplotlib","socketserver","curses"],
"include_files": "PhenoForecaster_Ancillary_Files/,LICENSE-BSD.txt,LICENSE-cx.txt","optimize":0 }

#build_exe_options = {"excludes": ["notebook","PyQt4.QtNetwork","PyQt4.QtScript","sqlite3","PyQt4.QtSql","mpl"],"include_files": "PhenoPredict_Ancillary_Files/,LICENSE-BSD.txt,LICENSE-cx.txt","optimize":2}


base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('PhenoForecaster.py', base=base)
]

setup(name='PhenoForecaster',
      version = '1.0',
      description = '',
      options = dict(build_exe = build_exe_options),
      executables = executables)
