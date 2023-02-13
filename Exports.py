import os


class Exports():

    EXPORTFILE = "exports.txt"
    DEFAULTEXPORTS = [
        "TrainerTable",
        "FieldEncountTable_d",
        "DistributionTable",
        "AddPersonalTable",
        "EvolveTable",
        "GrowTable",
        "ItemTable",
        "PedestalTable",
        "PersonalTable",
        "SealTable",
        "StoneStatuEeffect",
        "TamagoWazaTable",
        "TamaTable",
        "UgFatherExpansion",
        "UgFatherExpansion",
        "UgFatherShopTable",
        "UgItemTable",
        "WazaOboeTable",
        "WazaTable"
    ]

    def __init__(self) -> None:
        self.exportNames = self.DEFAULTEXPORTS
        self.exportNames = [i.lower() for i in self.exportNames]

    def readExports(self) -> None:
        self.exportNames = []
        if os.path.exists(self.EXPORTFILE):
            f = open(self.EXPORTFILE, "r")
            lines = f.readlines()

            for line in lines:
                line = line.strip()
                if line.startswith("#") or len(line) == 0:
                    continue
                else:
                    print("Read Name:", line)
                    self.exportNames.append(line)

            if len(self.exportNames) == 0:
                self.exportNames = self.DEFAULTTYPES
        else:
            print("exports.txt not found, using default values")
            
        self.exportNames = [i.lower() for i in self.exportNames]

    def getExportNames(self):
        return self.exportNames


if __name__ == "__main__":
    export = Exports()
    print(export.getExportNames())
