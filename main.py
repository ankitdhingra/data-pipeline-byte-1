#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import feedparser
import logging
import webapp2

from webapp2_extras import jinja2

# BaseHandler subclasses RequestHandler so that we can use jinja
class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

        # This will call self.response.write using the specified template and context.
        # The first argument should be a string naming the template file to be used.
        # The second argument should be a pointer to an array of context variables
        #  that can be used for substitutions within the template
    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)

def extract_feed(state1, state2):
    feed1 = feedparser.parse("http://pipes.yahoo.com/pipes/pipe.run?_id=ac7cd8d6fb84bb590251d80847338d25&_render=rss&state="+state1)
    logging.info("Respose from 1st query: " +str(feed1["items"]))
    feed2 = feedparser.parse("http://pipes.yahoo.com/pipes/pipe.run?_id=ac7cd8d6fb84bb590251d80847338d25&_render=rss&state="+state2)
    logging.info("Respose from 2st query: " + str(feed2["items"]))
    item1 = feed1["items"][0]
    item2 = feed2["items"][0]
    return [item1.description, item2.description]


class MainHandler((BaseHandler)):
    def get(self):
        rents = extract_feed("CALIFORNIA","PENNSYLVANIA")
        context = {"state1": "CALIFORNIA", "number1" : rents[0], "state2" : "PENNSYLVANIA", "number2" : rents[1]}

        self.render_response('index.html', **context)

    def post(self):
        logging.info(self.request)
        state1 = self.request.get('state1')
        state2 = self.request.get('state2')

        rents = extract_feed(state1,state2)
        context = {"state1": state1, "number1" : rents[0], "state2" : state2, "number2" : rents[1]}

        self.render_response('index.html', **context)

app = webapp2.WSGIApplication([
    ('/.*', MainHandler)
], debug=True)
