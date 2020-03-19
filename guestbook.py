#!/usr/bin/env python

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START imports]
import sys
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from firebase import firebase
firebase_url = 'https://profitlogger-1314.firebaseio.com'
fb = firebase.FirebaseApplication(firebase_url, None)

import json
from datetime import datetime, timedelta

from GetOrders import GetOrders
import socket

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)


# [START greeting]
class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END greeting]


# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END main_page]


# [START guestbook]
class Guestbook(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))
# [END guestbook]


# [START orders page]
class OrdersPage(webapp2.RequestHandler):

    def get(self):
        #orders = fb.get('/', 'fees')
        
        url = 'http://www.google.com/humans.txt'
        
        response = fb.get('/', 'fees')
        print 'lalalala'
        for fee in response:
            print fee
        
        return
        if False:
            Now = datetime.utcnow()
            NumberOfDays = 30

            try:
                if NumberOfDays > 0:
                    responses = GetOrders(NumberOfDays=NumberOfDays,
                                          IncludeFinalValueFee=True
                                         )

                    for i, response in enumerate(responses):
                        response = response.dict()
                        print 'PageNumber: %s' % (i + 1)
                        print json.dumps(response, sort_keys=True, indent=5)

                        if 'OrderArray' in response and 'Order' in response['OrderArray']:
                            for order in response['OrderArray']['Order']:
                                pass
            except Exception as e:
                raise
            else:
                print('successfully retrieved')

                # if GetAccount does not raise an exception, update the EndDate
                #firebase.put('/api_calls/ebay', 'update_orders', Now.isoformat() + 'Z')
                print('successfully updated')

            orders=[]
            for order in orders:
                print order

            template_values = {
                'orders': orders
            }

        #template = JINJA_ENVIRONMENT.get_template('index.html')
        #self.response.write(template.render(template_values))
# [END main_page]


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    ('/orders', OrdersPage)
], debug=True)
# [END app]
