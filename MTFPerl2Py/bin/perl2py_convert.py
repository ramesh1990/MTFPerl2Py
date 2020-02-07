import pickle
import json
import sys
root_dir = "C:\PycharmProjects\MTFPerl2PyMigration\MTFPerl2Py-AutoConversion\\"
sys.path.append(root_dir)
from auto_convert.parser.parser import Parser
from auto_convert.convertor.convertor import Convertor

data_dir =  root_dir +  "data\\"
input_file = data_dir +  "input_file\\" + "scn_files_to_convert"
conf_fir = root_dir + "conf\\"
config_file = conf_fir + "config.json"

config = json.load(open(config_file, 'r'))
pscn_dir = config["pscn_dir"] + "\\"
pyscn_dir = config["pyscn_dir"] + "\\"

def get_files_list():
    file_list = []
    with open(input_file, 'r') as fp:
        for line in fp.readlines():
            file_list.append(line.strip())
    return file_list

def create_py_scn(file, py_text_objs):
    with open(pyscn_dir + file + ".scn", 'w') as fp:
        for py_text in py_text_objs:
            fp.write(py_text.line)

def create_pseudo_scn(file, perl_text_objs, py_text_objs):
    tag_pl = "*"*10 + " perl " + "*"*10
    tag_py = "*"*10 + " py " + "*"*10
    with open(pscn_dir + file + ".pscn", 'w') as fp:
        for idx in range(0, len(perl_text_objs)):
            fp.write(tag_pl)
            fp.write(perl_text_objs[idx].line)
            fp.write(tag_py)
            fp.write(py_text_objs[idx].line)

if __name__ == "__main__":
    file_list = get_files_list()
    parser = Parser()
    convertor = Convertor()
    for file in file_list:
        file_name = file.split("\\")[-1].strip(".scn")
        perl_text_objs = parser.prepare_perl_txt_obj(file)
        py_text_objs = convertor.py_convert(perl_text_objs)
        create_pseudo_scn(file_name, perl_text_objs, py_text_objs)

