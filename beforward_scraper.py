from datetime import datetime
import requests
import csv
import bs4

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
REQUEST_HEADER = {
  'user-agent': USER_AGENT,
  'Accept-Language': 'en-US, en; q=0.5'
}


def get_page_html(url):
    res = requests.get(url=url, headers=REQUEST_HEADER)
    return res._content

def get_car_price(soup):
      main_price_span = soup.find('span', attrs={
          'id':'fn-vehicle-price-total-price'
          })
      price = main_price_span.text.strip().replace(',','')
      try:
          return float(price)
      except ValueError:
          print("Value obtained can't be parsed")
          exit()

def get_car_title(soup):
    car_info_div = soup.find('div', attrs={
        'class':'car-info-flex-box'
    })
    if car_info_div:
        title = car_info_div.find('h1').text.strip()
        return title
    else:
        print('Elemento <h1> não encontrado dentro da div.')  

def get_manufacture_year(soup):
    car_manufacture_year = soup.find('div', attrs={
        'class':'pickup-specification'
    })
    car_year = car_manufacture_year.findAll('td', class_='pickup-specification-text')
    year = car_year[1].text.strip().split('/')[0]
    return year

def get_kilometers(soup):
    car_kilometers_info = soup.find('div', attrs={
        'class':'pickup-specification'
    })
    car_kilometers = car_kilometers_info.findAll('td', class_='pickup-specification-text')
    kilometers = car_kilometers[0].text.strip()
    return kilometers

def get_car_image(soup):
    car_image_info = soup.find('p', attrs={
        'id':'imgMain'
    })
    car_image_sale = car_image_info.find('a')
    car_image = car_image_sale['href']
    return car_image

def get_transmission_type(soup):
    car_info = soup.find('div', attrs={
        'class':'pickup-specification'
    })
    car_transmission_type_info = car_info.findAll('td', attrs={
        'class':'pickup-specification-text'
    })
    car_transmission_type = car_transmission_type_info[3].text.strip()
    return car_transmission_type

def get_fuel_type(soup):
    car_info = soup.find('div', attrs={
        'class':'pickup-specification'
    })
    car_fuel_type_info = car_info.findAll('td', attrs={
        'class':'pickup-specification-text'
    })
    fuel_type = car_fuel_type_info[4].text.strip()
    return fuel_type

def extract_car_info(url):
    car_info = {}
    print('Scraping URL: '+ url)
    html = get_page_html(url = url)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    car_info['price'] = get_car_price(soup)
    car_info['title'] = get_car_title(soup)
    car_info['year'] = get_manufacture_year(soup)
    car_info['kilometers'] = get_kilometers(soup)
    car_info['image'] = get_car_image(soup)
    car_info['transmission'] = get_transmission_type(soup)
    car_info['fuel'] = get_fuel_type(soup)
    return car_info
    


if __name__ == "__main__":
    with open('beforward_cars_urls.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            url = row[0]
            print(extract_car_info(url))    