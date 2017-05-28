#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os
import sys

our_dir = os.path.dirname(os.path.abspath(__file__))
# For dev setups, we can find the API in the repo itself.
if os.path.exists(os.path.join(our_dir, '..')):
    sys.path.insert(0, '..')
from bots_test_lib import BotTestCase

class TestFollowUpBot(BotTestCase):
    bot_name = "followup"

    def test_bot(self):
        # This message calls `send_message` function of BotHandlerApi
        self.assert_bot_output(
            {'content': "foo", 'type': "private", 'sender_email': "foo_sender@zulip.com"},
            (dict(
                type='stream',
                to='followup',
                subject='foo_sender@zulip.com',
                content='from foo_sender@zulip.com: foo',
            ))
        )
        # This message calls `send_reply` function of BotHandlerApi
        self.assert_bot_output(
            {'content': "", 'type': "stream", 'display_recipient': "foo", 'subject': "foo", 'sender_email': "foo_sender@zulip.com"},
            "Please specify the message you want to send to followup stream after @mention-bot"
        )
        # This message calls `send_message` function of BotHandlerApi
        self.assert_bot_output(
            {'content': "I have completed my task", 'type': "stream", 'display_recipient': "foo", 'subject': "foo", 'sender_email': "foo_sender@zulip.com"},
            (dict(
                type='stream',
                to='followup',
                subject='foo_sender@zulip.com',
                content='from foo_sender@zulip.com: I have completed my task',
            ))
        )
