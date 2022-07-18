import requests
from bs4 import BeautifulSoup
import pathlib as path
import pandas as pd
import csv
import re
import os


#function that displays all requested details from the url provided for one book.

def detail_book_list(url):

    response = requests.get(url) # variable response
    soup_book = BeautifulSoup (response.content,"html.parser") #create the soup object
    detail_book_list = [] #creating a list named: detail_book_list
    title_book = soup_book.title.text.replace("\n","")[4:].replace(" | Books to Scrape - Sandbox","") #cleaning: since it is a character string, we only keep the elements from index 4 until the end
    detail_book = soup_book.find("table",{"class":"table table-striped"}).find_all('td') #inspection to find the details of the book
    
    num_available_text = detail_book[5].text #index 5 of the detail_book list
    num_available_ok = (re.findall("\d+", num_available_text))  # to recover ONLY the digits of the string number_available_string
    
    url_site = "https://books.toscrape.com/"
    image_url_research = soup_book.find('div', {'class': 'carousel-inner'}).find('div', {'class': 'item active'}).find('img').attrs['src'] #with .attrs['src'] to retrieve the link
    image_url = url_site+image_url_research.replace("../","") #concatenation + cleaning
    product_description = soup_book.find('h2').find_next("p").get_text() #to find the product description
    categorie = soup_book.find('div', {'class': 'container-fluid page'}).find('div', {'class': 'page_inner'}).find('ul', {'class': 'breadcrumb'}).find('li', {'class': 'active'}).find_previous('li').get_text().replace("\n","")  #to find the categories
    price_i_tax = detail_book[3].text.replace("£","") #index 3 of the detail_book list
    price_ex_tax = detail_book[2].text.replace("£","")  #index 2 of the detail_book list
    num_available = num_available_ok[0] #index 0 of num_available_ok
    review_rating = soup_book.find('div', {'id': 'content_inner'}).find('div', {'class': 'row'}).find('div', {'col-sm-6 product_main'}).find('p', {'class': 'instock availability'}).find_next('p') ['class'][1] #to find the review rating
    upc = detail_book[0].text #index 0 of the detail_book list
    product_page_url = url # here the link of product page url is the same of the url

  
    detail_book_list.append(product_page_url) #add of the details to the detail_book_list in the order we want
    detail_book_list.append(upc)
    detail_book_list.append(title_book)
    detail_book_list.append(price_i_tax)
    detail_book_list.append(price_ex_tax)
    detail_book_list.append(num_available)
    detail_book_list.append(product_description)
    detail_book_list.append(categorie)
    detail_book_list.append(review_rating)
    detail_book_list.append(image_url)

    

    return detail_book_list











#definition of a function that retrieves the name and the link of all categories from the site url
def all_categories(url):
    all_categories_list = [] #creating a list named: all_categories_list
    page = requests.get(url) # variable page
    soup = BeautifulSoup (page.content,'html.parser') #create the soup object
    categories = soup.find('div', {'class': 'side_categories'}).find('ul',{'class': ''}).find_all('a') #to find the categories

    for element in categories: #creating a for loop
        link_categorie = url+element['href'] # concatenation: url + retrieval of the element's href/link
        nom_categorie = element.text.replace(' ','').replace('\n','') # text + cleaning
        all_categories_list.append([nom_categorie, link_categorie])
        
    return all_categories_list






#definition of a function which displays ONLY the links of each categories
def all_url_categories(url):
    all_categories_list = [] #creating a list named: all_categories_list
    page = requests.get(url) #page variable
    soup = BeautifulSoup (page.content,'html.parser') #create the soup object
    categories = soup.find('div', {'class': 'side_categories'}).find('ul',{'class': ''}).find_all('a') #to find the categories emplacement

    for element in categories: #creating a for loop
        link_categorie = url+element['href'] # url + retrieval of the element's href/link
        nom_categorie = element.text.replace(' ','').replace('\n','') #texte and cleaning
        
    return all_categories_list

'''
CORRECTION DE LA FONCTION " def all_url_categories(url): " POUR QUE CELLE CI NE RETOURNE UNIQUEMENT QUE LES LIENS DES DIFFERENTES CATEGORIES
VOIR AVEC MAME SI OK 
(LE CODE COMMENTÉ CI DESSOUS À ÉTÉ TESTER SUR UN NOTEBOOK ET FONCTIONNE)

#definition of a function which displays ONLY the links of each categories
def all_url_categories(url):
    link_categories_list = [] #creating a list named: all_categories_list
    page = requests.get(url) #page variable
    soup = BeautifulSoup (page.content,'html.parser') #create the soup object
    categories = soup.find('div', {'class': 'side_categories'}).find('ul',{'class': ''}).find_all('a') #to find the categories emplacement

    for element in categories: #creating a for loop
        link_categorie = url+element['href'] # url + retrieval of the element's href/link
        nom_categorie = element.text.replace(' ','').replace('\n','') #texte and cleaning
        link_categories_list.append([link_categorie])
        
    return link_categories_list

'''

















