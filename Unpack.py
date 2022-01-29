import multiprocessing as mp
from multiprocessing import process

import os, UnityPy, glob, traceback, time, shutil
import queue
import rapidjson
import tqdm

from PIL import Image

exportNames = [
    "MonoBehaviour",
    # "AssetBundleManifest",
    "BoxCollider",
    "Transform"
    # "AssetBundle"
]

def unpackassets(queue, src):
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
        for i in range(len(env.objects)):
            obj = env.objects[i]
            if obj.type.name in exportNames:
                # export
                if obj.serialized_type.nodes:
                    
                    # save decoded data
                    tree = obj.read_typetree()
                    data = obj.read()
                    
                    if "m_Name" in list(tree.keys()):
                        name = tree["m_Name"]
                    else:
                        name = ""
                        
                    if name == "":
                        
                        if obj.type.name == "MonoBehaviour":
                            script_path_id = tree["m_Script"]["m_PathID"]
                            
                        elif obj.type.name == "Transform" or obj.type.name == "BoxCollider":
                            script_path_id = tree["m_GameObject"]["m_PathID"]
                            
                        for script in env.objects:
                            if script.path_id == script_path_id:
                                name = script.read().name
                                
                    name = os.path.basename(name)
                                
                    pathDic[str(obj.path_id)] = name
                    fp = os.path.join(extract_dir, f"{name}.json")
                    
                    ##Creates new file names for duplicates
                    j = 0
                    while os.path.exists(fp):
                        j += 1
                        fp = os.path.join(extract_dir, f"{name}_{obj.path_id}.json")
                        
                    if j > 0: 
                        pathDic[str(obj.path_id)] = f"{name}_{obj.path_id}"
                        
                    else:
                        pathDic[str(obj.path_id)] = name
                        
                    ##Finish Dumping the file
                    with open(fp, "wb") as f:
                        rapidjson.dump(tree, f, ensure_ascii = False, indent = 4)
                        # f.write(orjson.dumps(tree, option=orjson.OPT_INDENT_2))
                        f.close()
                else:
                    # save raw relevant data (without Unity MonoBehaviour header)
                    data = obj.read()
                    fp = os.path.join(extract_dir, f"{data.name}.bin")
                    with open(fp, "wb") as f:
                        f.write(data.raw_data)
                     
        filename = os.path.basename(src)   
        fp = os.path.join(path_dir, f"{filename}_pathIDs.json")
        with open(fp, "wt") as f:
            rapidjson.dump(pathDic, f, ensure_ascii = False, indent = 4)
            f.close()
        queue.put(f"{src} unpacked successfully")
        return
    
    except:
        
        print(traceback.format_exc())
        queue.put(f"{src} failed to unpack")
        return
    
def main():
    start_time = time.time()
    path = "AssetFolder"

    if not os.path.exists(path):
        os.makedirs(path, 0o666)
        print("Created folder 'AssetFolder' put Unity Assets e.g. masterdatas, ev_scripts in folder")
        input("Once all files are in, press enter to continue...")

    q = mp.Queue()
    processes = []
    i = 0
    for filepath in glob.iglob(path + "**/**", recursive=False):
        if os.path.isfile(filepath):
            i += 1
            extract_dir = str(filepath) + "_Export"
            
            ##This needs to be here b/c it'll break if done on a process
            if os.path.exists(extract_dir):
                input(f"Warning: {extract_dir} already exists, if this is intentional, press enter...")
                shutil.rmtree(extract_dir)
                
            print(f"Unpacking {filepath}")
            p = mp.Process(target=unpackassets, args=(q,filepath))
            p.start()
            processes.append(p)

    for process in processes:
        print(q.get())
        p.join()
            
    print("Finished Unpacking "f"{i} Files")
    print("Unpacking took", time.time() - start_time, "seconds to run")
    input("Press Enter to Exit...")

if __name__ == "__main__":
    mp.freeze_support()
    main()