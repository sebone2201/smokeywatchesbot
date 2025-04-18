import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
#import undetected_chromedriver.v2 as uc
#import time




#!/usr/bin/env python3.7


#import requests
#from bs4 import BeautifulSoup, Tag

import os
import platform
import requests
import re
 
from datetime import datetime, time
import time as t
#chat_id_list = []
querie_list = []

#queries = dict()
#apiCredentials = dict()
BotapiCredentials = "7742626687:AAE5dylLVxBxI54qx_M4dbbjQko8Za5zmwk"
#dbFile = "searches.tracked"
#telegramApiFile = "telegram_api_credentials"

#database part
#DB_NAME= "smokey_watches"

DB_NAME = "smokeywatches.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Table for queries
    c.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            name TEXT ,
            url TEXT,
            min_price TEXT,
            max_price TEXT,
            link TEXT PRIMARY KEY,
            title TEXT,
            price TEXT,
            location TEXT,
            chatid  TEXT
        )
    ''')



    conn.commit()
    conn.close()


def save_result(name, url, minP, maxP, link, title, price, location, chatid):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT OR IGNORE INTO queries (name, url, min_price, max_price, link, title, price, location, chatid)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, url, minP, maxP, link, title, str(price), location, chatid))
    conn.commit()
    conn.close()

def is_result_saved(link):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT link FROM (
            SELECT link FROM queries
            ORDER BY ROWID DESC
            LIMIT 100
        ) WHERE link = ?
    ''', (link,))
    result = c.fetchone()
    conn.close()
    return result is not None



    ######à



# Windows notifications
if platform.system() == "Windows":
    from win10toast import ToastNotifier
    toaster = ToastNotifier()

#open the web driver

# load from file





def print_queries():
    '''A function to print the queries'''
    global queries
    #print(queries, "\n\n")

    for search in queries.items():
        print("\nsearch: ", search[0])
        for query_url in search[1]:
            print("query url:", query_url)
            for url in search[1].items():
                for minP in url[1].items():
                    for maxP in minP[1].items():
                        for result in maxP[1].items():
                            print("\n", result[1].get('title'), ":", result[1].get('price'), "-->", result[1].get('location'))
                            print(" ", result[0])


# printing a compact list of trackings
def print_sitrep():
    '''A function to print a compact list of trackings'''
    global queries
    i = 1
    for search in queries.items():
        print('\n{}) search: {}'.format(i, search[0]))
        for query_url in search[1].items():
            for minP in query_url[1].items():
                for maxP in minP[1].items():
                    print("query url:", query_url[0], " ", end='')
                    if minP[0] !="null":
                        print(minP[0],"<", end='')
                    if minP[0] !="null" or maxP[0] !="null":
                        print(" price ", end='')
                    if maxP[0] !="null":
                        print("<", maxP[0], end='')
                    print("\n")

        i+=1

def refresh(notify):
    '''A function to refresh the queries

    Arguments
    ---------
    notify: bool
        whether to send notifications or not

    Example usage
    -------------
    >>> refresh(True)   # Refresh queries and send notifications
    >>> refresh(False)  # Refresh queries and don't send notifications
    '''
    global querie_list
    driver.refresh()
    #global queries
    try:
        for search in querie_list:
            
            run_query(search[0], search[1], notify, search[2], search[3], search[4])
    except requests.exceptions.ConnectionError:
        print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " ***Connection error***")
    except requests.exceptions.Timeout:
        print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " ***Server timeout error***")
    except requests.exceptions.HTTPError:
        print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " ***HTTP error***")
    except Exception as e:
        print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S")) #+ " " + e)  


def delete(toDelete):
    '''A function to delete a query

    Arguments
    ---------
    toDelete: str
        the query to delete

    Example usage
    -------------
    >>> delete("query")
    '''
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM queries WHERE name = ?", (toDelete))

def add(url, name, minPrice, maxPrice, chatid):
    ''' A function to add a new query

    Arguments
    ---------
    url: str
        the url to run the query on
    name: str
        the name of the query
    minPrice: str
        the minimum price to search for
    maxPrice: str
        the maximum price to search for

    Example usage
    -------------
    >>> add("https://www.subito.it/annunci-italia/vendita/usato/?q=auto", "auto", 100, "null")
    '''
    global querie_list

    # If the query has already been added previously, delete it
    querie_list.append([ f"{url}",f"{name}", f"{minPrice}", f"{maxPrice}", f"{chatid}"])




