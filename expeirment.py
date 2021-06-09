from bs4 import BeautifulSoup
from urllib.request import urlopen

link = "https://rhul.buggyrace.net/specs/"

page = urlopen(link)

html_page = page.read().decode("utf-8")
content = BeautifulSoup(html_page,"html.parser")


table = content.find('table', {'class': "table table-striped table-bordered table-hover})
rows = table.find_all('tr')
costs = []
for row in rows:
    cells = row.find_all('td')
    for cell in cells:
        costs.append(cell.get_text().strip(" \n ").strip())
print(costs)





    #if len(cells) > 1:
        #country_link = cells[1].find('a')
        #print(country_link.get('href'))