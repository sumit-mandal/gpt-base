import requests
import json

def api_calling_signzy(cin):
    
    
    url = "https://api-preproduction.signzy.app/api/v3/roc/simpleSearchByCin"
    
    payload = json.dumps({
      "cin": cin
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'kU9Owu40wGRxMAqrfoPn5h5LSDk2V22g'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text

def api_calling_instafinancials():
    url = "https://instafinancials.com/api/InstaBasic/v1/json/CompanyCIN/L24230GJ1995PLC025878/All"
    request_headers = { "user-key": "imNivkDuIOU0wb+pekiMFh+c6fJyhJ4MFADeNwBL8mFTJ9lgCqH15g==" }
    response = requests.get(url, headers = request_headers)

    return response.text

def api_calling_cii():
    url = "https://services.mycii.in/MemDirectory/GetMembers"

    cii_response = requests.request("GET", url)


    return cii_response.text



    

    


    