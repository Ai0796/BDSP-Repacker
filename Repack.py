
import multiprocessing as mp
import os, rapidjson, UnityPy, glob, traceback, time
from Constants import Constants
from UnityPy.enums import TextureFormat

TF = TextureFormat

from PIL import Image

constants = Constants()
exportNames = constants.exportNames

workingTypes = [
    TF.DXT1,
    TF.DXT5,
    TF.ETC_RGB4,
    TF.ETC2_RGB,
    TF.ETC2_RGBA8,
    TF.Alpha8,
    TF.R8,
    TF.RGB24,
    TF.RGBA32
]

defaultFormat = TextureFormat(12)

def repackassets(queue, src, output, fileNum):
    ##Creates a new folder named {src}_Export
    ##Puts files from source in folder
    extract_dir = str(src) + "_Export"
    path_dir = "pathIDs"
        
    filename = os.path.basename(src)   
    fp = os.path.join(path_dir, f"{filename}_pathIDs.json")
    with open(fp, "r") as f:
        pathDic = rapidjson.load(f)
        pathDicKeys = list(pathDic.keys())
    if os.path.exists(extract_dir):
        try:
            env = UnityPy.load(src)
            for obj in env.objects:
                if obj.type.name in exportNames:
                    # save decoded data
                    if str(obj.path_id) in pathDicKeys:
                        
                        name = pathDic[str(obj.path_id)]
                    
                    else:
                        
                        tree = obj.read_typetree()
                        
                        name = tree["m_Name"]
                        
                        if "m_Name" in list(tree.keys()):
                            name = tree["m_Name"]
                        else:
                            name = ""
                            
                        if name == "":
                            
                            if obj.type.name == "AssetBundle":
                                name = "AssetBundle"
                                script_path_id = 0
                            
                            elif obj.type.name == "MonoBehaviour":
                                script_path_id = tree["m_Script"]["m_PathID"]
                                
                            elif obj.type.name in ["Transform" ,"BoxCollider" ,"ParticleSystem", "MeshRenderer", "MeshFilter"]:
                                script_path_id = tree["m_GameObject"]["m_PathID"]
                                
                            for script in env.objects:
                                if script.path_id == script_path_id:
                                    name = script.read().name
                                    
                        name = os.path.basename(name)
                        
                    if obj.type.name == "Texture2D":
                        fp = os.path.join(extract_dir, f"{name}.png")
                        textureFormat = defaultFormat
                        image = Image.open(fp)
                        data = obj.read()
                        if data.m_TextureFormat in workingTypes:
                            textureFormat = data.m_TextureFormat
                        data.m_Width = image.width
                        data.m_Height = image.height
                        data.set_image(image, textureFormat)
                        data.save()
                                    
                    elif os.path.exists(name):
                        fp = os.path.join(extract_dir, f"{name}.json")
                        with open(fp, "r", encoding = "utf8") as f:
                            obj.save_typetree(rapidjson.load(f))
                            f.close()
                            
                    else:
                        print("Error, File not found:", name)
            
            fp = os.path.join(output, os.path.basename(src))
            with open(fp, "wb") as f:
                f.write(env.file.save(packer=(64,2))) 
                f.close()               
            queue.put(f"{src} repacked successfully")
            return
        
        except:
            
            print(name)
            print(traceback.format_exc())
            queue.put(f"{src} failed to repack")
            return
    else:

        print("Error: "f"{src}_Export does not exist (Have you ran Unpack.exe?)")
    

def main():
    mp.set_start_method('spawn')
    start_time = time.time()
    path = "AssetFolder"
    output = "EditedAssets"

    if not os.path.exists(path):
        os.makedirs(path, 0o666)
        print("Created folder 'AssetFolder' put Unity Assets e.g. masterdatas, ev_scripts in folder")
        input("Once all files are in, press enter to continue...")
        
    if not os.path.exists(output):
        os.makedirs(output, 0o666)

    q = mp.Queue()
    processes = []
    i = 0
    for filepath in glob.iglob(path + "**/**", recursive=False):
        if os.path.isfile(filepath):
            i += 1
            
            p = mp.Process(target=repackassets, args=(q, filepath, output, i))
            p.start()
            processes.append(p)

    for process in processes:
        print(q.get())
        process.join()
    # print(repackassets(filepath, output))
            
    print("Finished Repacking "f"{i} Files")
    print("Repacking took", time.time() - start_time, "seconds to run")
    input("Press Enter to Exit...")

if __name__ == "__main__":
    mp.freeze_support()
    main()