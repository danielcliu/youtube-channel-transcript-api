# youtube-transcript-channel-api
[![Build Status](https://travis-ci.com/github/danielcliu/youtube-channel-transcript-api.svg)](https://travis-ci.com/github/danielcliu/youtube-channel-transcript-api) [![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](http://opensource.org/licenses/MIT)
Expand upon the youtube-transcript-api and allow users to easily request all of a channel's (and maybe a playlist's) video captions. Will require use of Youtube Data API v3.

## API

Integrate this package into your python 3.6+ application. It is built as a sort of expansion [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api). For that reason, that package's warnings/use cases mostly apply to this project as well. 

The package revolves around creating YoutubeChannelTranscript objects. This package also is built on the YouTube Data API v3, which means to use this you will need to setup your own account and use your own API Key. See (here)[https://developers.google.com/youtube/v3/getting-started] for directions how to setup your account if you don't have one.

```python
YoutubeChannelTranscript(<youtube channel name>, <youtube data api key>)
```
You can then either call `get_transcripts()` to return a dictionary of all transcripts and a list of videos that errored, or you can call `write_transcripts()` to write out all of the transcripts to json files at the filepath location. `write_transcripts()` will create a directory `/YoutubeChannelTranscripts` and then write each videos transcript in ints own, seperate json file.

The easiest way to do so is to execute:

```python

from youtube_channel_transcript_api import YoutubeChannelTranscripts

channel_getter = YoutubeChannelTranscripts('A Youtube Channel', 'Youtube Data API Key here')

videos_data, videos_errored = channel_getter.get_transcripts()
```

In this instance, `videos_data` will look like

```python
{
 'video id 1': 
	{ 'title': 'videos title 1',
	  'captions': [
			{
				'text': 'Hey there',
				'start': 7.58,
				'duration': 6.13
			},
			{
				'text': 'how are you',
				'start': 14.08,
				'duration': 7.58
			},
			# ...
		]
	},
 'video id 2': 
	{ 'title': 'videos title 2',
	  'captions': [
			{
				'text': 'Hola there',
				'start': 5.1,
				'duration': 6.13
			},
			{
				'text': 'how are I',
				'start': 12.08,
				'duration': 3.58
			},
			# ...
		]
	},
 #...
}
```

And `videos_errored` will look like

```python
[ ['video title 1', 'video id 1'], ['video title 2', 'video id 2'] ]
```
### Parameters 
Both `get_transcripts()` and `write_transcripts()` have the same, optional parameters.

#### Languages

youtube-channel-transcripts-api supports users trying to get their desired language from a channel's videos. To do this you can add a `languages` parameter to the call (it defaults to english).

You can also add the `languages` param if you want to make sure the transcripts are retrieved in your desired language (it defaults to english).

```python
channel_getter = YoutubeChannelTranscripts('A Youtube Channel', 'Youtube Data API Key here')

videos_data, videos_errored = channel_getter.get_transcripts(languages=['de', 'en]))
```

It's a list of language codes in a descending priority. In this example it will first try to fetch the german transcript (`'de'`) and then fetch the english transcript (`'en'`) if it fails to do so.

#### Cookies

Some videos are age restricted, so this module won't be able to access those videos without some sort of authentication. To do this, you will need to have access to the desired video in a browser. Then, you will need to download that pages cookies into a text file. You can use the Chrome extension [cookies.txt](https://chrome.google.com/webstore/detail/cookiestxt/njabckikapfpffapmjgojcnbfjonfjfg?hl=en) or the Firefox extension [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/).

Once you have that, you can use it with the module to access age-restricted videos' captions like so. 

```python  
channel_getter = YoutubeChannelTranscripts('A Youtube Channel', 'Youtube Data API Key here')

videos_data, videos_errored = channel_getter.get_transcripts(cookies='/path/to/your/cookies.txt')
```

#### Proxies

You can specify a https/http proxy, which will be used during the requests to YouTube:  
  
```python  
channel_getter = YoutubeChannelTranscripts('A Youtube Channel', 'Youtube Data API Key here')

videos_data, videos_errored = channel_getter.get_transcripts(proxies={"http": "http://user:pass@domain:port", "https": "https://user:pass@domain:port"})  
```  
  
As the `proxies` dict is passed on to the `requests.get(...)` call, it follows the [format used by the requests library](http://docs.python-requests.org/en/master/user/advanced/#proxies).  

#### Just Text
You can specify for the responses to not include timestamp information in the `videos_data` returned, or in the files written out to memory. By default, `just_text` is set to `False`


```python  
channel_getter = YoutubeChannelTranscripts('A Youtube Channel', 'Youtube Data API Key here')

videos_data, videos_errored = channel_getter.get_transcripts(just_text=False)


videos_data, videos_errored = channel_getter.get_transcripts()
```

In this instance, `videos_data` will now look like

```python
{
 'video id 1': 
	{ 'title': 'videos title 1',
	  'captions': 'Hey there how are you ...',
	},
 'video id 2': 
	{ 'title': 'videos title 2',
	  'captions': 'Hola there how are I ...',
	},
 #...
}
```

## Warning  
  
 This code, in part, uses an undocumented part of the YouTube API, which is called by the YouTube web-client. So there is no guarantee that it won't stop working tomorrow, if they change how things work. It also uses the Youtube Data API v3, so it is up to you that you are following all of that API's rules. In addition, you will have to worry about managing your own Quota for the YouTube Data API, its resource for limiting calls.  
