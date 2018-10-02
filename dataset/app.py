from flask import Flask, render_template, request
#from chatterbot import ChatBot
#from chatterbot.trainers import ChatterBotCorpusTrainer



app = Flask(__name__)

#english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
#
#english_bot.set_trainer(ChatterBotCorpusTrainer)
#english_bot.train("chatterbot.corpus.english")

import nltk
from nltk.probability import FreqDist
from nltk.corpus import wordnet as wn
import copy

columns = ['LECTURE NAME', 'LECTURE CODE', 'LECTURE LOCATION AND TIME',
            'LECTURE CAREER', 'LECTURE WEBSITE', 'LECTURE UNITS OF CREDIT',
           'LECTURE INTRODUCTION','PROFESSOR', 'PROFESSOR CONTACT']
#print(lemma.name for lemma in wn.synset('teacher.n.01').lemmas)

def Similar_words(word):
    similar_word = copy.deepcopy(word)
    for w in word:
        if w in ['CLASS','COURCE','LESSON','SUBJECT']:
            similar_word[word.index(w)] = 'LECTURE'
            continue
        """
        if w in ['CLASS NAME','COURCE NAME','lesson name','subject name']:
            similar_word[word.index(w)] = 'LECTURE NAME'
            continue
        if w in ['class code','cource code','lesson code','subject code']:
            similar_word[word.index(w)] = 'LECTURE CODE'
            continue
        """
        if w in ['LOCATION','PLACE','POSITION','SITUATION','SPOT','WHERE','WHEN','TIME','DATE','PERIOD','SCHEDULE','PLAN','TIMETABLE']:
            similar_word[word.index(w)] = 'LECTURE LOCATION AND TIME'
            continue
        if w in ['WEBSITE','WEB PAGE','SITE','FORUM','NETWORK','INTERNET SITE']:
            similar_word[word.index(w)] = 'LECTURE WEBSITE'
            continue
        if w in ['INTRODUCTION','OUTLINE','OVERVIEW','SUMMARY','ROUGH GUIDE']:
            similar_word[word.index(w)] = 'LECTURE INTRODUCTION'
            continue
        if w in ['ASSISTANT','EDUCATOR','INSTRUCTOR','LECTURER','TEACHER','TUTOR','PROF','WHO']:
            similar_word[word.index(w)] = 'PROFESSOR'
            continue
        if w in ['E-MAIL','LINK','CALL','PHONE']:
            similar_word[word.index(w)] = 'CONTACT'
            continue
        """
        if w in ['HELLO','HI','HEY','MORNING','GREETINGS','WELCOME','HALLO','HIYA','HOLA','YO','GODD MORNING','GOOD AFTERNOON','GODD EVENING']:
            similar_word[word.index(w)] = 'HELLO'
            continue
        if w in ['BYE','BYE-BYE','GOODBYE','SEE YOU','SEE YOU LATER']:
            similar_word[word.index(w)] = 'BYE'
            continue
        """
    return similar_word
    """
    synonyms = []
    for syn in wn.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
    print(synonyms)
    #print(wn.synset('teacher.n.01').definition)
    """

def Combine_words(key_word):
    res = []
    # Combine two words
    if 'LECTURE' in key_word and 'NAME' in key_word:
        res.append('LECTURE NAME')
        key_word.remove('LECTURE')
        key_word.remove('NAME')
    if 'LECTURE' in key_word and 'CODE' in key_word:
        res.append('LECTURE CODE')
        key_word.remove('LECTURE')
        key_word.remove('CODE')
    if 'PROFESSOR' in key_word and 'CONTACT' in key_word:
        res.append('PROFESSOR CONTACT')
        key_word.remove('PROFESSOR')
        key_word.remove('CONTACT')
    """
    if 'GOOD' in key_word and 'MORNING' in key_word:
        res.append('GOOD MORNING')
        key_word.remove('GOOD')
        key_word.remove('MORNING')
    if 'GOOD' in key_word and 'AFTERNOON' in key_word:
        res.append('GOOD AFTERNOON')
        key_word.remove('GOOD')
        key_word.remove('AFTERNOON')
    if 'GOOD' in key_word and 'EVENING' in key_word:
        res.append('GOOD EVENING')
        key_word.remove('GOOD')
        key_word.remove('EVENING')
    if 'SEE' in key_word and 'YOU' in key_word and 'LATER' in key_word:
        res.append('SEE YOU LATER')
        key_word.remove('SEE')
        key_word.remove('YOU')
        key_word.remove('LATER')
    if 'SEE' in key_word and 'YOU' in key_word:
        res.append('SEE YOU')
        key_word.remove('SEE')
        key_word.remove('YOU')
    """
    return res+key_word
