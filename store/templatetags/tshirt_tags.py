from django import template
from math import floor
register=template.Library()


# creation of tags 
@register.simple_tag
def min_price(tshirt):
    size=tshirt.sizevariant_set.all().order_by('price').first()
    return size.price

@register.simple_tag
def sale_price(tshirt):
    price=min_price(tshirt)
    discount=tshirt.discount

    return floor(price-(price *discount/100))

@register.simple_tag 
def calc_sale_price(price,discount):
    return floor(price-(price *discount/100))

@register.simple_tag
def get_active_size_button_class(active_size ,size):
    if active_size.size==size.size:
        return "success"
    else:
        return "light"

@register.simple_tag 
def multiply(a,b):
    return a*b

@register.simple_tag 
def get_final_price(order):
    total=0
    for oi in  order.orderitem_set.all():
        total+=oi.price*oi.quantity
    return total


# making of custom filter

@register.filter 
def rupee(number):
    return f'₹ {number}'

    

@register.filter 
def cal_total_payable_amount(cart):
    total=0
   
    for c in cart : 
        discount= c.get('tshirt').discount
        price=c.get('size').price
        sale_price=calc_sale_price(price,discount)
        total_of_single_product=sale_price * c.get('quantity')
        total+=total_of_single_product
    return total


