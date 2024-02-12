import cx_Freeze

executables = [cx_Freeze.Executable('Arcade.py')]

cx_Freeze.setup(
    name="Jogos Arcade",
    options={'build_exe': {'packages':['pygame'],
                           'include_files':[]}},

    executables = executables
    
)
