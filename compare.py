
import argparse
parser = argparse.ArgumentParser(description='Scores docs')
parser.add_argument('input', type=str, help='Input docs')
parser.add_argument('output', type=str, help='Output of the result')
args = parser.parse_args()

import re
from statistics import mean
import codecs #для декодировки файлов, так как с некоторыми файлами open не справлялся

inp=[] # для записи ссылок на 1-е тексты для сравнения из строчек документа input.txt
inp2=[]# для записи ссылок на 2-е тексты для сравнения из строчек документа input.txt

file = open(args.output, 'w') # файл для записи итоговых результатов

for i in open(args.input):
    inp.append(i.split()[0])
    inp2.append(i.split()[1])

#согдаем пустые списоки и записываем в них строки из документов для сравнения
text=[]
text2=[]

for ind in range(len(inp)):
    for doc in codecs.open(inp[ind], "r", "utf-8" ):
        text.append(doc)
#удаляем из строк лишние символы и заменяим их на пробелы
    for i in range(len(text)):
        text[i]=re.sub("[^A-Za-z]", " ", text[i])
        
#удаляем пробелы в начале и конце строк и переводим все буквы в нижний регистр
    for i in range(len(text)):
        text[i]=text[i].strip().lower()

#разделяем строки на сткроки собержащие только одно слово или буквы через разделитель "пробел"
    textr=[]
    textrbp=[] 
    texts=[] 
    for i in range(len(text)):
        for x in range(len(text[i].split(' '))):
            textrbp=text[i].split(' ')
            if textrbp[x]!= '': #исключаем строки ничего несодержащие 
                textr.append(textrbp[x])
                
#производим все те же операции для второго текста
    for doc2 in codecs.open(inp2[ind], "r", "utf-8" ):
        text2.append(doc2)

    for i in range(len(text2)):
        text2[i]=re.sub("[^A-Za-z]", " ", text2[i])
        
    for i in range(len(text2)):
        text2[i]=text2[i].strip().lower()

    text2r=[]
    text2rbp=[] 
    text2s=[] 
    for i in range(len(text2)):
        for x in range(len(text2[i].split(' '))):
            text2rbp=text2[i].split(' ')
            if text2rbp[x]!= '': #исключаем строки ничего несодержащие 
                text2r.append(text2rbp[x])
                
#находим "уникальные" элементы текстов относительно друг друга, чтобы далее не работать с явно совпадающими          
    res1 = [x for x in textr + text2r if x not in text2r]
    res2 = [x for x in textr + text2r if x not in textr]
    #uniqsr=sum([len(element) for element in res2])/sum([len(element) for element in text2r]) - определение уникальности простым сравнением списков (в виде комментария, чтобы без необходимости не нагружал систему лишними вычислениями)
    #print("уникальность через сравнение:",round(uniqsr, 3))
    
#далее для "уникальных" элементов второго текста применяем метод расстояние Левенштейна  
    uniqlev=0 #колличество "уникальных" символов текста 
    if len(res1) and len(res2) !=0:
        uniq21 = [] #список средних уникальностей "уникальных"элемента 2го текста относительно всех "уникальных" элементов 1го текста
        for str_2 in res2:
            lev21=[]  #уникальности "уникального"элемента 2го текста относительно всех "уникальных" элементов 1го текста
            for str_1 in res1:
                def levenstein(str_2, str_1):
                    n, m = len(str_2), len(str_1)
                    if n > m:
                        str_2, str_1 = str_1, str_2
                        n, m = m, n

                    current_row = range(n + 1)
                    for i in range(1, m + 1):
                        previous_row, current_row = current_row, [i] + [0] * n
                        for j in range(1, n + 1):
                            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                            if str_2[j - 1] != str_1[i - 1]:
                                change += 1
                                current_row[j] = min(add, delete, change)
                    return current_row[n]
                lev21.append(1-levenstein(str_1, str_2)/max(len(str_1), len(str_2)))
            uniq21.append(mean(lev21))
        for ide in range(len(res2)):
            uniqlev+=len(res2[ide])*uniq21[ide] #кол-во уникальных символов второго текста
    else:
        uniqlev=0
        
#определяем итоговую уникальность 2го текста относительно 1го (по колличеству символов, чтобы уменьить влияние одиночных букв)
    uniq=uniqlev/sum([len(element) for element in text2r])
    print(round(uniq, 3))
    file.write(str(round(uniq, 3)) + "\n")
file.close()