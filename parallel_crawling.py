#Python program to scrape website  
#and save quotes from website 
import requests 
from bs4 import BeautifulSoup 
import csv 
import time
from multiprocessing import Pool

quotes=[]  # a list to store quotes 
authors=[] # a list to store the corresponding authors
theme=[] # a list to store the theme associated with quote

#Generating Links and storing them in a list to parallely process them

def generatelinks():
    url = "http://quotes.toscrape.com/"
    url_list=[url]
    for i in range(2,11):
        url_new=url+'page/'+str(i)
        url_list.append(url_new)
    return url_list
    
def writeCsvFile(fname, data, *args, **kwargs):
    mycsv = csv.writer(open(fname, 'a', encoding='utf-8'), *args, **kwargs)
    for row in data:
        mycsv.writerow(row)


def parse(url_new):
    data=()
    info=[]
    
    quotes=[]
    authors=[]
    theme=[]
                
    print("Scraping data from link: ",url_new)
    r = requests.get(url_new)
    soup = BeautifulSoup(r.content, 'lxml')

    #Storing the Quotes
    quotes_list = soup.find_all('span', attrs = {'class':'text'})
    for each_quote in quotes_list:
        quotes.append(each_quote.string)
    

    #Storing the authors of the quotes
    authors_list= soup.find_all('small', attrs={'class': 'author'})
    for each_author in authors_list:
        authors.append(each_author.string)

    titles_list=soup.find_all("meta", class_="keywords")
    #Extracting each content
    for title in titles_list:
        theme.append(title["content"])

    for i in range(len(quotes)):
        info=[quotes[i],authors[i],theme[i]]
        data=data+(info,)
    writeCsvFile('data_parallel.csv', data)





def run():
    a=time.time()
    with Pool(10) as p:
        p.map(parse, generatelinks())
    b=time.time()
    
    
    print("Web Scraping complete, time taken : ",(b-a),"seconds")
        
    


