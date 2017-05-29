#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import json
from . import giphy

our_dir = os.path.dirname(os.path.abspath(__file__))
# For dev setups, we can find the API in the repo itself.
if os.path.exists(os.path.join(our_dir, '..')):
    sys.path.insert(0, '..')
from bots_test_lib import BotTestCase
from bots.giphy import giphy

class TestGiphyBot(BotTestCase):
    bot_name = "giphy"

    def test_bot(self):
        # This message calls `send_reply` function of BotHandlerApi
        response_json={
        'meta': {'status':200},
        'data':{'images': {'original': {'url': "https://media4.giphy.com/media/3o6ZtpxSZbQRRnwCKQ/giphy.gif"}}}
        }
        self.assert_bot_output(
            {'content': "Hello", 'type': "private", 'sender_email': "foo_sender@zulip.com"},
            response_json,
            {'api_url': giphy.GIPHY_TRANSLATE_API, 'params': {'s': "Hello", 'api_key': giphy.get_giphy_api_key_from_config()}}
        )
       