#Similar_words('teacher')

def Transfer_to_noun(verb_word):
    """ Transform a verb to the closest noun: die -> death """
    verb_synsets = wn.synsets(verb_word, pos="v")
    # Word not found
    if not verb_synsets:
        return []
    # Get all verb lemmas of the word
    verb_lemmas = [l for s in verb_synsets \
                   for l in s.lemmas() if s.name().split('.')[1] == 'v']
    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms()) \
                                    for l in verb_lemmas]
    # filter only the nouns
    related_noun_lemmas = [l for drf in derivationally_related_forms \
                           for l in drf[1] if l.synset().name().split('.')[1] == 'n']
    # Extract the words from the lemmas
    words = [l.name for l in related_noun_lemmas]
    len_words = len(words)
    # Build the result in the form of a list containing tuples (word, probability)
    result = [(w, float(words.count(w))/len_words) for w in set(words)]
    result.sort(key=lambda w: -w[1])
    # return all the possibilities sorted by probability
    return result[0][0]()

def Key_words(sentence):
    sentence_split = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(sentence_split)
    #fdist1 = FreqDist(sentence_split)
    #minfo = dict(fdist1)

    # Extract noun word and number
    tag_list_n = ['NN','NNS','NNP','NNPS','CD']
    key_word_n = list(set([k.lower() for k,v in tagged if v in tag_list_n]))
    #print(key_word_n)

    # Extract verb word
    tag_list_v = ['VB','VBD','VBG','VBN','VBP','VBZ']
    key_word_v = list(set([k.lower() for k,v in tagged if v in tag_list_v]))
    #print(key_word_v)
    for w in key_word_v:
        if w in ['is','are','be','was','were','been']:
            key_word_v.remove(w)
        if w in ['please']:
            key_word_v.remove(w)
    kwv = copy.deepcopy(key_word_v)
    for w in key_word_v:
        #print(w)
        kwv[key_word_v.index(w)] = Transfer_to_noun(w)
    #print(kwv)

    # Extract WH words
    tag_list_wh = ['WDT','WP','WP$','WRB']
    key_word_wh = list(set([k.lower() for k,v in tagged if v in tag_list_wh]))
    #print(key_word_wh)

    # Total key words
    key_word = key_word_n+kwv+key_word_wh

    # Transfer to Upper word
    u_key_word = []
    #print(key_word)
    for i in key_word:
        if i!=[]:
            u_key_word.append(i.upper())
    #print(u_key_word)

    # Combine two single word to a word group
    #key_word = Combine_words(key_word)
    #print(key_word)

    # Match similar word in attribute table
    key_word = Similar_words(u_key_word)
    #print(key_word)

    # Combine two single word to a word group
    key_word = Combine_words(key_word)
    #print(key_word)

    # Remove same words
    key_word = list(set(key_word))
    #print(key_word)

    return key_word

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


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    keywords = Key_words(userText)
    a = transfer_keyword(keywords)
    res = match(a)
#    return str(english_bot.get_response(userText))
#    for i in res:
#        return str(i)
    return '\n'.join(map(str,res))





if __name__ == "__main__":
    app.run()
