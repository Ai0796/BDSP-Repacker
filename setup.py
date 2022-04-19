from cx_Freeze import setup, Executable

build_exe_options = {"excludes": ["tkinter", "PyQt4.QtSql", "sqlite3", 
                                  "scipy.lib.lapack.flapack",
                                  "PyQt4.QtNetwork",
                                  "PyQt4.QtScript",
                                  "numpy.core._dotblas", 
                                  "PyQt5", "numpy", "matplotlib", "scipy"],
                     "optimize": 2}

setup(
        name = "Unity-Repacker",
        version = "1.0",
        options = {"build_exe": build_exe_options},
        description = "Unpacks and Repacks in for Unity monobehavior jsons",
        executables = [Executable("Unpack.py"), Executable("Repack.py")])