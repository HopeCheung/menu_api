import requests

print("----------------------------Test GET-------------------------------")
def get_menu():
    url = 'http://127.0.0.1:5000/api/menusection'
    request = requests.get(url)
    print(request.text)

get_menu()


print("----------------------------Test GET with ID-------------------------------")
def get_specific_menu(id):
    url = 'http://127.0.0.1:5000/api/menusection' + "/" + id
    request = requests.get(url)
    print(request.text)

get_specific_menu("1")


print("----------------------------Test POST-------------------------------")
def post_menu(tmp):
    url = 'http://127.0.0.1:5000/api/menusection'
    headers = {'Content-Type' : 'application/json'}
    payload = tmp
    request = requests.post(url, headers = headers, data=payload)
    print(request.text)

post_menu("{\n\t\"id\" : 4,\n\t\"name\": \"Breakfast specials\",\n\t\"item\": \"bread\"\n}")
print("----------------------------After insert new item-------------------------------")
get_menu()


print("----------------------------Test DELETE-------------------------------")
def delete_specific_menu(id):
    url = 'http://127.0.0.1:5000/api/menusection' + "/" + id
    request = requests.delete(url)
    print(request.text)

delete_specific_menu("3")
print("----------------------------After Deletion-------------------------------")
get_menu()


print("----------------------------Test POST with ID-------------------------------")
def post_specific_menu(tmp, id):
    url = 'http://127.0.0.1:5000/api/menusection' + "/" + id
    headers = {'Content-Type': 'application/json'}
    payload = tmp
    request = requests.post(url, headers=headers, data=payload)
    print(request.text)

post_specific_menu("{\n\t\"name\": \"New specials\",\n\t\"item\": \"milk\"\n}", "3")
print("----------------------------After insert new item-------------------------------")
get_menu()


print("----------------------------Upload item with id=3,name=New specials,item=milk------------------------------")
def update_menu(payload):
    url = "http://127.0.0.1:5000/api/menusection/3/name=New specials,item=milk"
    headers = {'Content-Type': 'application/json'}
    response = requests.request("PUT", url, data=payload, headers=headers)
    print(response.text)

update_menu("{\n\t\"name\": \"Old specials\",\n\t\"item\": \"coffee\"\n}")
print("----------------------------After update item 3-------------------------------")
get_menu()
