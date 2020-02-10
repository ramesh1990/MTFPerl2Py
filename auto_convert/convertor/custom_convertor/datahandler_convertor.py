from generic_convertor.generic_convertor import *

class Startping_Convertor(Generic_Convertor):
    def construct_py_params(self, perl_params, perl2py_params, perl_obj):
        print (" Ramesh => ",perl_params, perl2py_params, perl_obj,perl_obj.params)
        comment = None
        retV = super(Startping_Convertor, self).construct_py_params(perl_params, perl2py_params, perl_obj)
        py_params = retV["py_params"]
        py_params['direction'] = "'ul'"
        comment = "server name which defined in json file"
        py_vars = {"py_params": py_params, "comment": comment}
        return py_vars

class Endping_Convertor(Generic_Convertor) :
    def construct_py_params(self, perl_params, perl2py_params, perl_obj):
        comment = None
        retV = super(Endping_Convertor, self).construct_py_params(perl_params, perl2py_params, perl_obj)
        return retV

class Makedatacall_Convertor(Generic_Convertor):
    def construct_py_params(self, perl_params, perl2py_params, perl_obj):
        comment = None
        retV = super(Makedatacall_Convertor, self).construct_py_params(perl_params, perl2py_params, perl_obj)
        #return retV
        if perl_obj.params["Call Type"] == "'embedded'":
            self.py_kw = "MakeEmbeddedDataCall"
        elif perl_obj.params["Call Type"] == "'rmnet'":
            self.py_kw = "makermnetcall"
        elif perl_obj.params["Call Type"] == "'dun'":
            self.py_kw = "startdundatacall"
            comment = "dun_conn_name parameter need to provide"


