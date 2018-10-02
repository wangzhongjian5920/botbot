# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 13:53:34 2018

@author: Paul
"""

import pandas as pd
import random
#from input_process import *

Data = 'dataset.csv'

def transfer_keyword(keyword):
    columns = ['LECTURE NAME', 'LECTURE CODE', 'LECTURE LOCATION AND TIME',
               'PROFESSOR', 'PROFESSOR CONTACT', 'LECTURE CAREER', 'LECTURE WEBSITE', 'LECTURE UNITS OF CREDIT',
               'LECTURE INTRODUCTION']
    """
    columns = ['LECTURE NAME', 'LECTURE CODE', 'LECTURE LOCATION AND TIME',
                'LECTURE CAREER', 'LECTURE WEBSITE', 'LECTURE UNITS OF CREDIT',
               'LECTURE INTRODUCTION','PROFESSOR', 'PROFESSOR CONTACT']
    """
    new_list = []
    for i in keyword:
        new_list.append(i.upper())

    for c in columns:
        for i in new_list:
            if i in c:
                if c not in new_list:
                    new_list.append(c)
                else:
                    continue

#    print(new_list)
    return new_list


def match(keyword):
    columns = ['LECTURE NAME', 'LECTURE CODE', 'LECTURE LOCATION AND TIME',
               'PROFESSOR', 'PROFESSOR CONTACT', 'LECTURE CAREER', 'LECTURE WEBSITE', 'LECTURE UNITS OF CREDIT',
               'LECTURE INTRODUCTION']
    """
    columns = ['LECTURE NAME', 'LECTURE CODE', 'LECTURE LOCATION AND TIME',
                'LECTURE CAREER', 'LECTURE WEBSITE', 'LECTURE UNITS OF CREDIT',
               'LECTURE INTRODUCTION','PROFESSOR', 'PROFESSOR CONTACT']
    """
    column = []
#    print(keyword)
    other = []
    for i in keyword:
        if i in columns:
            column.append(i)
        else:
            other.append(i)
#    print(column, other)


    if column == []:
        column = columns


    check = False
    match_res = []

    df_col_1 = pd.read_csv(Data, index_col = 'LECTURE NAME')
    for row in df_col_1.index:
        if row in other:
            for c in df_col_1:
                if c in column:
                    if df_col_1.loc[row, c] != 'None':
                        match_res.append(message(c, df_col_1.loc[row, c]))
                        check = True


    df_col_2 = pd.read_csv(Data, index_col = 'LECTURE CODE')
    for row in df_col_2.index:
        if row in other:
            for c in df_col_2:
                if c in column:
                    if df_col_2.loc[row, c] != 'None':
                        match_res.append(message(c, df_col_2.loc[row, c]))
                        check = True


    df_col_3 = pd.read_csv(Data, index_col = 'LECTURE LOCATION AND TIME')
    for row in df_col_3.index:
        if row in other:
            for c in df_col_3:
                if c in column:
                    if df_col_3.loc[row, c] != 'None':
                        match_res.append(message(c, df_col_3.loc[row, c]))
                        check = True


    df_col_4 = pd.read_csv(Data, index_col = 'PROFESSOR')
    for row in df_col_4.index:
        if row in other:
            for c in df_col_4:
                if c in column:
                    if df_col_4.loc[row, c] != 'None':
                        match_res.append(message(c, df_col_4.loc[row, c]))
                        check = True


    df_col_5 = pd.read_csv(Data, index_col = 'PROFESSOR CONTACT')
    for row in df_col_5.index:
        if row in other:
            for c in df_col_5:
                if c in column:
                    if df_col_5.loc[row, c] != 'None':
                        match_res.append(message(c, df_col_5.loc[row, c]))
                        check = True


    df_col_6 = pd.read_csv(Data, index_col = 'LECTURE CAREER')
    for row in df_col_6.index:
        if row in other:
            for c in df_col_6:
                if c in column:
                    if df_col_6.loc[row, c] != 'None':
                        match_res.append(message(c, df_col_6.loc[row, c]))
                        check = True

    df_col_7 = pd.read_csv(Data, index_col = 'LECTURE WEBSITE')
    for row in df_col_7.index:
        if row in other:
            for c in df_col_7:
                if c in column:
                    if df_col_7.loc[row, c] != 'None':
                        match_res.append(message(c, df_col_7.loc[row, c]))
                        check = True

    df_col_8 = pd.read_csv(Data, index_col = 'LECTURE UNITS OF CREDIT')
    for row in df_col_8.index:
        if row in other:
            for c in df_col_8:
                if c in column:
                    if df_col_8.loc[row, c] != 'None':
                        match_res.append(message(c, df_col_8.loc[row, c]))
                        check = True

    df_col_9 = pd.read_csv(Data, index_col = 'LECTURE INTRODUCTION')
    for row in df_col_9.index:
        if row in other:
            for c in df_col_9:
                if df_col_9.loc[row, c] != 'None':
                    match_res.append(message(c, df_col_8.loc[row, c]))
                    check = True
    if check is False:
        return print_output([])

    return match_res


def message(c, g):
    columns = ['LECTURE NAME', 'LECTURE CODE', 'LECTURE LOCATION AND TIME',
               'PROFESSOR', 'PROFESSOR CONTACT', 'LECTURE CAREER', 'LECTURE WEBSITE', 'LECTURE UNITS OF CREDIT',
               'LECTURE INTRODUCTION']
    """
    columns = ['LECTURE NAME', 'LECTURE CODE', 'LECTURE LOCATION AND TIME',
                'LECTURE CAREER', 'LECTURE WEBSITE', 'LECTURE UNITS OF CREDIT',
               'LECTURE INTRODUCTION','PROFESSOR', 'PROFESSOR CONTACT']
    """
    res = []
#    mes_lec_name = 'The Lecture name is: '
#    mes_lec_code = 'The Lecture code is: '
#    mes_lec_timetable = 'The timetable of lecture is: '
#    mes_lec_professor = 'The professor of lecture is: '
#    mes_contact = 'The contact number of professor is: '
#    mes_career = 'The type of lecture is: '
#    mes_website = 'The homepage of lecture is: '
#    mes_credit = 'The credit units of lecture is: '
#    mes_introduction = 'The introduction of lecture is: '

    mes = ['The Lecture name is: ', 'The Lecture code is: ', 'The timetable of lecture is: ',
           'The professor of lecture is: ', 'The contact number of professor is: ',
           'The type of lecture is: ', 'The homepage of lecture is: ',
           'The credit units of lecture is: ', 'The introduction of lecture is: ']
#    if g != 'None':
    for i in range(len(columns)):
        if c == columns[i]:
            res.append(mes[i] + g)
            break
#    if c == columns[0]:
#        res.append(mes_lec_name + g)
#    elif c == columns[1]:
#        res.append(mes_lec_code + g)
#    elif c == columns[2]:
#        res.append(mes_lec_timetable + g)
#    elif c == columns[3]:
#        res.append(mes_lec_professor + g)
#    elif c == columns[4]:
#        res.append(mes_contact + g)
#    elif c == columns[5]:
#        res.append(mes_career + g)
#    elif c == columns[6]:
#        res.append(mes_website + g)
#    elif c == columns[7]:
#        res.append(mes_credit + g)
#    else:
#        res.append(mes_introduction + g)
    

    return print_output(res)

def print_output(res):
    out = ''
#    print(res)
    if len(res) != 0:
        for i in res:
            out += i
    else:
        out = []
        out_base = ["Sorry, it's out of my knowledge, maybe you can find it on www.handbook.unsw.edu.au",
                    'Emmmm, I have no idea about that, please check your input',
                    "Sorry, it's out of my knowledge, maybe you can find it on cse website: www.engineering.unsw.edu.au/computer-science-engineering",
                    "Sorry, it's out of my knowledge"]
        rand_ans = random.randint(0,len(out_base) - 1)
        out.append(out_base[rand_ans])

    return out

def final_result(keyword):
    step_1 = transfer_keyword(keyword)
    c = match(step_1)
#    print(c)
#    final_result = ''.join(c)

    return c

#a = Key_words("Who is GSOE9820?")
#b = final_result(a)
#for i in b:
#    print(i)


if __name__ == "__main__":
    a = transfer_keyword(['comp6714','professor'])
    print(match(a))
