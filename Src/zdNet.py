from bs4 import BeautifulSoup
import requests

header = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}

url = "https://www.zdnet.com/home-and-office/smart-home/eufy-edge-security-system-hands-on/"


def scrapeZDNet(url):
    html_text = requests.get(url, headers=header).text
    soup = BeautifulSoup(html_text, "lxml")
    dic = {}
    dic["first paragraph"] = soup.find("div",
                                       class_="c-contentHeader_description g-outer-spacing-top-medium g-outer-spacing-bottom-medium").text.strip()

    textContainer = soup.find("div", class_="c-ShortcodeContent")
    pArray = textContainer.find_all("p")
    rawText = " ".join(list(map(lambda val : val.text, pArray)))
    dic["raw text"] = rawText
    return dic

# Uncomment the following line to test the scraper
# print(scrapeZDNet(url))