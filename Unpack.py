import os, UnityPy, glob, traceback, time
import rapidjson

from PIL import Image

def unpackassets(src):
    ##Creates a new folder named {src}_Export
    ##Puts files from source in folder
    extract_dir = str(src) + "_Export"
    path_dir = "pathIDs"
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir, 0o666)
        
    if not os.path.exists(path_dir):
        os.makedirs(path_dir, 0o666)
    try:
        env = UnityPy.load(src)
        
        pathDic = {}
        for obj in env.objects:
            if obj.type.name == "MonoBehaviour":
                # export
                if obj.serialized_type.nodes:
                    
                    # save decoded data
                    tree = obj.read_typetree()
                    # data = obj.read()
                    
                    name = tree["m_Name"]
                    if name == "":
                        script_path_id = tree["m_Script"]["m_PathID"]
                        for script in env.objects:
                            if script.path_id == script_path_id:
                                name = script.read().name
                                
                    pathDic[str(obj.path_id)] = name
                    fp = os.path.join(extract_dir, f"{name}.json")
                    with open(fp, "wt", encoding = "utf8") as f:
                        rapidjson.dump(tree, f, ensure_ascii = False, indent = 4)
                else:
                    # save raw relevant data (without Unity MonoBehaviour header)
                    data = obj.read()
                    fp = os.path.join(extract_dir, f"{data.name}.bin")
                    with open(fp, "wb") as f:
                        f.write(data.raw_data)
                        
            # elif obj.type.name == "Texture2D":
            #     # export texture
            #     tree = obj.read_typetree()
            #     data = obj.read()
                    
            #     name = data.name
            #     if name == "":
            #         script_path_id = tree["m_Script"]["m_PathID"]
            #         for script in env.objects:
            #             if script.path_id == script_path_id:
            #                 name = script.read().name
            #     fp = os.path.join(extract_dir, f"{name}.png")
            #     data.image.save(fp)
            #     # edit texture
                
            #     # pil_img = Image.open(fp)
            #     # data.image = pil_img
            #     # data.save()
                     
        filename = os.path.basename(src)   
        fp = os.path.join(path_dir, f"{filename}_pathIDs.json")
        with open(fp, "wt") as f:
            rapidjson.dump(pathDic, f, ensure_ascii = False, indent = 4)
        return(f"{src} unpacked successfully")
    
    except:
        
        print(traceback.format_exc())
        return(f"{src} failed to unpack")
    
    
if __name__ == "__main__":
    start_time = time.time()
    path = "AssetFolder"

    if not os.path.exists(path):
        os.makedirs(path, 0o666)
        print("Created folder 'AssetFolder' put Unity Assets e.g. masterdatas, ev_scripts in folder")
        input("Once all files are in, press enter to continue...")

    i = 0
    for filepath in glob.iglob(path + "**/**", recursive=False):
        if os.path.isfile(filepath):
            print(unpackassets(filepath))
            i += 1
            
            
    print("Finished Unpacking "f"{i} Files")
    print("Unpacking took", time.time() - start_time, "seconds to run")
    input("Press Enter to Exit...")