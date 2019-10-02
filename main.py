import crawler
import csv
import pandas

#  list of all links to find products
categories_links = crawler.find_categories()
brand_links = crawler.find_brand(categories_links)
model_links = crawler.find_model(brand_links)
type_links = crawler.find_type(model_links)
group_links = crawler.find_group(type_links)
products = crawler.find_goods(group_links)

#  lists of name, price, quantity, brand, model
name = products[0]
price = products[1]
quantity = products[2]
brand = products[3]
model = products[4]

#  storing data into products.csv file
dictionary = {"name": name, "price": price, "quantity": quantity, "brand": brand, "model": model}

data = pandas.DataFrame(dictionary)

data.to_csv("products.csv")
