import os # Для получения имен файлов
import codecs # Для открытия файла
import re # Регулярные выражения
from bs4 import BeautifulSoup # Парсинг Html
from collections import Counter # Нахождение одинаковых элементов в массиве
import mailparser

path = './mail/' #Адрес каталога

emls = os.listdir(path) #Получение списка файлов 

eFormCount=[]
eFromLoginCount=[]
SubjCount=[]
LinksCount=[]
nFromCount=[]
listIdCount=[]
messageBodyCount=[]
titleBodyCount=[]
IPCount=[]



# Читаем фаил
def open(eml):
	fileObj = codecs.open( eml, "r", "utf_8_sig" ) 
	text = fileObj.read() 
	fileObj.close()
	return text

# BS для парсинга HTML	
def soup(text):
	text=text.lower()
	soup=BeautifulSoup(text, 'lxml')
	return soup

# Проаерка электронного адреса отправителя
def eForm(text):
	result=re.findall('X-Envelope-From:.+?(\w+@\w+.+?\w+)', text)
	return result[0]

# Проверка логина отправителя
def eFromLogin(text):
	result = re.findall(r'\w+@', text)
	return result[0]

# Проверка темы письма
def Subj(text):
	mail = mailparser.parse_from_string(text)
	return mail.subject

# Проверка ссылок в письмах
def Links(text):
	result = re.findall(r'://(.+?)\"', text)

	return result

# Проверка имени отправителя
def nFrom(text):
	mail = mailparser.parse_from_string(text)
	result = re.findall(r'(.+?)<.+?>', mail.from_)
	return result[0]

# Проверка List-ID
def listId(text):
	result=re.findall('List-ID: \w+@(.+?)\s', text)
	return result

# Определение IP отправителя
def IP(text):
        result=re.findall('Received: from \\[(.+?)\\].+?\\(port', text)
        return result

# Только уникальные элементы массива
def unique(lst):
    seen = set()
    result = []
    for x in lst:
        if x in seen:
            continue
        seen.add(x)
        result.append(x)
    return result

# Проверка текста сообщения
def messageBody(soup):
	message=" "
	for cont in soup.findAll('font'):
		try:       
			message+=" "
			message+=cont.contents[0]
		except:
			p=0
	
	stopWords=[r' в ', r' от ', r' на ', r' и ', r' за ', r' не ', r',', r'!', r' уже ', r'[.]', r'-']
	for stopWord in stopWords:
		message = re.sub(stopWord, ' ', message)		
	message=unique(message.split())
	return message

# Проверка текста title
def titleBody(soup):
        soup=BeautifulSoup(text, 'lxml')
        titleTag = soup.find('title')
        titleTag1 = titleTag.contents[0] 
        stopWords=[r'!', r'—', r'[?]', r'“', r',', r'[.]', r'”', r'[(]', r'[)]']
        for stopWord in stopWords:
                titleTag1 = re.sub(stopWord, ' ', titleTag1)
        titleTag=unique(titleTag1.split())
        return(titleTag)


# Цикл обработки файлов
for eml in emls:
	text=open(path+eml)
	mBody=soup(text)
	messageBodyCount.extend(messageBody(mBody))
	titleBodyCount.extend(titleBody(mBody))
	eFormCount.append(eForm(text))
	eFromLoginCount.append(eFromLogin(text))
	SubjCount.append(Subj(text))
	LinksCount.extend(Links(text))
	nFromCount.append(nFrom(text))
	listIdCount.extend(listId(text))
	IPCount.extend(IP(text))


print("Проверка на повторения адреса отправителя")
print(Counter(eFormCount))
print("================================================================")
print("Проверка на повторения логина отправителя")
print(Counter(eFromLoginCount))
print("================================================================")
print("Проверка на повторения темы письма")
print(Counter(SubjCount))
print("================================================================")
print("Проверка на повторения ссылок в письме")
print(Counter(LinksCount))
print("================================================================")
print("Проверка на имени отправителя")
print(Counter(nFromCount))
print("================================================================")
print("Проверка на повторения севиса отправителя")
print(Counter(listIdCount))
print("================================================================")
print("Проверка на повторение Ip отправителя")
print(Counter(IPCount))
print("================================================================")
print("Проверка на повторение текста в письме")
print(Counter(messageBodyCount))
print("================================================================")
print("Проверка на повторение аголовка в письме")
print(Counter(titleBodyCount))




