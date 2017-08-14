# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2017 CERN.
#
# INSPIRE is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Module for backend of multi record editor used in http://inspirehep.net."""

from __future__ import absolute_import, print_function

from flask import Blueprint, render_template,request
from flask_babelex import gettext as _
import requests
#from actions import *

blueprint = Blueprint(
    'multiedit',
    __name__,
    template_folder='templates',
    static_folder='static',
)


"""@blueprint.route("/multiedit")
def index():
    Basic view
    return render_template(
        "multiedit/index.html",
        module_name=_('MultiEdit'))"""


@blueprint.route("/multiedit/update", methods=['POST'])
def index():
    """Basic view."""
    from remote_pdb import RemotePdb
    RemotePdb('0.0.0.0', 4444).set_trace()
    return request.data

