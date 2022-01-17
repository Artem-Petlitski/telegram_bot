import json

ar = []

with open("error_words", 'r', encoding='utf-8') as file:
    for words in file:
        word = words.lower().split('\n')[0]
        if word != "":
            ar.append(word)

with open('error_words.json', 'w', encoding='utf-8') as file_2:
    json.dump(ar, file_2)
