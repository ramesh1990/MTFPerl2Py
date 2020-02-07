import re
post_fix_pattern = re.compile("\d*$")
class Perl_Text():

    def __init__(self, line_txt):
        self.line = line_txt
        self.kw = None
        self.params = []
        self.param_string = None
        self.post_fix = None


    def set_kw(self, name):
        post_match = post_fix_pattern.search(name)
        if post_match:
            self.post_fix = post_match.group(0)
            self.kw = post_fix_pattern.sub(repl="", string=name)
        else:
            self.kw = name

    def set_param_string(self, string):
        self.param_string = string

    def set_params(self, param_list):
        self.params = param_list

    def __repr__(self):
        return "{}\n{}\n{}\n{}\n{}\n".format(self.line, self.kw, self.post_fix,self.params, self.param_string)