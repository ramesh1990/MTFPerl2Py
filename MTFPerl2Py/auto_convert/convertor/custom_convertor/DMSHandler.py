from generic_convertor.generic_convertor import *

class Waitforpmoperatingmode_Convertor(Generic_Convertor):

    def construct_py_params(self, perl_params, perl2py_params, perl_obj):
        comment = None
        if isinstance(perl_obj.params, list):
            py_params = {}
            tech = []
            if len(perl_obj.params) > 2:
                perl_key = perl_params[2]
                py_params[perl2py_params[perl_key]] = tech
            for idx, val in enumerate(perl_obj.params):
                if idx < 2:
                    if not 'undef' in val:
                        perl_key = perl_params[idx]
                        py_params[perl_key] = val
                else:
                    if digit_pattern.search(val):
                        py_params["timeout"] = val
                    else:
                        tech.append(val)
        elif isinstance(perl_obj.params, dict):
            py_params = super().construct_py_params(perl_params, perl2py_params, perl_obj)

        py_params.update(self.construct_subid_param(perl_obj))

        py_vars = {"py_params":py_params, "comment":comment}
        return py_vars

