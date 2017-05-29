#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import requests
import unittest
import requests_mock
import mock
from mock import MagicMock, patch

from run import get_lib_module
from bot_lib import StateHandler
from contrib_bots import bot_lib
from six.moves import zip

from unittest import TestCase

from typing import List, Dict, Any
from types import ModuleType

current_dir = os.path.dirname(os.path.abspath(__file__))
from bots import giphy

class BotTestCase(TestCase):
    bot_name = '' # type: str

    def assert_bot_output(self, request, response, http_request=None):
        # type: (Dict[str, Any], str) -> None
        bot_module = os.path.join(current_dir, "bots",
                                  self.bot_name, self.bot_name + ".py")
        self.bot_test(request=request, bot_module=bot_module,
                      bot_response=[response], http_request=http_request)

    def mock_test(self, messages, message_handler, bot_response, http_request):
        # message_handler is of type Any, since it can contain any bot's
        # handler class. Eventually, we want bot's handler classes to
        # inherit from a common prototype specifying the handle_message
        # function.
        # type: (List[Dict[str, Any]], Any, List[str]) -> None
        # Mocking BotHandlerApi
        with patch('contrib_bots.bot_lib.BotHandlerApi') as MockClass:
            instance = MockClass.return_value

            for (message, response) in zip(messages, bot_response):
                # Send message to the concerned bot
                if http_request is not None:
                    with patch('requests.get') as mock_get:
                        mock_result = mock.MagicMock()
                        mock_result.json.return_value = response
                        mock_result.ok.return_value = True
                        mock_get.return_value = mock_result

                        message_handler.handle_message(message, MockClass(), StateHandler())
                        # There are 2 functions of the BotHandlerApi that the bot may call.
                        # It can call 'send_reply' function or the 'send_message' function for
                        # a given message.
                        try:
                            # Check if the bot is sending a reply message.
                            # 'response' is a string here.
                            instance.send_reply.assert_called_with(message, "https://media4.giphy.com/media/3o6ZtpxSZbQRRnwCKQ/giphy.gif")
                        except AssertionError:
                            # Check if the bot is sending a message via `send_message` function.
                            # Where response is a dictionary here.
                            instance.send_message.assert_called_with(response)

    def mock_http_test(self, request, message_handler, bot_response):
        with requests_mock.mock() as m:
            m.get(request['api_url'], params=request['params']).return_value = bot_response

            message_handler.handle_message(message, MockClass(), StateHandler())

    def bot_to_run(self, bot_module):
        # Returning Any, same argument as in mock_test function.
        # type: (str) -> Any
        lib_module = get_lib_module(bot_module)
        message_handler = lib_module.handler_class()
        return message_handler

    def bot_test(self, request, bot_module, bot_response, http_request):
        # type: (List[Dict[str, Any]], str, List[str]) -> None
        message_handler = self.bot_to_run(bot_module)
        self.mock_test(messages=[request], message_handler=message_handler,
                       bot_response=bot_response, http_request=http_request)
