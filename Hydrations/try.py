msg = ""
name = "vitamin-1"
quantity = 2
price = 2000
product_data = ['vitamin-1#2#2000',"gummied-hair#4#4500"]
for i in product_data:
    name = i.split("#")[0]
    quantity = i.split("#")[1]
    price = i.split("#")[2]
    msg += ",name->{},quantity->{},price->{}".format(name,quantity,price)
print(msg)