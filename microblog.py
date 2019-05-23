#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 user <user@user-pc>
#
# Distributed under terms of the MIT license.

"""

"""

from app import app,db
from app.models import User, Post


@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User, 'Post':Post}
