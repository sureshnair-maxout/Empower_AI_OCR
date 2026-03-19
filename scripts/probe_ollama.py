import requests

if __name__ == '__main__':
    try:
        r = requests.get('http://localhost:11434')
        print(r.status_code)
        print(r.text[:1000])
    except Exception as e:
        print('error', e)
