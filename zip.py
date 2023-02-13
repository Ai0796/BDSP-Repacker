
import rapidjson
import zipfile
import os

zipArchive = zipfile.ZipFile("output.zip", "w")

async def make_archive(fp, data):
    # Less annoying make archive with workaround classes
    jsondata = rapidjson.dumps(data, ensure_ascii = False, indent = 4)
    zipArchive.writestr(fp, jsondata)

def close_archive():
    zipArchive.close()