import random
import os
from datetime import datetime
import cv2 as cv
import imgkit

def normal_character(c):
    c_o = ord(c)
    return (c_o>=65 and c_o<=90) or (c_o>=97 and c_o<=122) or (c_o>=48 and c_o<=57)

def convert_char(c):
    return '&#'+str(hex(ord(c)))[1:]+';'

def sanitize_input(text):
    sanitized_text = ''
    for c in text:
        if normal_character(c):
            sanitized_text += c
        else:
            sanitized_text += convert_char(c)

    return sanitized_text

def post_screenshot(post_text, green_text, image_path, name='Anonymous', filename='mfw.jpg', output_filename='page_screenshot.png'):
    replacements = {}

    with open('default_replacements', 'r') as rep_file:
        lines = rep_file.readlines()

        for line in lines:
            equals_index = line.find('=')
            var_name = line[:equals_index]
            var_val = line[equals_index+1:].strip('\n')

            replacements[var_name] = var_val

    c_img = cv.imread(image_path)

    replacements['FINDANDREPLACEME_TEXTBODY'] = post_text
    replacements['FINDANDREPLACEME_GREENTEXT'] = green_text
    replacements['FINDANDREPLACEME_FILENAME'] = filename
    replacements['FINDANDREPLACEME_IMG'] = image_path
    replacements['FINDANDREPLACEME_IMGWIDTH'] = c_img.shape[1]
    replacements['FINDANDREPLACEME_IMGHEIGHT'] = c_img.shape[0]
    replacements['FINDANDREPLACEME_IMAGESIZE'] = str(round(os.path.getsize(image_path)/1024, 1))+' KB'
    replacements['FINDANDREPLACEME_POSTERNAME'] = name

    oppost_num = random.randrange(10000000, 100000000)
    replacements['FINDANDREPLACEME_OPPOSTNUMBER'] = oppost_num
    replacements['FINDANDREPLACEME_POSTNUMBER'] = oppost_num+random.randrange(1, 10)

    dt_today = datetime.now()
    replacements['FINDANDREPLACEME_DATE'] = dt_today.strftime('%m/%d/%y(%a)%H:%M:%S')

    #parse the inputs DANGER ALERT!!!!
    #if i messed something up u will have an arbitrary code execution bug or something alike :)
    for r_key, r_val in replacements.items():
        replacements[r_key] = sanitize_input(str(r_val))

    edited_html_name = 'edited.html'
    edited_html_file = open(edited_html_name, 'w')

    with open('main.html', 'r') as html_file:
        lines = html_file.readlines()
        for line in lines:
            parsed_line = line

            if len(parsed_line)<500:
                #dont search lines which are too long
                for r_name, r_val in replacements.items():
                    parsed_line = parsed_line.replace(r_name, r_val)

            edited_html_file.write(parsed_line)

    edited_html_file.close()

    kitopts = {'enable-local-file-access': None,
               'quiet': None,
               'log-level': 'error'}

    imgkit.from_file(edited_html_name, output_filename, options=kitopts)

    os.remove(edited_html_name)

    return output_filename