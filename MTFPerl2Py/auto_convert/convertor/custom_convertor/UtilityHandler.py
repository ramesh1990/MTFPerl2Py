from generic_convertor.generic_convertor import *

class Msleep_Convertor(Generic_Convertor):

    def construct_py_params(self, perl_params, perl2py_params, perl_obj):
        comment = None
        if isinstance(perl_obj.params, list):
            py_params = {"time":perl_obj.params[0]}
        py_vars = {"py_params":py_params, "comment":comment}
        return py_vars