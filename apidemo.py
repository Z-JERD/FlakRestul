import json
import requests

URL = 'http://127.0.0.1:8088/todo/api/v1.0'
TASKID = '1'


def get_requests(url):
    """GET请求"""
    url = url +'/tasks'

    headers = {
        'Content-Type': "application/json",
        'Accept-Charset': "utf-8",
    }

    response = requests.request("GET", url, headers=headers)
    print(response.text)

def post_requests(url):
    """POST请求"""
    url = url + '/tasks'
    payload =  {
        "description": "python for data analysis",
        "done": False,
        "title": "Read a book"
                }

    headers = {
        'Content-Type': "application/json",
        'Accept-Charset': "utf-8",
    }

    response = requests.request("POST", url,data = json.dumps(payload), headers=headers)
    print(response.text)

def getone_requests(url,id):
    """GET请求"""
    url = url + '/tasks/' + id

    headers = {
        'Content-Type': "application/json",
        'Accept-Charset': "utf-8",
    }

    response = requests.request("GET", url, headers=headers)
    print(response.text)

def put_requests(url,id):
    """PUT请求"""
    url = url + '/tasks/' + id
    payload = {
        "description": "data warnging with pandas",
        "done": True,
        "title": "Ipython"
    }

    headers = {
        'Content-Type': "application/json",
        'Accept-Charset': "utf-8",
    }

    response = requests.request("PUT", url, data=json.dumps(payload), headers=headers)
    print(response.text)

def delete_requests(url,id):
    """DELETE请求"""
    url = url + '/tasks/' + id
    headers = {
        'Content-Type': "application/json",
        'Accept-Charset': "utf-8",
    }

    response = requests.request("DELETE", url, headers=headers)
    print(response.text)

if __name__ == '__main__':
    #get_requests(URL)
    post_requests(URL)
    #getone_requests(URL, TASKID)
    #put_requests(URL, TASKID)
    #delete_requests(URL, TASKID)
