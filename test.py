import requests 

BASE = "http://127.0.0.1:5000/"

# data = [{"likes": 10, "name": "How to Golf", "views":555},
#         {"likes": 3000, "name": "Putting 101", "views":4000},
#         {"likes": 676, "name": "Build better teams", "views":10000}]

# for i in range(len(data)):
#     j = i + 7 
#     response = requests.put(BASE + "video/" + str(j), data[i])
#     print(response.json())

# input()
# response = requests.delete(BASE + "video/0")
# print(response)
# input()
# response = requests.get(BASE + "video/2")
# print(response.json())

response = requests.patch(BASE + "video/2", {"views":909, "likes":1})
print(response.json())
