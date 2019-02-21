import datetime
from httplib2 import Http
from json import dumps, loads

#
# Hangouts Chat incoming webhook quickstart
#
def main():
    http_obj = Http()
    url = 'https://chat.googleapis.com/v1/spaces/AAAADxpD2dc/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=WxwfLTQizAX8WEheMF6ByWuTxtAUX9Jvk33S2sLq-LI%3D'
    packtpub_url = 'https://www.packtpub.com/packt/offers/free-learning'

    # get current offers
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    tomorrow = now + datetime.timedelta(days=1)
    tomorrowDate = tomorrow.strftime('%Y-%m-%d')
    (resp_headers, content) = http_obj.request(
        uri=f'https://services.packtpub.com/free-learning-v1/offers?dateFrom={nowDate}T00:00:00.000Z&dateTo={tomorrowDate}T00:00:00.000Z',
    )
    offerJson = loads(content)
    productId = offerJson['data'][0]['productId']

    # get free offer info from summary
    (resp_headers, content) = http_obj.request(
        uri=f'https://static.packt-cdn.com/products/{productId}/summary',
    )
    bookInfoJson = loads(content)
    bookTitle = bookInfoJson['title']
    bookCover = bookInfoJson['coverImage']

    # send info with bot
    bot_message = {
        'text' : f'Free book, from <{packtpub_url}|Packtpub> \n\n Book: {bookTitle}\n Cover: {bookCover}',
    }
    message_headers = { 'Content-Type': 'application/json; charset=UTF-8'}
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )
    print(response)

if __name__ == '__main__':
    main()
