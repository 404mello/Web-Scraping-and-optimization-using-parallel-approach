#Python program to scrape website  
#and save quotes from website 
import time
a=time.time()
import requests 
import bs4
import csv 


def writeCsvFile(fname, data, *args, **kwargs):
    mycsv = csv.writer(open(fname, 'a', encoding='utf-8'), *args, **kwargs)
    for row in data:
        mycsv.writerow(row)



  
url = "http://quotes.toscrape.com/"

for i in range(1,11):
    info=[]
    data=()
    quotes=[]  #  list to store quotes 
    authors=[] #  list to store the corresponding authors
    theme=[]   #  list to store the theme associated with quote

    if i==1:
        url_new=url
    else:
        url_new=url+'page/'+str(i)
        
    print("Scraping data from link: ",url_new)
    r = requests.get(url_new)
    soup = bs4.BeautifulSoup(r.content, 'lxml')

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
        info=[quotes[i], authors[i], theme[i]]
        data=data+(info,)
    writeCsvFile('data_serial.csv', data)

    

b=time.time()

print("Web Scraping complete, time taken : ",(b-a),"seconds")

