import os

class Types():
    
    TYPEFILE = "types.txt"
    DEFAULTTYPES = [
        "MonoBehaviour",
        "AssetBundleManifest",
        "GameObject",
        "BoxCollider",
        "Transform",
        "ParticleSystem",
        "AssetBundle",
        "AnimationClip"
    ]
    
    def __init__(self) -> None:
        self.typeNames = self.DEFAULTTYPES
    
    def readTypes(self) -> None:
        self.typeNames = []
        if os.path.exists(self.TYPEFILE):
            f = open(self.TYPEFILE, "r")
            lines = f.readlines()

            for line in lines:
                line = line.strip()
                if line.startswith("#") or len(line) == 0:
                    continue
                else:
                    print("Read Type:", line)
                    self.typeNames.append(line)

            if len(self.typeNames) == 0:
                self.typeNames = self.DEFAULTTYPES
        else:
            print("Type.txt not found, using default values")
                
    def getTypeNames(self):
        return self.typeNames
                
                
if __name__ == "__main__":
    type = Types()
    print(type.getTypeNames())