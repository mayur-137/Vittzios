# Open and read the HTML file
with open('D:/DHRUV/pyrean/Vittzios/Vittzios/templates/main/verification.html', 'r') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_content, 'html.parser')

# Find the <h1> tag and extract the text from it
h1_tag = soup.find('h1')
site = h1_tag.text.strip()

# Now you can use the 'site' variable in Python as needed
print("Site:", site)
