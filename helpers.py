#
# This file is part of mtcli, a CLI for MeisterTask. mtcli is free software: 
# you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Michael Drüing <md@au.de>
#

import json

# MTCLI helper functions

def handle_api_error(response):
    json = response.json()
    print("----------------------------")
    print("API Error occured:")
    for error in json['errors']:
        print("  HTTP %s: %s" % (error['status'], error['message']))

    exit(1)


