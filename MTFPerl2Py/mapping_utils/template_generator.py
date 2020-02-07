import os
import pandas as pd
import csv

rel_path = "C:/PycharmProjects/MTFPerl2PyMigration/MTFPerl2Py-AutoConversion" + "/"
data_path = rel_path + "data" +"/"
kw_file = data_path +  "input_file" + "/" + "team_keywords"
perl2py_map_file = data_path + "static" + "/" + "perl2pykw.csv"
template_path = data_path + "template" + "/"

map_df = pd.read_csv(perl2py_map_file)
map_df.fillna('', inplace=True)

kws_to_process = []
handler_dir = {}

header1 = ["Perl.Keyword", "Py.Keyword", "Convertor"]
header2 = ["Perl.Params","Perl2Py.ParamMap","Py.Params"]

def find_kws_to_process():
    with open(kw_file, 'r') as fp:
        for line in fp.readlines():
            kws_to_process.append(line.strip(" |\n|\r|\t"))

def create_handler_dir():
    handlers = map_df.loc[map_df["Perl.Keyword"].isin(kws_to_process), "Perl.Handler"].unique()
    for handler in handlers:
        dir_path = template_path + handler.strip(".py")
        os.makedirs(dir_path, exist_ok=True)
        handler_dir[handler] = dir_path

def create_template():
    for kw in kws_to_process:
        csv_data = []
        items = map_df.loc[map_df["Perl.Keyword"] == kw, ["Perl.Handler","Py.Keyword","Perl.Params", "Py.Params"]].values
        hdlr = items[0][0]
        py_kw = items[0][1]
        perl_params = str(items[0][2]).strip('(|)').split(':')
        py_params = str(items[0][3]).strip('(|)').split(':')
        csv_data.append(header1)
        csv_data.append([kw, py_kw, 'generic_convertor'])
        csv_data.append(['','',''])
        csv_data.append(header2)

        for idx in range(0, max([len(perl_params), len(py_params)])):
            try:
                perl_param = perl_params[idx]
            except:
                perl_param = ''

            try:
                py_param = py_params[idx]
            except:
                py_param = ''
            csv_data.append([perl_param, '', py_param])
        to_csv(handler_dir[hdlr] + "/" + kw, csv_data)

def to_csv(file_name, data_lines):
    with open(file_name + ".csv", 'w', newline='') as fp:
        writer = csv.writer(fp, delimiter=',')
        writer.writerows(data_lines)


if __name__ == "__main__":
    find_kws_to_process()
    create_handler_dir()
    create_template()