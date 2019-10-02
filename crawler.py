from selenium import webdriver

import time
from bs4 import BeautifulSoup
import requests
import os


class Crawler:

    def __init__(self):
        self.url = "https://e-katalog.intercars.com.pl"
        self.driver = webdriver.Firefox()
        self.driver.get(self.url)

    #  method finds link to sith with products
    def find_oferta_ic(self):

        """
        finds category links element
        :return: list of ekatalog/category
        """
        link = self.driver.find_element_by_xpath('//a[@href="/oferta/"]')
        link = link.get_attribute('href')

        return link

    def find_products(self, url):

        """
        finds products by searching navigations side bar
        :param url: link to site with offer
        :return:we will see
        """

        #  find first level links of navigation tree
        self.driver.get(url)
        dTree = self.driver.find_elements_by_xpath('//div[@id="content"]/div/div[@id="dTree"]/a')

        #  lists of links /first_level/second_level/third_level/fourth_level if exists
        first_links = []
        second_links = []
        third_links = []

        #  find second level links of navigation tree
        for link in dTree:
            link = link.get_attribute("href")
            first_links.append(link)

        for link in first_links:
            self.driver.get(link)
            subtreeroot = self.driver.find_elements_by_xpath('//div[@class="subTreeRoot"]/a')

            for second_link in subtreeroot:
                second_links.append(second_link.get_attribute('href'))

        for scond_link in second_links:
            self.driver.get(scond_link)
            li0 = self.driver.find_elements_by_xpath('//li[@id="li0"]/a')

            for third_link in li0:
                third_links.append(third_link)

        return third_links

    def catalog(self):

        """
        finds products in cars catalog
        :return: products store in database
        """

        print(self.url)


    def find_brand(self, url):

        """
        :param url: list of links ekatalog/category
        :return: list of links /ekatalog/category/brand
        """

        links = []
        for element in url:

            options = webdriver.FirefoxOptions()
            options.add_argument('-headless')
            cwd = os.getcwd()
            path = f"{cwd}/geckodriver"
            driver = webdriver.Firefox(executable_path=path, firefox_options=options)

            driver.get(element)

            content = driver.page_source.encode("utf-8").strip()
            soup = BeautifulSoup(content, "lxml")
            kontener_marka = soup.find("div", {"id": "kontener_marka"})

            a = kontener_marka.find_all("a")

            for link in a:
                link = link["href"]
                links.append(f"https://e-katalog.intercars.com.pl{link}")

        return links


    def find_model(self):

        """
        :param url: list of /ekatalog/category/brand/
        :return: list of links /ekatalog/category/brand/model
        """
        links = []
        for element in url:

            options = webdriver.FirefoxOptions()
            options.add_argument('-headless')
            cwd = os.getcwd()
            path = f"{cwd}/geckodriver"
            driver = webdriver.Firefox(executable_path=path, firefox_options=options)

            driver.get(element)

            content = driver.page_source.encode("utf-8").strip()
            soup = BeautifulSoup(content, "lxml")

            kontener_model = soup.find("div", {"id": "kontener_model"})
            links = []
            for a in kontener_model.find_all("li", {"class": "width40 vtop mod"}):
                link = a.find("a")
                link = link["href"]
                links.append(f"https://e-katalog.intercars.com.pl{link}")

        return links


    def find_type(self):

        """
        :param url: list of links /ekatalog/category/brand/model
        :return: list of links /ekatalog/category/brand/model/type/number
        """
        links = []
        for element in url:

            options = webdriver.FirefoxOptions()
            options.add_argument('-headless')
            cwd = os.getcwd()
            path = f"{cwd}/geckodriver"
            driver = webdriver.Firefox(executable_path=path, firefox_options=options)

            adress = element
            driver.get(adress)

            content = driver.page_source.encode("utf-8").strip()
            soup = BeautifulSoup(content, "lxml")
            kontener_type = soup.find("div", {"id": "kontener_typ"})
            li = kontener_type.find_all("li", {"class": "width30 tKod vmiddle typli"})

            for a in li:
                a = a.find("a")
                links.append(a["href"])

        return links


    def find_group(self):

        """
        :param url: list of links /ekatalog/category/brand/model/type/number
        :return: list of links /ekatalog/category/group/35009
        """
        links = []
        for element in url:

            options = webdriver.FirefoxOptions()
            options.add_argument('-headless')
            cwd = os.getcwd()
            path = f"{cwd}/geckodriver"
            driver = webdriver.Firefox(executable_path=path, firefox_options=options)

            driver.get(element)

            content = driver.page_source.encode("utf-8").strip()
            soup = BeautifulSoup(content, "lxml")

            ul = soup.find("ul", {"id": {"TecDoc-tree-grp"}})
            a = ul.find_all("a")

            #  not every <a> tag contains href attribute
            for link in a:
                try:
                    links.append(link["href"])
                except KeyError:
                    pass

        return links


    def find_goods(self):

        """
        :param url: list of links /ekatalog/category/goods/number/number/"
        :return: store information in products.csv file
        """

        #  name of products
        name = []
        #  price of products
        price = []
        #  quantity of products
        quantity = []
        #  name of brand
        brand = []
        #  name of model
        model = []

        for adress in url:

            options = webdriver.FirefoxOptions()
            options.add_argument('-headless')
            cwd = os.getcwd()
            path = f"{cwd}/geckodriver"
            driver = webdriver.Firefox(executable_path=path, firefox_options=options)

            driver.get(adress)
            content = driver.page_source.encode("utf-8").strip()
            soup = BeautifulSoup(content, "lxml")

            ul = soup.find_all("ul", {"class": "tecdocProList"})

            #  for each element of ul scrap info about product
            for element in ul:

                n = element.find("li", {"class": "tecdocCol tecdocCol2"})
                #  check if element is active
                if n.find("a", {"class": "ajax"}) is not None:
                    n = n.find("span", {"class": "tecdocIndex"})
                    n = n.text
                    name.append(n)

                    #  adding name of brand and model
                    b = soup.find("nav", {"class": "KatTcDcBreadCrumbs"})
                    b = b.find_all("span", {"itemprop": "title"})

                    brand_name = b[1]
                    brand_name = brand_name.text
                    brand.append(brand_name)

                    model_name = b[2]
                    model_name = model_name.text
                    model.append(model_name)
                else:
                    pass

                try:
                    p = element.find("li", {"class": "tecdocCol tecdocCol4"})
                    p = p.find("span", {"class": "tecdocCena"})
                    p = p.text
                    price.append(p)
                except AttributeError:
                    pass

                try:
                    q = element.find("li", {"class": "tecdocCol tecdocCol5"})
                    q = q.find("span", {"class": "tecdocStany"})
                    q = q.text
                    quantity.append(q)
                except AttributeError:
                    pass

        return name, price, quantity, brand, model


site = Crawler()
# oferta_ic = site.find_oferta_ic()
# print(oferta_ic)
# for i in site.find_products(oferta_ic):
#     print(i)
