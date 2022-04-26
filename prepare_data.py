import json
import glob

def get_anns():
    path = '/media/idt/c9fed8d0-a409-4fac-b88e-61892dc0e35b/NWPU-Crowd/jsons/*.json'
    anns = {}

    def get_annP(p):
        with open(p,'r') as f:
            ann_data = json.load(f)
        return ann_data['human_num']

    for name in glob.glob(path):
        count = get_annP(name)
        file = name.replace('/media/idt/c9fed8d0-a409-4fac-b88e-61892dc0e35b/NWPU-Crowd/jsons/','').replace('.json','')
        if count <= 200:
            anns[file] = count
    return anns