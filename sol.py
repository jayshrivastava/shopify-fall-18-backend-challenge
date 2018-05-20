# Enter your code here. Read input from STDIN. Print output to STDOUT
import urllib.request,sys, json, collections
#Get input parameters
params = json.load(sys.stdin)
cartid = (params['id'])
cartidstr = str(cartid)
dtype = (params['discount_type'])
discount_value = (params['discount_value'])
eligibility= ""
if 'collection' in params.keys(): eligibility= 'collection'
elif 'product_value' in params.keys(): eligibility= 'product_value'
else: eligibility= 'cart_value'

#Get pagination Information
with urllib.request.urlopen("http://backend-challenge-fall-2018.herokuapp.com/carts.json?id=" +cartidstr + "+&page=1") as url:
    data = json.loads(url.read().decode())
total = data['pagination']['total']
perpage =  data['pagination']['per_page']
pages = 0
if  (total % perpage):
  pages = total//perpage + 1
else: pages = total//perpage

#Price variables
total_price = 0
total_discounted = 0

#Cycle through data
for i in range(1, pages + 1):
  istr = str(i)
  with urllib.request.urlopen("http://backend-challenge-fall-2018.herokuapp.com/carts.json?id="+cartidstr+"&page="+istr) as url:
    data = json.loads(url.read().decode())
  for product in data['products']:
    #Record the price
    total_price += product['price']
    total_discounted += product['price']
    #Collections Discount
    if 'collection' in product.keys():
      if eligibility== 'collection' and product['collection'] == params['collection']:
        total_discounted -= min(discount_value, product['price'])
    #Products Price Discount
    if eligibility== 'product_value' and product['price'] >= params['product_value']:
        total_discounted -= min(discount_value, product['price'])

#Cart Discount
if eligibility== 'cart_value' and total_price > params['cart_value']:
    total_discounted -= min(discount_value, total_price);

#Generate Answer
ans = collections.OrderedDict()
ans["total_amount"]= total_price
ans["total_after_discount"] = total_discounted
print(json.dumps(ans,  sort_keys=False, indent=2, separators=(',', ': ')))
