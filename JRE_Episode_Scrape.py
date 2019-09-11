#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 17:12:21 2019

@author: Tim_Smaluk
"""
from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib.parse
import re

guests = []
urls = []
full_list = []
list_of_books = []
episode_number_guest = []

def url_connection(url):
    """
    Creates a soup object to represent the url html
    :@return(string): returns the html for a given url
    """
    url = requests.get(url)
    soup = BeautifulSoup(url.text, 'lxml')
    return soup

def scrape_names(soup):
    """
    Returns names of each guest
    :@return (list): list of names
    """

    a = soup.find_all('a')
    for names in a:
        r = re.search(r"#.+", names.text)
        if r is not None:
            guests.append(r.group(0))
    for links in a:
        urls.append(links['href'])
    
    return guests, urls

def hasNumbers(inputString):
    """
    Checks to see if a string contains numbers. Credit to theFourtheye on Stack 
    :@return(bool): returns True/False if str contains numbers
    """
    return bool(re.search(r'\d', inputString))

def cleanup_links(links):
    """
    Removes unnecesary urls 
    :@return(list): list of cleaned urls
    """

    for path in links:
        if hasNumbers(path) is True and not "onnit" in path:
            full_list.append(urllib.parse.urljoin('https://jrelibrary.com', 
            path))
    return full_list
  
def scrape_books(url_list):
    """
    Returns list of tuples of books mentioned and guest who mentioned it
    :@return(list):list of tuples (book,author) 
    """
    for url in url_list:
        result = url_connection(url) #prints the first link for testing
        x = result.find_all("h3", {"class" : "book-title"})
        for a in x:
            list_of_books.append(tuple((a.text).replace('\n', '').rsplit('by ', 1)
            ))
    return list_of_books


def exporting_to_csv(names, books):
    """
    Creates a csv file from a Pandas Data Frame
    :@return(file): csv file containing  Episode #, Name of Guest,Books, Author
    """
    try:
        for name in names:
            guest = tuple(name.split(' – ', 1))
            episode_number_guest.append(guest)
    except IndexError:
        print(str(name))
        pass    
    
    df1 = pd.DataFrame(episode_number_guest, columns= ['Epsiode #', 'Name of Guest'])
    df2 = pd.DataFrame(books, columns = ['Book Title', 'Book Author'])
    return df1.to_csv(r'/Users/Tim_Smaluk/Desktop/JRE-Analysis/out2.csv',index=False, encoding='utf-8')
    #return df2.to_csv(r'/Users/Tim_Smaluk/Desktop/JRE-Analysis/out2.csv',index=False, encoding='utf-8')

def main():  
    seed = 'https://jrelibrary.com/episode-list/'
    soup = url_connection(seed)
    names, links = scrape_names(soup)
    url_list = cleanup_links(links)
    books = scrape_books(url_list)
    exporting_to_csv(names, books)


if __name__ == "__main__":
     main()
