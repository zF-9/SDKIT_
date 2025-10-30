from bs4 import BeautifulSoup

soup = BeautifulSoup("<h1>Hello World!</h1>", "html.parser")

print(soup.get_text())