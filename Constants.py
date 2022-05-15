from rapidjson import loads, dumps
from os import path

class Constants:
    
    configFile = "types.json"
    exportNames = [
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
        if(path.exists(self.configFile)):
            with open(self.configFile) as f:
                file = loads(f.read())
                self.exportNames = file
        else:
            with open(self.configFile, "w") as f:
                f.write(dumps(self.exportNames, indent = 4))