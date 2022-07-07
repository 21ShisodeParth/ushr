import ticketpy
import tekore as tk
import requests

sp = tk.Spotify()
token = '' #your token

artists = []
with sp.token_as(token):
    for term in ["long_term", "short_term"]:
        temp_artists = sp.current_user_top_artists(limit=1, offset=0, time_range=term)
        for artist in temp_artists.items:
            artists.append(artist.name)

# print(artists)

key = '' #your token
tm = ticketpy.ApiClient(key)
artists = ["Kanye West", "BIGBABYGUCCI"]

def get_event(ticket_url, event_id):
    event = requests.get(ticket_url,  json = {"id":event_id})
    json_resp = event.json()
    return json_resp

events = []
for artist in artists:
    temp = tm.events.find(
        classification_name='Hip-Hop',
        keyword=artist
    )

    for pages in temp:
        for event in pages:
            event_id = event.id
            ticket_url = 'https://app.ticketmaster.com/discovery/v2/events/' + str(event_id) + '.json?apikey=nsLfwpueMjA6sRNDrJ8QOg90LOO4ApAj'
            temp2 = [
                artist,
                get_event(ticket_url, event_id)['name'],
                get_event(ticket_url, event_id)['url'],
                get_event(ticket_url, event_id)['id'],
                get_event(ticket_url, event_id)['locale'],
                get_event(ticket_url, event_id)['dates']['start']['localDate'],
                get_event(ticket_url, event_id)['_embedded']['venues'][0]['name'],
                get_event(ticket_url, event_id)['_embedded']['venues'][0]['postalCode']
                ]

            events.append(temp2)

for event in events:
    print(event)
