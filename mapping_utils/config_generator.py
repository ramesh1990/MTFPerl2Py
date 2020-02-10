import pandas as pd
import os
import re


user = input("Enter your name \n")
cur_path = os.getcwd()
path = cur_path + "\\" + "data_source" + "\\"
kw_map_df = pd.read_csv(path + "perl2pykw_dummy.csv")
perl_kw = []
perl_hdlr = []
py_kw = []
py_hdlr = []
perl2py_config = []
all_files = os.listdir(path)
ignore_exp = re.compile("\s*\(\s*(optional|mandatory)\s*\)\s*|", flags=re.I)

for file in all_files:
    perl_params = []
    perl2py_params = {}
    config = {'class': 'generic_convertor', 'perl_params': perl_params, 'perl2py_params': perl2py_params}
    if file.endswith(".txt"):
        kw_name = file.split(".txt")[0]
        with open(path + file, 'r') as fp:
            for line in fp.readlines():
                if ':' in line:
                    param = "{}".format(ignore_exp.sub(repl="", string=line.split(":")[0]).strip())
                else:
                    param = "{}".format(ignore_exp.sub(repl="", string=line.split("-")[0]).strip())
                perl_params.append(param)
                perl2py_params[param] = param
        perl_kw.append(kw_name)
        perl2py_config.append(config)
        kw_index = kw_map_df["Perl.Keyword"]==kw_name
        values = kw_map_df.loc[kw_index, ["Py.Keyword","Perl.Handler","Py.Handler"]].values
        py_kw.append(values[0][0])
        perl_hdlr.append(values[0][1])
        py_hdlr.append(values[0][2])

df = pd.DataFrame({"Owner":user, "Perl.Keyword":perl_kw,"Perl.Handler":perl_hdlr, "Py.Keyword":py_kw,"Py.Handler":py_hdlr, "Param.Config":perl2py_config})
df.to_csv(path + "perl2py_parameter_mapping.csv", index=False)