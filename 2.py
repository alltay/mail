import os # Для получения имен файлов
import codecs # Для открытия файла
import re # Регулярные выражения
from bs4 import BeautifulSoup # Парсинг Html
from collections import Counter # Нахождение одинаковых элементов в массиве
import mailparser # помощь в парсинге некоторых заголовков
from validate_email import validate_email # Проверка валидности почты
import dns.resolver # Проверка на наличие в спамбазах


file='./mail/610771551.eml'

print('Анализ файла'+file)

# Чтение из файла
fileObj = codecs.open( file, "r", "utf_8_sig" ) 
text = fileObj.read()
fileObj.close()

# Чтение из файла словаря
fileObj = codecs.open( 'dict.txt', "r", "utf_8_sig" ) 
dictionary= fileObj.read()
fileObj.close()
dictionary=dictionary.split()


soup=BeautifulSoup(text, 'lxml')
mail = mailparser.parse_from_string(text)

# Адрес отправителя
result=re.findall('X-Envelope-From:.+?(\w+@\w+.+?\w+)', text)

# Проверка на валидность адреса отправителя
is_valid = validate_email(result[0])

# Определение IP отправителя
senderIP=re.findall('Received: from \\[(.+?)\\].+?\\(port', text)


# Нахождение title письма
text=text.lower()
titleTag = soup.find('title')
titleTag = titleTag.contents[0] 


# Только уникальные значения массива
def unique(lst):
    seen = set()
    result = []
    for x in lst:
        if x in seen:
            continue
        seen.add(x)
        result.append(x)
    return result

# Разбиваем текст сообщения на слова
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


# Поиск совпадений в словаре
def bad(message, dictionary):
	badwords=[]
	for word in message:
                
		for words in dictionary:
			if(word.lower()==words.lower()):
				badwords.append(word)
	return unique(badwords)



if (is_valid==True):
        print('Почтовый адрес '+result[0]+' валиден.\n ====================')
else:
        print('Неверный почтовый адрес!\n ====================')

if (titleTag==mail.subject):
	print ('Тема письма и title совпадают.\n ====================')
else:
	print ('Тема письма и title не совпадают!\n ====================')

# Проверка на наличие в спамбазах

bls = ["zen.spamhaus.org", "spam.abuse.ch", "cbl.abuseat.org", "virbl.dnsbl.bit.nl", "dnsbl.inps.de", 
    "ix.dnsbl.manitu.net", "dnsbl.sorbs.net", "bl.spamcannibal.org", "bl.spamcop.net", 
    "xbl.spamhaus.org", "pbl.spamhaus.org", "dnsbl-1.uceprotect.net", "dnsbl-2.uceprotect.net", 
    "dnsbl-3.uceprotect.net", "db.wpbl.info"]
 

myIP = senderIP[0]

print("Проверка IP адреса на наличие в спам базах\n ====================")
for bl in bls:
    try:
        my_resolver = dns.resolver.Resolver()
        query = '.'.join(reversed(str(myIP).split("."))) + "." + bl
        answers = my_resolver.query(query, "A")
        answer_txt = my_resolver.query(query, "TXT")
        print ('IP: %s НАХОДИТСЯ в списке %s (%s: %s)' %(myIP, bl, answers[0], answer_txt[0]))
    except dns.resolver.NXDOMAIN:
        print ('IP: %s нет в списке %s' %(myIP, bl))


print('====================\nВ тексте найдены следующие сомнительные слова: ')
message=messageBody(soup)
print(bad(message, dictionary))

        
print('====================\nВ теме письма найдены следующие сомнительные слова: ')
sub=mail.subject
print(bad(sub.split(), dictionary))
