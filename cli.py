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

import click

@click.group()
@click.option('--apikey', help="Set the API key")
@click.pass_context
def mtcli(ctx, apikey):
    if (apikey is not None): 
        # save APIKEY for later use
        ctx.obj['apikey'] = apikey

    try:
        ctx.obj['apikey']
    except:
        print ("No apikey defined. Either specify --apikey or put it into ~/.mtcli.conf.")
        exit()

