class Py_Text():

    def __init__(self, line_txt):
        self.line = line_txt
        self.kw = None
        self.params = []
        self.param_string = None


    def set_kw(self, name):
        self.kw = name

    def set_param_string(self, string):
        self.param_string = string

    def set_params(self, param_list):
        self.params = param_list

    # def __repr__(self):
    #     return "{}\n{}\n{}\n{}\n".format(self.line, self.kw, self.params, self.param_string)