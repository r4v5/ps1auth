#!/usr/bin/env python
import json
from pprint import pprint

# pretend we are getting actual data
raw_string = open('records.json', 'r').read()
records = json.loads(raw_string)

# get just the useful stuff
records = records['response']['result']['Contacts']['row']

#something looks wrong here, I suspect multi record resoponses are going to look different
person = records['FL']

#format a person object sanely
sane_object = dict( map( lambda f: (f['val'], f['content']), person ) )

#restrict to just the data I expect after getting a custom view
member = {}
member['CONTACTID'] = sane_object['CONTACTID'] # uniq id's are almost always useful
member['Email'] = sane_object['Email'] # password reset links
member['First Name'] = sane_object['First Name']
member['Last Name'] = sane_object['Last Name']
member['Membership Status'] = sane_object['Membership Status'] # need to handle former/banned members carefully

#present the finished product
pprint(member)