def run_query(url, name, notify, minPrice, maxPrice, chatid):
        '''Run a query using Selenium (bypasses anti-bot protections)'''
        print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + f" running query (\"{name}\" - {url})...")

        #global queries
        products_deleted = False
        msg = []

    # Set up Chrome in headless mode
    

    
        driver.get(url)
        t.sleep(3)  # Wait for JS to load the content

        products = driver.find_elements(By.CSS_SELECTOR, "div.item-card")

        for product in products:
        
                title_el = product.find_element(By.CSS_SELECTOR, "h2")
                title = title_el.get_attribute("innerHTML")

                link_el = product.find_element(By.CSS_SELECTOR, "a")
                link = link_el.get_attribute("href")

                try:
                    price_el = product.find_element(By.CSS_SELECTOR, "p[class*='price']")
                    price_text = driver.execute_script("return arguments[0].childNodes[0].textContent;", price_el).strip()
                    price =  int(price_text.replace('.','')[:-2])
                except:
                    price = "Unknown price"

                try:
                    town_el = product.find_element(By.CSS_SELECTOR, "span[class*='town']")
                    city_el = product.find_element(By.CSS_SELECTOR, "span[class*='city']")

                    location = town_el.get_attribute("innerHTML") + city_el.get_attribute("innerHTML")
                    #print(location)
                except:
                    location = "Unknown location"

                sold = None
                try:
                    sold_el = product.find_element(By.CSS_SELECTOR, "span[class*='item-sold-badge']")
                    sold = sold_el.get_attribute("innerHTML")
                except:
                    pass

                
                    

                if minPrice == "null" or price == "Unknown price" or price >= int(minPrice):
                    if maxPrice == "null" or price == "Unknown price" or price <= int(maxPrice):
                        if name.lower() not in title.lower():
                           continue  # skip this product
                        if not is_result_saved(link):
                            tmp = (
                                datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + "\n"
                                + str(price) + "\n"
                                + title + "\n"
                                + location + "\n"
                                + link + '\n'
                            )
                            msg.append(tmp)
                            save_result(name, url, minPrice, maxPrice, link, title, price, location, chatid)
                            #queries[name][url][minPrice][maxPrice][link] = {
                            #    'title': title,
                            #    'price': price,
                            #    'location': location
                            #}
                            print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " Adding result:", title, "-", price, "-", location)

        if len(msg) > 0:
            if notify:
                if not win_notifyoff and platform.system() == "Windows":
                    global toaster
                    toaster.show_toast("New announcements", "Query: " + name)
                
                send_telegram_messages(msg, chatid)
                print("\n".join(msg))
                print(f"\n{len(msg)} new elements have been found.")
            #save_queries()
        else:
            print('\nAll lists are already up to date.')

        #if products_deleted:
       #     save_queries()
    






def send_telegram_messages(messages, chatid):
    '''A function to send messages to telegram

    Arguments
    ---------
    messages: list
        the list of messages to send

    Example usage
    -------------
    >>> send_telegram_messages(["message1", "message2"])
    '''
    for msg in messages:
        request_url = "https://api.telegram.org/bot" + BotapiCredentials + "/sendMessage?chat_id=" + chatid + "&text=" + msg
        requests.get(request_url)

def in_between(now, start, end):
    '''A function to check if a time is in between two other times

    Arguments
    ---------
    now: datetime
        the time to check
    start: datetime
        the start time
    end: datetime
        the end time

    Example usage
    -------------
    >>> in_between(datetime.now(), datetime(2021, 5, 20, 0, 0, 0), datetime(2021, 5, 20, 23, 59, 59))
    '''
    if start < end:
        return start <= now < end
    elif start == end:
	    return True
    else: # over midnight e.g., 23:30-04:15
        return start <= now or now < end

def main():
  try:
    ### Setup commands ###
    global win_notifyoff
    global driver
    win_notifyoff = True


    chrome_options = Options()
    #options = uc.ChromeOptions()
    #options.headless = True
    #options.add_argument("--no sandbox")
    #options.add_argument("--disable-dev-shm-usage")
    
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.binary_location = "/usr/bin/chromium"  # molto importante
    chrome_options.add_argument("--no-sandbox")
    #chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/chromium"
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    init_db()#start database
    global querie_list
    

    querie_list.append(["https://www.subito.it/annunci-italia/vendita/abbigliamento-accessori/orologi-e-gioielli/?q=longiness&shp=true&order=datedesc", "Longiness", "50", "2000","-1002530005192" ])
    querie_list.append(["https://www.subito.it/annunci-italia/vendita/abbigliamento-accessori/?q=Omega&shp=true&order=datedesc", "Omega", "10", "3000","-1002413715692" ])
    querie_list.append(["https://www.subito.it/annunci-italia/vendita/abbigliamento-accessori/orologi-e-gioielli/?q=Cartier&shp=true&order=datedesc", "Cartier", "10", "3000","-1002562562736" ])
    querie_list.append(["https://www.subito.it/annunci-italia/vendita/abbigliamento-accessori/orologi-e-gioielli/?q=Zenith&shp=true&order=datedesc", "Zenith", "10", "3000","-1002530445224" ])
    
    for queries in querie_list:
      run_query(queries[0], queries[1], False, queries[2] if queries[2] is not None else "null", queries[3] if queries[3] is not None else "null", queries[4])
      print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " Query added.")

    #if args.delete is not None:
        #delete(args.delete)

    #if args.activeHour is None:
    activeHour="0"
    delay = "120"

    
    pauseHour="0"

    # Telegram setup

    
    ### Run commands ###

    

    
    


    
    notify = False # Don't flood with notifications the first time
    while True:
            if in_between(datetime.now().time(), time(int(activeHour)), time(int(pauseHour))):
                refresh(notify)
                notify = True
                print()
                print(str(delay) + " seconds to next poll.")
                #save_queries()
            t.sleep(int(delay))
  except KeyboardInterrupt:
        
        print("Stopping bot...")
  finally:
        driver.quit()







