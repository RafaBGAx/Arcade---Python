import cx_Freeze

executables = [cx_Freeze.Executable('pacman.py')]

cx_Freeze.setup(
    name="Pac-Quest",
    options={'build_exe': {'packages':['pygame'],
                           'include_files':[]}},

    executables = executables
    
)
