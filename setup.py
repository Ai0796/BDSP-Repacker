from cx_Freeze import setup, Executable

setup(
        name = "Showdown Import BDSP",
        version = "1.0",
        description = "Unpacks and Repacks in for Unity monobehavior jsons",
        executables = [Executable("Unpack.py"), Executable("Repack.py")])