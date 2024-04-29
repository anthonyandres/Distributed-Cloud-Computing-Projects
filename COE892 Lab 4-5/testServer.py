import requests
# lista = requests.get("http://127.0.0.1:8000/rovers").json()['rover Status List']
# print(lista)
# for rover in lista:
#     if rover.startswith("04"):
#         print("ROVER 04 EXISTS!!")
#         break
#     else:
#         print("searching for ROVER 04...")
#print(requests.get("http://127.0.0.1:8000/rovers/01").json()["rover Status"])

response = requests.get("http://127.0.0.1:8000/rovers/02")
print(response.json())
data1 = response.json()['rover commands']
print(data1)
print(requests.get("http://127.0.0.1:8000/map").json()['map'])
# commands = input("input commands: ")
# ID = input("input ID: ")
# print(requests.put("https://lab4-fast-api.azurewebsites.net/rovers/{ID}?commands={commands}".format(ID=ID, commands=commands)).json())
#rovers?id=11&commands=MMLMRM
#print(requests.get("https://lab4-fast-api.azurewebsites.net/rovers").json())
