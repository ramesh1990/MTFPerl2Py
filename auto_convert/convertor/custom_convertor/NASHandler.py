from generic_convertor.generic_convertor import *

class Checkmodepref_Convertor(Generic_Convertor):

    def construct_py_params(self, perl_params, perl2py_params, perl_obj):
        comment = None
        if isinstance(perl_obj.params, list):
            py_params = {"systems": perl_obj.params}
            py_params.update(self.construct_subid_param(perl_obj))
        elif isinstance(perl_obj, dict):
            py_params = super().construct_py_params(perl_params, perl2py_params, perl_obj)

        py_vars = {"py_params": py_params, "comment": comment}
        return py_vars

class Switchdataprofile_Convertor(Generic_Convertor):

    def construct_py_params(self, perl_params, perl2py_params, perl_obj):
        comment = None
        if isinstance(perl_obj.params, list):
            if "sub1" in perl_obj.params[0]:
                py_params = {"subs_id": 0}
            else:
                py_params = {"subs_id": 1}

        py_vars = {"py_params":py_params, "comment":comment}
        return py_vars

class Waitforsystem_Convertor(Generic_Convertor):

    def construct_py_params(self, perl_params, perl2py_params, perl_obj):
        comment = None
        if isinstance(perl_obj.params, list):
            py_params = {}
            tech = []
            for val in perl_obj.params:
                if digit_pattern.search(val):
                    py_params["timeout"] = val
                elif service_type_pattern.search(val):
                    py_params["service_type"] = val
                else:
                    tech.append(digit_pattern.sub(repl="", string=val).lower())
            if tech:
                py_params["systems"] = "&".join(tech)
            else:
                comment = 'systems is mandatory input, please provide it in scenario'
        elif isinstance(perl_obj.params, dict):
            py_params = super().construct_py_params(perl_params, perl2py_params, perl_obj)
            if not py_params.get("systems"):
                comment = 'systems is mandatory input, please provide it in scenario'

        py_params.update(self.construct_subid_param(perl_obj))
        py_vars = {"py_params":py_params, "comment":comment}

        return py_vars