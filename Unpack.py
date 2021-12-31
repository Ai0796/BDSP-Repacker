import multiprocessing as mp
from multiprocessing import process

import os, UnityPy, glob, traceback, time
import queue
import rapidjson

from PIL import Image

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