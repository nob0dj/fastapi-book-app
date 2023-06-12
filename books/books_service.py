import requests
import xmltodict
from fastapi import HTTPException

from books import books_crud
from models import Book

# 요청 헤더 설정
headers = {
    'X-Naver-Client-Id': 'AQPs0J6bHIrxFKN8Yxqb',
    'X-Naver-Client-Secret': 'iNcRoY21Q2'
}


def search_books(query: str):
    params = {'query': query}
    response = requests.get('https://openapi.naver.com/v1/search/book.json', params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data['items']
    else:
        raise HTTPException(status_code=500, detail="API요청 실패!")


def get_book(isbn: str):
    response = requests.get(f'https://openapi.naver.com/v1/search/book_adv.xml?d_isbn={isbn}', headers=headers)
    if response.status_code == 200:
        # xmltodict xml데이터를 dict형태로 변환
        data = xmltodict.parse(response.text)
        # print(data)
        if data['rss']['channel']['total'] == '1':
            return Book(data['rss']['channel']['item'])
        else:
            return {'result': 'Not Found'}, 404
    else:
        raise HTTPException(status_code=500, detail="API요청 실패!")
