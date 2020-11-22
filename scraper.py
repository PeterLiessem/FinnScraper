#!/usr/local/bin/python3
import bs4 as bs
import platform
import urllib.request
import sys
from tqdm import tqdm
import matplotlib.pyplot as plt


class FinnS:  # Static variables
    link = 'https://www.finn.no/job/fulltime/search.html?filters=&occupation=0.23&page='
    page = 1
    source = urllib.request.urlopen(link+str(page)).read()
    soup = bs.BeautifulSoup(source, 'lxml')
    count = 0
    wordCount = [('java', 0), ('net', 0), ('python', 0), ('xml', 0),
                 ('jpa', 0), ('react', 0), ('node', 0), ('nodejs', 0), ('fullstack', 0), ('mongodb', 0), ('haskell', 0), ('go', 0), ('shell', 0)]


def mainLoop():
    sys.stdout.flush()
    while(True):
        articles = findArticles()
        tqdmBar = tqdm(articles, desc="page " + str(FinnS.page))
        # Fetch text and count words.
        for (name, alink) in tqdmBar:
            finn = ''
            if alink[0] != 'h':
                finn = 'https://www.finn.no'
            words = scrapePage(finn +
                               alink).lower().replace('\"', ' ').replace(',', ' ').replace('.', ' ').replace(':', ' ').replace(';', ' ').replace('!', ' ').replace('?', ' ').split()
            updateWords(words)
            # Can put 'break' to only load first article.TODO
        # break if there are no more pages; if not update page.
        # Can put 'or True' to only load first page. TODO
        if(not nextPage()):
            break

        # Update Link
        FinnS.source = urllib.request.urlopen(
            FinnS.link+str(FinnS.page)).read()
        FinnS.soup = bs.BeautifulSoup(FinnS.source, 'lxml')

    print('-----------------------------------------\n')
    showResult()


def nextPage():  # update to next page :: boolean
    for a in FinnS.soup.find('div', class_='u-hide-lt768').find_all('a'):
        if a.get('aria-current') != "page" and int(a.text) > FinnS.page:
            FinnS.page = int(a.text)
            return True
    return False


def findArticles():  # :: (Article-name, link)
    tuples = []
    for article in FinnS.soup.find_all('article'):
        a = article.find('div', class_="ads__unit__content").h2.a
        FinnS.count += 1
        text = a.text
        href = a.get('href')
        tuples.append((text, href))
    return tuples


def scrapePage(sLink):  # :: All relevant text from page.
    source = urllib.request.urlopen(sLink).read()
    soup = bs.BeautifulSoup(source, 'lxml').find('div', class_="u-word-break")
    text = ""
    for p in soup.find_all('p'):
        text += p.text + ' '
    for dt in soup.find_all('dt'):
        text += dt.text + ' '
    for dd in soup.find_all('dd'):
        text += dd.text + ' '
    for h1 in soup.find_all('h1'):
        text += h1.text + ' '
    for h2 in soup.find_all('h2'):
        text += h2.text + ' '
    for b in soup.find_all('b'):
        text += b.text + ' '
    return text


def updateWords(words):  # Updates the word counters
    for i in range(len(FinnS.wordCount)):
        for word in words:
            if(word == FinnS.wordCount[i][0]):
                FinnS.wordCount[i] = (
                    FinnS.wordCount[i][0], FinnS.wordCount[i][1]+1)
                break


def showResult():  # Shows the result in barPlot
    sortResult()
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    langs = [x[0] for x in FinnS.wordCount]
    words = [x[1] for x in FinnS.wordCount]
    ax.bar(langs, words)
    plt.show()


def sortResult():
    WordC = []
    for i in range(len(FinnS.wordCount)):
        smallest = i
        for j in range(i, len(FinnS.wordCount)):
            if FinnS.wordCount[smallest][1] < FinnS.wordCount[j][1]:
                smallest = j
        temp = FinnS.wordCount[i]
        FinnS.wordCount[i] = FinnS.wordCount[smallest]
        FinnS.wordCount[smallest] = temp
    print(FinnS.wordCount)


mainLoop()
