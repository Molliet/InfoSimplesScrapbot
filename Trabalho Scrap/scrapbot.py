from bs4 import BeautifulSoup
from unidecode import  unidecode
import json
import requests




data={}
url = 'https://infosimples.com/vagas/desafio/commercia/product.html'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')


#Classes
class Skus:

     def __init__(self, name, current_price, old_price, avaiable):
          self.name = name
          self.current_price = current_price          
          self.old_price = old_price
          self.avaiable = avaiable

class Properties:

     def __init__(self, label, value):
          self.label = label
          self.value = value     

class Reviews:

     def __init__(self, name, date, score, text):
          self.name = name
          self.date = date          
          self.score = score
          self.text = text     



#traduz para INT    
def dstars(stars):
     if stars=='★★★★★':
          stars = 5
     if stars=='★★★★☆':
          stars = 4
     if stars=='★★★☆☆':
          stars = 3
     if stars=='★★☆☆☆':
          stars = 2
     if stars=='★☆☆☆☆':
          stars = 1
     if stars=='☆☆☆☆☆':
          stars = 0
     return stars




#Pega titulo
title = soup.find(id='product_title').text

#save to data  
data['title'] = title



#Pega categoria
breadcrumb = soup.find('nav').text
bd_fmt = breadcrumb.strip().split("> ")

#save to data  
data['categories']=bd_fmt


#Pega descrição
proddet = soup.find(class_='proddet').text
description = unidecode(proddet)

#save to data  
data['description'] = description



#Cria classe skus
ducks = soup.find_all(itemprop='sku')
skus_list=[]
for info in ducks:  
     skus_fmt = info.parent
     name = skus_fmt.find(class_="prod-nome").text

     try:
          c_price = skus_fmt.find(class_="prod-pnow").text
     except AttributeError:
          c_price = None

     try:
          o_price = skus_fmt.find(class_="prod-pold").text
     except AttributeError:
          o_price = None

     if skus_fmt.find("i"):
          avaiable = False
     else:
          avaiable = True
     
     #Cria Dict de SKUS
     create_skus = Skus(name, c_price, o_price, avaiable)
     skus = create_skus.__dict__
     skus_list.append(skus)

#save to data  
data['skus'] = skus_list






#Cria classe  prorpiedades
tabela = soup.find(class_ = 'pure-table pure-table-bordered')
list_properties = []


for td in tabela.find_all('td'):
     for label in td.find_all('b'):
          p_label = label.text
          p_value = label.find_next('td').text

          #Cria Dict de Properties
          create_properties = Properties(p_label, p_value)
          properties = create_properties.__dict__
          list_properties.append(properties)

#save to data          
data['properties'] = list_properties

          



#Cria Classe Reviews
list_review=[]
list_avg_score=[]

comments = soup.find_all(class_='analisebox')
for box in comments:
     name = unidecode(box.find(class_='analiseusername').text)
     date = box.find(class_='analisedate').text     
     stars = box.find(class_='analisestars').text
     text = unidecode(box.find('p').text)
     stars = dstars(stars)

     #Cria Dict de Review
     create_review = Reviews(name, date, stars, text)
     review_box = create_review.__dict__
     list_review.append(review_box)
     list_avg_score.append(create_review.score)
media = round(sum(list_avg_score)/len(list_avg_score),2)

#save to data  
data['reviews'] = list_review
data['reviews_average_score'] = media
data['url'] = url





#dump data to jsonfile
with open("produto.json", "w") as f:
     json.dump(data, f, indent=4)
     print('SAVED')











     


