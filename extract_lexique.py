#!/usr/bin/python3
# -*- coding: utf-8 -*-


# http://www.lexique.org/

# Lexique383.tsv
# mot, phonétique, racine, type, genre, nombre ... infoverbe(inf...)
#

GRAMM_CAT = ('VER', 'ADJ', 'ADV', 'NOM', 'PRO', 'PRE', 'LIA', 'CON',
             'AUX', 'ART', 'ONO')


import pickle as pk
import unidecode

with open("Lexique383.tsv" , 'r') as lx:
    RAW_DATA = lx.readlines()


def extract_all():
    """
    [(mot, racine, type, genre, nombre, infoverbe), (...), ...]
    """
    DATA = list()
    print("extract")
    for L in RAW_DATA:
        l = L.split('\t')
        DATA.append((unidecode.unidecode(l[0]), l[2], l[3], l[4], l[5], l[10]))
    print("write")
    with open("data_global.pk", 'wb') as save:
        myPk = pk.Pickler(save)
        myPk.dump(DATA)
    return DATA


def load_data():
    with open("data_global.pk", 'rb') as save:
        myPk = pk.Unpickler(save)
        DATA = myPk.load()
    return DATA

def generate_lexique(data, gramm_cat=GRAMM_CAT, conj=True, plur=True,
                     fem=True, symbols=" -'."):
    """
    Genere un fichier .txt avec tout les mots selon critères
    (mot, racine, type, genre, nombre, infoverbe)
    data = liste des mot (extract_all)
    gramm_cat catégories grammaticales voulues (ADV, VER, NOM...)
    conj False pour l'infinitif uniquement (si 'VER' dans gramm_cat)
    plur False pour exclure les pluriels
    fem False pour exclure les accords féminins (pas chaise, table...)
    symbols True pour tous, False pour aucun et str pour choisir
    """
    data2 = []
    
    def contains_symbols(w, sy):
        for i in w:
            if i in sy: return True
        return False
    
    for line in data:
        word = line[0]
        # exclude symbols
        if symbols == False and contains_symbols(word, " -'."):
            continue
        if type(symbols) == str and contains_symbols(word, symbols):
            continue
        # exclude by grammatical catergories
        if line[2][:3] not in gramm_cat:
            continue
        # exclude conj
        if line[2][:3] == "VER" and conj == False and 'inf' not in line[5]:
            continue
        # exclude plural
        if plur == False and line[4] == 'p':
            continue
        # exclude feminine
        if fem == False and line[3] == 'f':
            # mot accordé au feminin
            # unidecode car seule le mot est unidecodé
            if line[0] != unidecode.unidecode(line[1]):
                continue
        data2.append(line[0])
    result = sorted(set(data2))
    with open('lexique.txt', 'w') as lx:
        lx.writelines("\n".join(result))
    return result

def find(word, data):
    res = []
    for line in data:
        if line[0] == word:
            res.append(line)
    return res

if __name__ == '__main__':
    DATA = extract_all()
    a = generate_lexique(DATA, conj=False, plur=False, fem=False, symbols=False)
