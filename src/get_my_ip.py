import  requests 


url = "http://lumtest.com/myip.json"


response = requests.get(url)

if response.status_code == 200: 
    print(response.json())
    
else:
    print("error")
    