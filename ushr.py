import ticketpy
import tekore as tk
import requests

# Input your own Spotify API token.
token = ''
sp = tk.Spotify()

# Input your own Ticketmaster key.
key = ''
tm = ticketpy.ApiClient(key)

# Collecting and compounding the user's top 50 artists for short-term listening and long-term listening.
'''
artists = []
with sp.token_as(token):
    for term in ["long_term", "short_term"]:
        temp_artists = sp.current_user_top_artists(limit = 1, offset = 0, time_range = term)
        for artist in temp_artists.items:
            # Ensuring no repetitions in the 'artists' list will exist.
            if artist.name not in artists:
                artists.append(artist.name)

print(artists) 
'''

# //just example artists
artists = ["Kanye West", "BIGBABYGUCCI", "Gregory Alan Isakov"]


# Function to handle the JSON extraction of event information.
def get_event(ticket_url, event_id):
    event = requests.get(ticket_url,  json = {"id":event_id})
    json_resp = event.json()
    return json_resp

def gather(element):
    try:
        return element
    except:
        return None

def handle_events(sort_by = None, genre = None):

    events = []
    for artist in artists:
        temp = tm.events.find(
            # FIND A WAY TO HAVE ALL GENRES IF GENRE IS NONE
            classification_name = genre,
            keyword=artist
        )

        for pages in temp:
            for event in pages:
                event_id = event.id
                ticket_url = 'https://app.ticketmaster.com/discovery/v2/events/' + str(event_id) + '.json?apikey=' + key

                date_info = get_event(ticket_url, event_id).get('dates')
                emb_info = get_event(ticket_url, event_id).get('_embedded')

                event_dict = {
                    'name' : get_event(ticket_url, event_id).get('name'),
                    'url' : get_event(ticket_url, event_id).get('url'),
                    'id' : get_event(ticket_url, event_id).get('id'),
                    'locale' : get_event(ticket_url, event_id).get('locale'),
                    'localDate' : date_info['start']['localDate'] if date_info else 'n/a',
                    'name' : emb_info['venues'][0]['name'] if emb_info else 'n/a',
                    'postalCode' : emb_info['venues'][0]['postalCode'] if emb_info else 'n/a'
                }

                events.append((artist, event_dict))
    

    match sort_by:
        case 'localDate':
            events = sorted(events, key = lambda x: x[1]['localDate'])
        # ADD MORE SORTING CASES

    for event in events:
        print(event)

handle_events('localDate')
