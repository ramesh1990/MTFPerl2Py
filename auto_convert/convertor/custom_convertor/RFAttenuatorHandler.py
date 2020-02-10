from generic_convertor.generic_convertor import *

class Turnonselectports_Convertor(Generic_Convertor):

    def construct_py_params(self, perl_params, perl2py_params, perl_obj):
        comment = "Verify these port aliases are defined in the py config file"
        if isinstance(perl_obj.params, list):
            py_params = {'ports':perl_obj.params}
        py_vars = {"py_params":py_params, "comment":comment}
        return py_vars