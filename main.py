import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import sqlite3

class theVergeArticles:

    def convertArrayToCsv(self, pageData, linkData, authorData, headlineData, dateData):
        for i in range(len(linkData)):
            tempObj = []
            tempObj.append(str(linkData[i]))
            tempObj.append(str(authorData[i]))
            tempObj.append(str(headlineData[i]))
            tempObj.append(str(dateData[i]))
            pageData.append(tempObj)
        fields = ['Links', 'Author', 'Headline', 'Date']
        csvLocation = str(datetime.today().strftime('%d%m%Y_verge.csv'))
        with open(csvLocation, 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(fields)
            csv_writer.writerows(pageData)

    def getPageInfo(self, linkData, authorData, headlineData, dateData):

        # Website url
        url = "https://www.theverge.com"

        # Fetch html from website
        r = requests.get(url)
        htmlContent = r.content
        soup = BeautifulSoup(htmlContent, 'lxml')

        # print(soup.prettify())

        # Get all anchor tags
        links = soup.find_all('a')

        for data in links:
            flag = False
            classes = data.get('class')
            if classes != None:
                for classMatching in classes:
                    if flag == True: 
                        break
                    if ( (classMatching.find('group-hover:shadow-underline-franklin') 
                        or classMatching.find('group-hover:shadow-highlight-blurple')) 
                        and data.get('aria-label') != 'advertisement' 
                        and data.get('rel') == None
                        and data.get('href') != ('#content')
                        and data.get('href') != ('/')
                        and data.get('href').find('http') == -1
                        and (data.get_text() != '' and len(data.get_text()) > 15)
                        and data.get('href').find('/author') == -1 ):

                        linkData.append(url + data.get('href'))
                        headlineData.append(data.get_text())
                        flag = True

            if data.get('href').find('author') == 1:
                authorData.append(data.get_text())

        # for date of article
        dates = soup.find_all('span')
        for date in dates:
            data = date.get('class')

            if data != None:
                flag = False
                for dateCheck in data:
                    if flag == True:
                        break
                    if dateCheck.find('dark:text-gray-94') != -1:
                        dateNumber = date.get_text()
                        if dateNumber.find('UTC') != -1 or dateNumber.find('ago') != -1:
                            dateData.append(str(datetime.today().strftime('%d/%m/%Y')))
                        else:
                            tempMonth = date.get_text().split()
                            month = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07',
                                    'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', "Dec": '12'}
                            formatDate = str(tempMonth[1]) + '/' + str(month[tempMonth[0]]) + '/' + str(datetime.today().year)
                            dateData.append(formatDate)
                        flag = True
    
    def makeSqliteDb(self):
        conn = sqlite3.connect('Data.db')

        cur = conn.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            Link TEXT,
            Author TEXT,
            Headline TEXT,
            Date TEXT
        )""")

        csvLocation = str(datetime.today().strftime('%d%m%Y_verge.csv'))

        with open(csvLocation, 'r') as file:
            csvreader = csv.reader(file)
            insertRecords = "INSERT INTO articles (Link, Author, Headline, Date) VALUES(?, ?, ?, ?)"
            cur.executemany(insertRecords, csvreader)

        # cur.execute("""DROP TABLE articles""")


        conn.commit()

        conn.close()


def main():
    pageData = []
    linkData = []
    authorData = []
    headlineData = []
    dateData = []
    obj = theVergeArticles()
    obj.getPageInfo(linkData, authorData, headlineData, dateData)
    obj.convertArrayToCsv(pageData, linkData, authorData, headlineData, dateData)
    obj.makeSqliteDb()

if __name__ == '__main__':
    main()

