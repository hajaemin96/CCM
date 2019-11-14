#-*- encoding: utf8 -*-
import pep8
import StringIO
import sys
import os
import tempfile
import re


def template_pep8(temp):
    return {'type': temp[3][1],
            'code': temp[3][2:5],
            'line': temp[1],
            'place': temp[2],
            'text': temp[3][6:]}


def template_results(temp):
    return {'type': temp[0][0],
            'code': temp[0][1:],
            'line': temp[1],
            'place': temp[2],
            'text': temp[3]}


def pep8parser(strings, temp_dict_f=template_pep8):
    result_list = []
    for s in strings:
        temp = re.findall(r"(.+?):(.+?):(.+?):(.*)", s)
        if temp and len(temp[0]) >= 4:
            result_list.append(temp_dict_f(temp[0]))
    return result_list


def check_text(text, temp_dir, logger=None):
    # pep8 옵션 추가
    pep8_option_list = []
    with open('pep8-option.txt', 'r') as f:
        for val in f.read().splitlines():
            pep8_option_list.append(val)    
    code_file, code_filename = tempfile.mkstemp(dir=temp_dir)
    with open(code_filename, 'w') as code_file:
        code_file.write(text.encode('utf8'))
    pep8style = pep8.StyleGuide(parse_argv=False, config_file=False)
    options = pep8style.options
    temp_outfile = StringIO.StringIO()
    sys.stdout = temp_outfile
    checker = pep8.Checker(code_filename, options=options)
    checker.check_all()
    sys.stdout = sys.__stdout__
    result = temp_outfile.buflist[:]
    temp_outfile.close()
    code_file.close()
    os.remove(code_filename)
    fullResultList = pep8parser(result)
    fullResultList.sort(key=lambda x: (int(x['line']), int(x["place"])))
    if (pep8_option_list is not None):
        for val in pep8_option_list:
            for idx, result in enumerate(fullResultList):
                if (result.get('code') == val[1:]) and (result.get('type') == val[0]):
                    fullResultList.pop(idx)
    if logger:
        logger.debug(result)
    return fullResultList

def is_py_extension(filename):
    return ('.' in filename) and (filename.split('.')[-1] == 'py')

if __name__ == '__main__':
    pass
