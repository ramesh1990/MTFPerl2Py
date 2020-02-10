import re
from text_container.py_text import Py_Text

perl_var_literal = re.compile('\$:+\s*')
is_cmnt = re.compile('^\s*#+')
if_clause = re.compile('^\s*if(.*);', flags=re.DOTALL|re.I)
perl_var_decl = re.compile("^\s*(EXPR)")
digit_pattern = re.compile("\d+")
undef_pattern = re.compile("undef")
service_type_pattern = re.compile("full|limited|oos")

class Generic_Convertor(object):

    def __init__(self):
        pass

    def set_vars(self, **kwargs):
        self.perl_kw = kwargs['perl_kw']
        self.py_kw = kwargs['py_kw']
        self.config = kwargs['config']

    def get_map_vars(self):
        return self.config["perl_params"],self.config["perl2py_params"]

    def construct_subid_param(self, perl_obj):
        if perl_obj.post_fix in [None, '0']:
            return {"subs_id":0}
        else:
            return {"subs_id":1}

    def construct_py_params(self, perl_params, perl2py_params, perl_obj):
        comment = None
        if perl_obj.params == '':
            py_params = ''
        elif isinstance(perl_obj.params, list):
            py_params = {}
            # print(perl_obj.params)
            for idx,val in enumerate(perl_obj.params):
                perl_key = perl_params[idx]
                py_key = perl2py_params[perl_key]
                py_params[py_key] = perl_var_literal.sub(repl='', string=val)
        elif isinstance(perl_obj.params, dict):
            # print(perl_obj.params)
            py_params = {}
            for key, val in perl_obj.params.items():
                py_key = perl2py_params[key]
                py_params[py_key] = perl_var_literal.sub(repl='', string=val)

        py_vars = {"py_params":py_params, "comment":comment}
        return py_vars

    def prepare_py_params(self, perl_obj):
        perl_params, perl2py_params = self.get_map_vars()
        self.construct_py_params(perl_params, perl2py_params, perl_obj)

    def py_convert(self, perl_obj):
        py_params = self.prepare_py_params(perl_obj)
        self.construct_py_text(perl_obj, py_params)

    def construct_py_text(self, perl_obj, py_vars):
        py_params = py_vars["py_params"]
        # print(perl_obj.kw, perl_obj.param_string)
        perl_ptrn = re.compile("{}\s*\(\s*{}\s*\)".format(perl_obj.kw, re.escape(perl_obj.param_string)), flags=re.I)
        # print(perl_obj.line)
        if isinstance(py_params, dict):
            py_text = "{" + ", ".join([key + ':' + val for key,val in py_params.items()]) + "}"

        else:
            py_text = py_params
        py_line = perl_ptrn.sub(repl="{}({})".format(self.py_kw, py_text), string=perl_obj.line) +  " #" + py_vars["comment"] if py_vars["comment"] else ''
        obj = Py_Text(py_line)
        obj.set_kw(self.py_kw)
        obj.set_param_string(py_text)
        obj.set_params(py_params)
        return obj
        # print(py_line)

class NonKW_Convertor(object):

      def __init__(self):
          pass

      def py_convert(self, perl_obj):
          if is_cmnt.search(perl_obj.line):
              return Py_Text(perl_obj.line)
          else:
              py_line = self.variable_decl_convert(perl_obj.line)
              py_line = self.variable_convert(py_line)
              py_line = self.if_clause_convert(py_line)
              return Py_Text(py_line)

      def variable_convert(self, line):
          return perl_var_literal.sub(repl='', string=line) # variable replacement

      def if_clause_convert(self, line):
          match = if_clause.search(line)
          if match:
              cnd = match.group(1)
              if not re.search("^\(",cnd) :
                  cnd = '('+ cnd + ')'
                  line = line.replace(match.group(1), cnd)
          return line

      def variable_decl_convert(self, line):
          match = perl_var_decl.search(line)
          if match:
              line = perl_var_decl.sub(repl='default', string=line)
              return self.variable_convert(line)
