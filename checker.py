import requests
url = "http://localhost:8000/login"

data={
    "username":"yuba",
    "password":"asdf"
}
requests.post(url,json=data)