#definition of a function that will manage the pagination and return all the pages of the category from the category url.

def all_url_pages_categories(url_categ):
    
    url_books_list = []  #creating a list named: url_books_list
    r = requests.get(url_categ) # variable r response to requete
    i = 2 # creating a i variable which has the value 2 because the second page of the url categorie uses the number 2
    urls = url_categ # creating urls variable who has the same value of url_categ


    while r.ok: #creating a while loop which ensures that the r response is ok
        url_books_list.append(urls) #add of the urls to the url_books_list
        urls = url_categ.replace("index", "page-"+str(i)) #formatting the url variable
        i += 1 # add 1 each time the loop passes
        r = requests.get(urls) # urls query
        
    return url_books_list







# function that will return all the links of the books contained in a category (index page only)

def all_url_page_books_categ (url_page_categ):
    req = requests.get(url_page_categ) # variable response
    soup = BeautifulSoup (req.content,'html.parser') # create the soup object
    link_book_categ = soup.find('section').find_all('h3') # to find all the h3
    url = "https://books.toscrape.com/"
    
    liste_book_categ = [] #creating a list named: liste_book_categ
    for element in link_book_categ: #creating a for loop 
        url_book = url+"catalogue"+element.find('a')['href'].replace('../../..','') # concatenation: url + retrieval of the element's href/link + cleaning
        liste_book_categ.append(url_book) #add of the url_book to the liste_book_categ 

    return liste_book_categ
    
    
    
    

# definition of a function that returns all the links of the books contained in the pages of a category
# we provide the url of the index (first page of a category)
    
    
def all_url_books_categ(url_index_categ):
    all_url = all_url_pages_categories(url_index_categ) # variable than use all_url_pages_categories fonction 
    #(fonction that will manage the pagination and return all the pages of the category from the category url)with url_index_categ parameter
        
        
    all_list_book = [] #creating a list named: all_list_book
    for link_page in all_url:  #creating a for loop  ( for each link contained in the variable 
        #all_url(variable which contains the urls of all the pages of the category while managing the pagination))
        d = all_url_page_books_categ(link_page)  #creating a variable d using link_page parmater and run a function that will return all the links of the books contained in a category (index page only)
        for element in d: #creating a for loop
            all_list_book.append(element) #creating a list who add the elements
                
    return all_list_book
        
    
    
    
    
    
    
    
    

#definition of a dataframe with pandas which returns all the requested information in table form
    
df_detail_book = pd.DataFrame(columns=["Product page url","UPC","Title Book",
                                               "Prix incl. tax","Prix Excl. tax","Nb Available","Product Description","Catégorie","Review rating","Image url"])
    
    
    
    
    
    
    
    
    
    
    
def all_book_detail_categ(url_index_categ, df_detail_book):
    all_urls_books = all_url_books_categ(url_index_categ)  # using all_url_books_categ function that returns all the links of the books contained in the pages of a category
# we provide the url of the index (first page of a category)
    my_list = [] #creating a list named my_list
        
        
    for link_book in all_urls_books:
        detail_book = detail_book_list(link_book)
        df_detail_book.loc [len(df_detail_book)] = detail_book
            
    for i in df_detail_book.index:
         my_list.append([df_detail_book["Title Book"][i], df_detail_book['Image url'][i]])
                
            
    return df_detail_book, my_list







            
            
            
            
            
            
def save_img(book_title_url_list, path_local):
    
    for elt in book_title_url_list:
        
        response = requests.get(elt[1])
        
        title_mod = elt[0].replace(':', '_').replace('(', '').replace(')', '').replace(' ', '_').replace(
                '/', '_').replace('"', '').replace("'", "").replace('...', '').replace('&', '').replace('*', '').replace('?', '').replace('#', '')
        imagename = str(title_mod) + '.' + elt[1].split('.')[-1]

        file = open(path_local+imagename, "wb")

        
        file.write(response.content)
        file.close()










#good code



rep = os.getcwd()  #current working directory

chemin_sauvegarde = rep+"/DATATEST/"
#path_local = "D:\\hakim\\testimg\\"

if not os.path.exists(chemin_sauvegarde):
    os.makedirs(chemin_sauvegarde)



for url_categ in all_categories("https://books.toscrape.com/"):
    #print(url_categ[0])
    df_detail_book = pd.DataFrame(columns=["Product page url","UPC","Title Book",
                                               "Prix incl. tax","Prix Excl. tax","Nb Available","Product Description","Catégorie","Review rating","Image url"])
    df, list_img = all_book_detail_categ(url_categ[1], df_detail_book)
    #exporter le fichier .csv dans le repertoire data
    df.to_csv(chemin_sauvegarde+url_categ[0]+".csv")
    #enregistrer les images dans le repertoire data
    #save_img3(list_img, path_local)
    save_img(list_img, chemin_sauvegarde)









    
    
    
    
    
    