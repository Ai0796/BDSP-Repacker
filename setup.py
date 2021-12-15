from cx_Freeze import setup, Executable

build_exe_options = {"excludes": ["tkinter", "PyQt4.QtSql", "sqlite3", 
                                  "scipy.lib.lapack.flapack",
                                  "PyQt4.QtNetwork",
                                  "PyQt4.QtScript",
                                  "numpy.core._dotblas", 
                                  "PyQt5"],
                     "optimize": 2}

setup(
        name = "Showdown Import BDSP",
        version = "1.0",
        description = "Unpacks and Repacks in for Unity monobehavior jsons",
        executables = [Executable("Unpack.py"), Executable("Repack.py")])