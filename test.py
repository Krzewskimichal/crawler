import crawler
import time
import csv
import pandas

#  tests
start = time.time()

urls_list = []
urls_list.append("https://e-katalog.intercars.com.pl/#/ekatalog/osobowe/towary/2134/101000000/")
urls_list.append("https://e-katalog.intercars.com.pl/#/ekatalog/osobowe/towary/2134/1401000000/")
urls_list.append("https://e-katalog.intercars.com.pl/#/ekatalog/osobowe/towary/33341/102000000/")
products = crawler.find_goods(urls_list)

#  lists of name, price, quantity
name = products[0]
price = products[1]
quantity = products[2]
brand = products[3]
model = products[4]

#  storing data into products.csv file
dictionary = {"name": name, "price": price, "quantity": quantity, "brand": brand, "model": model}

data = pandas.DataFrame(dictionary)

data.to_csv("products.csv")

end = time.time() - start
print(f"time: {end}")
