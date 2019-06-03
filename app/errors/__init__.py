#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 user <user@user-pc>
#
# Distributed under terms of the MIT license.

"""
    错误蓝图 blueprint
"""

from flask import Blueprint

bp = Blueprint('errors',__name__)

from app.errors import handlers
