from ytmusicapi import YTMusic

ytmusic = YTMusic()

search_results = ytmusic.search("i am good by david guetta")

for result in search_results:
    if result.get('resultType') == 'song':
        videoid = result.get('videoId')
        song_name = result.get('title')
        artists = [artist.get('name') for artist in result.get('artists', []) if artist.get('name') != 'Song']
        album_name = result.get('album', {}).get('name')
        thumbnail_url = result.get('thumbnails', [{}])[0].get('url', 'No thumbnail available')


        print('videoId: ', videoid)
        print('Song Name:', song_name)
        print('Artist(s):', ', '.join(artists))
        print('Album:', album_name)
        print('Thumbnail URL:', thumbnail_url)
        print()


    elif result.get('resultType') == 'album':
        album_name = result.get('title')
        album_artists = [artist.get('name') for artist in result.get('artists', []) if artist.get('name') != 'Album']
        album_thumbnail_url = result.get('thumbnails', [{}])[0].get('url', 'No thumbnail available')
        album_browse_id = result.get('browseId')
        album_id = ytmusic.get_album(album_browse_id)

        print('Album Name:', album_name)
        print('Album Artist(s):', ', '.join(album_artists))
        print('Album Thumbnail URL:', album_thumbnail_url)
        print('Album ID', album_id.get('audioPlaylistId'))
        print()

        break