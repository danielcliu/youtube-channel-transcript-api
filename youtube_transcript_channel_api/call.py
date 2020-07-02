from _api import YoutubeChannelTranscripts
from pprint import pprint

x = YoutubeChannelTranscripts('The Great War', 'AIzaSyC_OY9wErKeHnoIGzbdNLcY4XV3jhWBFj8')

vids, error = x.get_transcripts(just_text = True)
pprint(vids)
print('\nErrors: ', error)
