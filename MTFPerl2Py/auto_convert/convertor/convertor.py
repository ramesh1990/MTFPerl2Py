import pandas as pd
from custom_convertor.dummy_convertor import *

kw_map_df = pd.read_csv("C:\PycharmProjects\MTFPerl2PyMigration\MTFPerl2Py-AutoConversion\data\output_file\perl2py_parameter_mapping.csv")
kw_map_df["Param.Config"] = kw_map_df["Param.Config"].apply(lambda x: eval(x))

converter_handles = {'nonkw_convertor':NonKW_Convertor()}

def get_handle(class_name):
    if class_name not in converter_handles:
        converter_handles[class_name] = eval(class_name.title())()
    return converter_handles[class_name]

class Convertor:

    def __init__(self):
        self.py_objs = []

    def py_convert(self, perl_objs):
        self.py_objs = []
        for obj in perl_objs:
            if obj.kw is None:
                convertor = get_handle('nonkw_convertor')
                py_obj = convertor.py_convert(obj)
            else:
                perl_kw = obj.kw.lower()
                items = kw_map_df.loc[kw_map_df["Perl.Keyword"] == perl_kw, ["Py.Keyword","Param.Config"]].values
                py_kw = items[0][0]
                config = items[0][1]
                convertor_class = config['class']
                convertor = get_handle(convertor_class)
                kwargs = {'perl_kw':obj.kw, 'py_kw':py_kw, 'config':config}
                convertor.set_vars(**kwargs)
                py_obj = convertor.py_convert(obj)
            self.py_objs.append(py_obj)
        return self.py_objs

