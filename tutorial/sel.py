import time
import pandas as pd
from selenium import webdriver

start = time.time()
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("./chromedriver",
                          chrome_options=options)
driver.get("https://www.brandstof-zoeker.nl/")


def options_scrape(id):
    options = []
    select = driver.find_element_by_xpath("//select[@id = '" + id + "']")
    select = select.find_elements_by_tag_name("option")
    for option in select:
        options.append(option.text)
    options.pop(0)
    return options


fuel = options_scrape("brandstofselect")
chain = options_scrape("ketenselect")

stations, fuels, prices, chains, addresses, times, gratises = [], [], [], [], [], [], []
for i in fuel:
    for j in chain:
        station, price, address, tim, gratis = [], [], [], [], []
        search_fuel = driver.find_element_by_id('brandstofselect')
        search_fuel.send_keys(i)
        search_fuel.click()
        search_chain = driver.find_element_by_id('ketenselect')
        search_chain.send_keys(j)
        search_chain.click()
        time.sleep(10)  # todo: its bad to put a fixed wait time, try wait until done loading
        results = driver.find_element_by_xpath("//div[@id = 'results']")
        selections = results.find_elements_by_tag_name("h2")
        selections_else = results.find_elements_by_tag_name("ul")
        for option in selections:
            try:
                station.append(option.text.split('\n')[1])
                price.append(option.text.split('\n')[0]),
            except IndexError:
                price.append(''),
                station.append(option.text)
        for option in selections_else:
            details = [d for d in option.text.split('\n') if d != '']
            time_price = details[1]
            address.append(details[0])
            if 'Geen prijs bekend' in time_price:
                tim.append('')
            else:
                tim.append(details[1].split(':')[0])
            if len(details) == 3:
                gratis.append(time_price.split(',')[1])
            else:
                gratis.append(details[2])

        try:
            assert len(station) == len(price) == len(tim) == len(gratis) == len(address)
            stations.extend(station)
            prices.extend(price)
            times.extend(tim)
            gratises.extend(gratis)
            addresses.extend(address)
            fuels.extend([i for x in range(len(station))])
            chains.extend([j for x in range(len(station))])
        except AssertionError:
            print('ASSERTION ERROR')
            print(len(stations), len(prices), len(times), len(gratis), len(address))

df = pd.DataFrame({'Fuel': fuels, 'Chain': chains, 'Station': stations, 'Address': addresses, 'Time': times,
                   'Price': prices, 'Gratis': gratises})
df.to_csv('./stations2.csv', index=False)

end = time.time()

print('Run time:', end - start)
