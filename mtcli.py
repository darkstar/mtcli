#!/usr/bin/env python

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

from pathlib import Path
import click
import sys, json, requests  # TODO: remove "requests" as soon as all users have been moved out
import helpers
import projects
from cli import mtcli
from projects import get_project_id

# MeisterTask CLI interface

@mtcli.group()
def section():
    """Section management commands"""

    pass

@section.command()
@click.argument('id_or_name')
@click.pass_context
def list(ctx, id_or_name):
    """List sections"""

    apikey = ctx.obj['apikey']

    id = get_project_id(apikey, id_or_name)
    click.echo("Section list for project %s" % id_or_name)

    r = requests.get("https://www.meistertask.com/api/projects/%s/sections" % id,
            headers= {'Authorization': 'Bearer ' + apikey})

    if (r.status_code != requests.codes.ok):
        handle_api_error(r)

    json = r.json()
    fmt = "{:>10} | {:>4} | {:<15} | {:}" 
    print(fmt.format("id", "seq", "name", "description"))
    print("-" * 60)
    for section in json:
        print(fmt.format(section["id"], int(section["sequence"]), section["name"], section["description"]))


if __name__ == '__main__':
    print('mtcli - cli utility for MeisterTask.com')

    homedir = str(Path.home())
    cfgfiles = [ homedir + "/.mtcli.conf", "mtcli.conf" ]

    config = None
    ctxobj = {}

    for cfgfile in cfgfiles:
        if not Path(cfgfile).is_file():
            # skip / ignore files that don't exist
            continue

        # try to open the file
        try:
            with open(cfgfile) as config_file:
                config = json.load(config_file)
                ctxobj['apikey'] = config['apikey']
                print("Using config file " + cfgfile)
        except Exception as e:
            if (e is IOError): continue
            print ("Error in config file " + cfgfile + ": " + str(e))
            exit()

    mtcli(obj=ctxobj)

