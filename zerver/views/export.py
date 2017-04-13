from __future__ import absolute_import
from __future__ import print_function

from typing import Any

from argparse import ArgumentParser
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError

import os
import shutil
import subprocess
import tempfile
import ujson

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import Encoders
import datetime

from zerver.management.commands.export_single_user import Command

def export_single_user(request):
    options = {}
    options["email"] = "aaron@zulip.com"
    options["output_dir"] = None
    args = []
    command = Command()
    Command.handle(command, args, **(options))
