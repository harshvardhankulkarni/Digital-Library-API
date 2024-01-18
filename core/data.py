import requests
from bs4 import BeautifulSoup


def scrape_countries():
    response = requests.get('https://www.britannica.com/topic/list-of-countries-1993160')

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        countries = []
        for i in range(6, 33):
            for country in soup.select(selector=f'.reading-channel #ref3268{str(i).zfill(2)} ul li'):
                countries.append(country.find('a', class_='md-crosslink').text.strip())
        return countries

    else:
        print(f"Error: Unable to retrieve the webpage. Status code: {response.status_code}")
        return None


def scrape_genra():
    response = requests.get('https://selfpublishing.com/list-of-book-genres/')

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        genra = []
        for country in soup.select(selector=f'.et_pb_post_content_0_tb_body h{3}'):
            genra.append(country.text.split('.')[1].strip())
        for country in soup.select(selector=f'.et_pb_post_content_0_tb_body h{4}'):
            genra.append(country.text.split('.')[1].strip())
        return list(set(genra))

    else:
        print(f"Error: Unable to retrieve the webpage. Status code: {response.status_code}")
        return None


def scrape_languages():
    response = requests.get('https://guidely.in/blog/languages-of-india')

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        languages = []
        for country in soup.select(selector=f'.maincontent ol span'):
            if len(languages) != 22:
                languages.append(country.text)
        return languages

    else:
        print(f"Error: Unable to retrieve the webpage. Status code: {response.status_code}")
        return None
