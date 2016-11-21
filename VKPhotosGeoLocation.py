import time
import vk

ACCESS_TOKEN = "4588c22abb2379b0e8c50b8f394bf2b8eb2f169e4112ba0334b5972934684f8a7a4d36f6bded39e7b3908"

session = vk.Session(ACCESS_TOKEN)

api = vk.API(session)

friends = api.friends.get()

geolocation = []

for id in friends:
    print('Получаем данные пользователя: %s' % id)

    try:
        albums = api.photos.getAlbums(owner_id=id)
        print('\t... альбом %s...' % len(albums))

        for album in albums:
            photos = api.photos.get(owner_id=id, album_id=album['aid'])
            print('\t\t... обрабатываем фотографии альбома....')

            for photo in photos:
                if 'lat' in photo and 'long' in photo:
                    geolocation.append((photo['lat'], photo['long']))

            print('\t\t... найдено %s фото...' % len(photos))

            time.sleep(.5)
        time.sleep(.5)
    except:
        pass

js_code = ""

for loc in geolocation:
    js_code += 'new google.maps.Marker({position: {lat: %s, lng: %s}, map: map });\n' % (loc[0], loc[1])

html = open('map.html').read()
html = html.replace('/* PLACEHOLDER */', js_code)

f = open('VKPhotosGeoLocation.html', 'w')
f.write(html)
f.close()
