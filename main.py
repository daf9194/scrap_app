from bs4 import BeautifulSoup
import requests
import json

key_word = input('key_word: ')
url = 'https://play.google.com/store/search'

params = {'q': key_word}
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'
}
r = requests.get(url, params=params, headers=headers)   #запрос к url
with open('index.html', 'w') as f:      #сохраняем полученую html страницу в файл
    f.write(r.text)


soup = BeautifulSoup(r.text, 'lxml')
app = soup.find_all(class_='Si6A0c Gy4nib')
app_dict = {}                                           #находим в на странице подходящие приложения,
for i in app:                                           #парсим название и url каждого приложения
    if key_word.lower() in i.text.lower():              #упаковываем в словарь app_dict
        app_name = i.find(class_="DdYX5").text
        app_href = i.get('href')
        app_dict[app_name] = app_href


result_dict = {}
for ind, i_app in enumerate(app_dict):
    url = f'https://play.google.com{app_dict[i_app]}'
    resp = requests.get(url=url, headers=headers)
    soup_2 = BeautifulSoup(resp.text, 'lxml')                   #проходим циклом по словарю, обращаясь к каждой ссылке
    author = soup_2.find(class_='Vbfug auoIOc')                 #на детальную страницу приложения, собираем необходимые данные
    rated = soup_2.find(class_='w7Iutd').find('span')
    discript = soup_2.find(class_='bARER')
    try:
        stars = soup_2.find(class_='TT9eCd').text
        cnt_stars = soup_2.find(class_='g1rdde').text
    except:
        stars = 'NONE'                                          #если данных нет, присваеваем значение none
        cnt_stars = 'NONE'

    result_dict[ind] = [{'name': i_app}, {'url': url}, {'discription': discript.text}, {'author': author.text}, {
        'rated': rated.text}, {'stars': stars}, {'cnt_stars': cnt_stars}]

with open('result.json', 'w') as file:                          #собираем результат в словарь result_dict, 
    json.dump(result_dict, file, indent=4, ensure_ascii=False)  #сохраняем словарь в json
