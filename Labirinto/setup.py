import cx_Freeze

executables = [cx_Freeze.Executable('ProjetoLabirinto.py')]

cx_Freeze.setup(
    name="Labirinto",
    options={'build_exe': {'packages':['pygame'],
                           'include_files':[]}},

    executables = executables
    
)
