import requests
import sys
def url_test(url):
    try:
        response = requests.head(url)
        if response.status_code == 200:
            print("True")
            return True
        else:
            return False
    except requests.ConnectionError as error:
        print(error)
        return error


if __name__ == '__main__':
    url = "http://localhost:5000/"
    if url_test(url):
        sys.exit(0)
    else:
        sys.exit(1)

