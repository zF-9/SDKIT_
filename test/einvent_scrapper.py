'''
    import pandas as pd
    URL = 'https://en.wikipedia.org/wiki/List_of_largest_banks'
    tables = pd.read_html(URL)
    df = tables[0]
    print(df)
'''
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

url = 'https://digitalisation.jpan.my/eInv/index.cfm?section=Transaction_ReassignStaff'
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')
mesa = soup.find('table')
#df = pd.read_html(StringIO(str(mesa)), displayed_only=False)
print(soup.get_text())

'''
header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

r = requests.get(url, headers=header)ghhfjghfjhgdjhdjfhgk

dfs = pd.read_html(r.text)
'''