import multiprocessing as mp
import os, UnityPy, glob, traceback, time, shutil
import rapidjson

from Types import Types

import asyncio


async def dumpJson(tree, fp):
    with open(fp, "wb") as f:
        rapidjson.dump(tree, f, ensure_ascii=False, indent=4)
        # f.write(orjson.dumps(tree, option=orjson.OPT_INDENT_2))
        f.close()
        
async def dumpImg(image, fp):
    image.save(fp)

async def unpackassets(queue, src, exportNames):
    ##Creates a new folder named {src}_Export
    ##Puts files from source in folder
    extract_dir = str(src) + "_Export"
    path_dir = "pathIDs"
    existingFPs = []
    q = []
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir, 0o666)
        
    if not os.path.exists(path_dir):
        os.makedirs(path_dir, 0o666)
    try:
        env = UnityPy.load(src)

        pathDic = {}
        for obj in env.objects:

            if obj.type.name in exportNames:
                
                # save decoded data
                tree = obj.read_typetree()
                
                if "m_Name" in tree:
                    name = tree["m_Name"]
                else:
                    name = ""

                ##Grab a name from script or gameobject name
                if name == "":

                    if obj.type.name == "AssetBundle":
                        name = "AssetBundle"
                        script_path_id = 0

                    elif obj.type.name == "MonoBehaviour":
                        script_path_id = tree["m_Script"]["m_PathID"]

                    elif obj.type.name in ["Transform", "BoxCollider", "ParticleSystem", "MeshRenderer", "MeshFilter", "SkinnedMeshRenderer"]:
                        script_path_id = tree["m_GameObject"]["m_PathID"]

                    else:
                        print("Error, Type:", obj.type.name, "name not recognized")
                        continue

                    for script in env.objects:
                        if script.path_id == script_path_id:
                            name = script.read().name
                            
                name = os.path.basename(name)
                            
                # fp = os.path.join(extract_dir, f"{name}.json")
                if obj.type.name in ["Texture2D", 'Sprite']:
                    fp = os.path.join(extract_dir, f"{name}.png")
                    
                    if fp.upper() in existingFPs:
                        fp = os.path.join(extract_dir, f"{name}_{obj.path_id}.png")
                        pathDic[str(obj.path_id)] = f"{name}_{obj.path_id}"

                    else:
                        pathDic[str(obj.path_id)] = name
                        
                    data = obj.read()
                    image = data.image
                    image = image.convert("RGBA")
                    existingFPs.append(fp.upper())
                    q.append(dumpImg(image, fp))
                        
                else:
                    fp = os.path.join(extract_dir, f"{name}.json")
                    
                    ##Creates new file names for duplicates
                    if fp.upper() in existingFPs:
                        fp = os.path.join(extract_dir, f"{name}_{obj.type.name}_{obj.path_id}.json")
                        pathDic[str(obj.path_id)] = f"{name}_{obj.type.name}_{obj.path_id}"

                    else:
                        pathDic[str(obj.path_id)] = name
                        
                    existingFPs.append(fp.upper())
                    q.append(dumpJson(tree, fp))
                        
                    ##Finish Dumping the file
                    
        await asyncio.gather(*q)     
        filename = os.path.basename(src)   
        fp = os.path.join(path_dir, f"{filename}_pathIDs.json")
        with open(fp, "wt") as f:
            rapidjson.dump(pathDic, f, ensure_ascii = False, indent = 4)
            f.close()
        queue.put(f"{src} unpacked successfully")
        return
    
    except:
        
        print(traceback.format_exc())
        print(tree)
        queue.put(f"{src} failed to unpack")
        return
    
def run(queue, src, exportNames):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(unpackassets(queue, src, exportNames))
    
async def main():
    path = "AssetFolder"
    
    type = Types()
    type.readTypes()
    exportNames = type.getTypeNames()

    if not os.path.exists(path):
        os.makedirs(path, 0o666)
        print("Created folder 'AssetFolder' put Unity Assets e.g. masterdatas, ev_scripts in folder")
        input("Once all files are in, press enter to continue...")

    q = mp.Queue()
    processes = []
    filepaths = []
    
    for filepath in glob.iglob(path + "**/**", recursive=False):
        if os.path.isfile(filepath):
            extract_dir = str(filepath) + "_Export"
            
            ##This needs to be here b/c it'll break if done on a process
            if os.path.exists(extract_dir):
                input(f"Warning: {extract_dir} already exists, if this is intentional, press enter...")
                shutil.rmtree(extract_dir)
                
            filepaths.append(filepath)    
          
    start_time = time.time()
    i = 0
    for filepath in filepaths:
        i += 1
        print(f"Unpacking {filepath}")
        p = unpackassets(q, filepath, exportNames)
        processes.append(p)
    
    await asyncio.gather(*processes)
            
    print("Finished Unpacking "f"{i} Files")
    print("Unpacking took", time.time() - start_time, "seconds to run")
    input("Press Enter to Exit...")

if __name__ == "__main__":
    
    mp.freeze_support()
    asyncio.run(main())