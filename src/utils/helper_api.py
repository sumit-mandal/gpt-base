import requests
import json
import requests

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


    return cii_response.json()

def insta_combo():
  
  url = "https://instafinancials.com/api/InstaCombo/v1/json/OrderID/1324658/DownloadReport"
  request_headers = { "user-key": "imNivkDuIOU0wb+pekiMFh+c6fJyhJ4MFADeNwBL8mFTJ9lgCqH15g==" }
  response = requests.get(url, headers = request_headers)

  return response.json()

def json_data_source():

    # Path to your JSON file
    file_path = "new_cii_data.json"
    
    with open(file_path, 'r') as f:
      
      json_data = f.read()
    json_string = json.dumps(json_data) 

    
    return str(json_string)
    
    

    


    