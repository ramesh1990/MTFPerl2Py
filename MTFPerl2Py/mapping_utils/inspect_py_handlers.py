# import modules
import os
import re
import fnmatch
import csv

param_pttrn = re.compile('(\w+)\s*\(:')

def get_path_from_user():
    root_dir = input("Enter the root path for searching the files: ")
    return root_dir

def invalid_path(errorMsg):
    print(errorMsg)
    exit(-1)

def get_dir_tree(path):
    return os.walk(path, onerror=invalid_path)

def get_file_name_pattern():
    return '*.py' # scn file pattern

def get_content_pattern():
    return re.compile(r'^(\w+)(\(.*\));', re.M) # search for keyword,param_values

def get_class_def_pattern():
    return re.compile(r'^class\s+(\w+)', flags=re.M)

def get_method_def_pattern():
    return re.compile(r'^\s+def\s+(?!_+)(\w+)', flags=re.M)

# def get_kwargs_pattern():
#     return re.compile(r'kwargs.get\(\s*[\'\"]*(\w+)', flags=re.M)

def get_kwargs_pattern():
    return re.compile(r'Args\s*:+(.*)Example', flags=re.M|re.DOTALL)

def create_csv_file(file_name):
    fp = open(file_name + ".csv", 'w', newline='')
    return fp

def create_csv_writer(fp):
    filewriter = csv.writer(fp, delimiter=',')
    return filewriter

def write_to_csv(data, writer):
    writer.writerows(data)

def close_csv_file(fp):
    fp.close()
    print("csv file location : %s"%(os.getcwd() + "\\" + fp.name))

def check_for_py_files(files, file_pattern):
    py_file_list = fnmatch.filter(files, file_pattern)
    return py_file_list

def get_class_blocks(pttrn, data):
    blocks = pttrn.split(data)
    return blocks[1:]

def get_method_blocks(pttrn, data):
    blocks = pttrn.split(data)
    return blocks[1:]

def parse_kwargs(pttrn, data):
    match = pttrn.search(data)
    if match:
        return param_pttrn.findall(match.group(0))

    return [""]

def get_handler_py_mod(dir_tree, file_pattern):
    py_file_list = []
    for root, dirs, files in dir_tree:
        file_list = check_for_py_files(files, file_pattern)
        for filename in file_list:
            file_path = os.path.join(root, filename)
            py_file_list.append(file_path)
    return py_file_list

def parse_files(file_path):
    matched_list = []
    no_match_list = []
    class_def_ptrn = get_class_def_pattern()
    method_def_ptrn = get_method_def_pattern()
    kwargs_ptrn = get_kwargs_pattern()
    with open(file_path) as fp:
        data = fp.read()
    class_blocks = get_class_blocks(class_def_ptrn, data)
    for idx in range(1,len(class_blocks),2):
        class_name = class_blocks[idx-1]
        method_blocks = get_method_blocks(method_def_ptrn, class_blocks[idx])
        for idx in range(1,len(method_blocks),2):
            method_name = method_blocks[idx-1]
            kwargs_list = parse_kwargs(kwargs_ptrn, method_blocks[idx])
            matched_list.append([class_name, method_name, ":".join(kwargs_list)])

    return matched_list, no_match_list

def main():
    root_dir = get_path_from_user()
    dir_tree = get_dir_tree(root_dir)  # get directory tree if present else exit
    file_pattern = get_file_name_pattern()
    handler_files = get_handler_py_mod(dir_tree, file_pattern)
    fp = create_csv_file(file_name="py_keyword_info")
    if not handler_files:
        print("No py files found at %s" % root_dir)
        exit(-1)
    for path in handler_files:
        py_file_name = path.split("\\")[-1]
        print("Processing %s "%(py_file_name))
        matched_data, no_matched_data = parse_files(path)
        if not matched_data:
            print("No classes/methods found in %s file"%(path))
        else:
            handler_name = py_file_name.strip('.py')
            csv_writer = create_csv_writer(fp)
            write_to_csv(matched_data, csv_writer)
    close_csv_file(fp)

if __name__ == "__main__":
    main()
