from cx_Freeze import setup, Executable

base = None    

executables = [Executable("eds_analysis_windows.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "EDS Windows",
    options = options,
    version = "<any number>",
    description = '<any description>',
    executables = executables
)