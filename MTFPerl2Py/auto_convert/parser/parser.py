import os
import pickle
from text_container.perl_text import Perl_Text
from convertor.convertor import *

class Parser():
    kw_pattern = re.compile(r'^\s*(\w+)\((.*)\)\s*;+', re.M|re.DOTALL|re.I)
     # kw_pattern_if = re.compile(r'^\s*if\s*\(*(\w+)\((.*)\)\s*', re.M|re.DOTALL|re.I)
     # kw_patten_in_if =
    cmnt_pattern = re.compile(r'^\s*#')
    hash_expr = "\s*{(.*)}\s*"
    check_hash_pattern = re.compile(hash_expr, flags=re.DOTALL)
    hash_key_expr= "\s*['\"]*[.|\w]*['\"]*\s*"
    hash_val_expr = "\s*['\"]*\$*:*[.|\w]*['\"]*\s*"
    hash_pattern = re.compile(hash_key_expr + "=>" + hash_val_expr)


    perl_txt_objs = []

    def __init__(self, **kwargs):
         pass

    def add_perl_txt(self, obj):
         self.perl_txt_objs.append(obj)

    def prepare_perl_txt_obj(self, scn_file):
         self.perl_txt_objs = []
         multiline_for_kw = []
         with open(scn_file, 'r') as fp:
             # print(fp.readlines())
             for line in fp.readlines():
                 if self.prepare_kw(line) or self.prepare_nonkw(line) :
                     if multiline_for_kw:
                        self.prepare_multiline_kw("".join(multiline_for_kw))
                        multiline_for_kw = []
                 else:
                     # print(line)
                     multiline_for_kw.append(line)
         return self.perl_txt_objs

    def prepare_kw(self, line):
         status = False
         kw_line_match = self.kw_pattern.search(line)
         if kw_line_match:
             status = True
             self.create_perl_txt_obj_on_match(line, kw_line_match)
         # kw_line_match = self.kw_pattern_if.search(line)
         # if kw_line_match:
         #     status = True
         #     self.create_perl_txt_obj_on_match(kw_line_match, line)

         return status

    def prepare_multiline_kw(self, line):
         # print(line)
         if not self.prepare_kw(line):
             self.create_perl_txt_obj_on_match(line)


    def prepare_nonkw(self, line):
         status = False
         # print(is_cmnt.search(line))
         if is_cmnt.search(line) or line.strip("\n|\r|\t").strip()=='':
             self.create_perl_txt_obj_on_match(line)
             return True

         match = if_clause.search(line)
         if match:
                 status = True
                 self.create_perl_txt_obj_on_match(line)
         else:
             status = False

         return status

    def create_perl_txt_obj_on_match(self, line, kw_line_match=None):
         perl_txt_obj = Perl_Text(line)
         if kw_line_match:
            kw = self.get_kw(kw_line_match)
            param_string, params = self.get_params(kw_line_match)
            perl_txt_obj.set_kw(kw)
            perl_txt_obj.set_param_string(param_string)
            perl_txt_obj.set_params(params)
         self.add_perl_txt(perl_txt_obj)

    def get_kw(self, match):
        # print(match.group(1))
        return match.group(1)

    def get_params(self, match):
         param_string = match.group(2).strip(" |)")
         # print(param_string)
         if param_string=='':
             params = ''
         else:
            params = self.parse_params(param_string)
         # print(params)
         return param_string, params

    def parse_params(self, param_string):
         hash = self.check_hash_pattern.search(param_string)
         if hash:
             return self.parse_hash(hash.group(1))
         else:
             return param_string.split(',')

    def parse_hash(self, param_string):
         params = {}
         all_values = self.hash_pattern.findall(param_string)
         for val in all_values:
             items = val.split('=>')
             params[items[0].strip()] = items[1].strip()
         return params




if __name__ == "__main__":
   parser = Parser()
   for file in file_list:
        file_name = file.split("\\")[-1]
        parser.prepare_perl_txt_obj(file)


