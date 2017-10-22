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
import sys, json, requests
import helpers
from cli import mtcli

# project related functions

project_id_to_status = { "1": "active", "4": "trashed", "5": "archived" }
project_status_to_id = { "active": "1", "trashed": "4", "archived": "5" }

def get_project_id(apikey, id_or_name):
    """Get the ID of a project by its name or id"""

    # if ID is numeric, treat it as the final ID
    try:
        int(id_or_name)
        return id_or_name
    except ValueError:
        # get all projects
        r = requests.get("https://www.meistertask.com/api/projects", 
                headers= {'Authorization': 'Bearer ' + apikey})
    
        # Find the wanted project
        # TODO: Fuzzy match?
        for p in r.json():
            if (p["name"] == id_or_name):
                return p["id"]
    
    # Not found? -> error
    print("No project named '%s' found" % id_or_name)
    exit(1)


@mtcli.group()
def project():
    """Project management commands"""

    pass


@project.command()
@click.option('--status', 
        type=click.Choice(["active", "archived", "trashed", "all"]),
        help="Status of the project. Default is active",
        default="active")
@click.pass_context
def list(ctx, status):
    """List all projects"""

    # grab api key
    apikey = ctx.obj['apikey']

    click.echo("Project List")

    r = requests.get("https://www.meistertask.com/api/projects", 
            params= { 'status': status },
            headers= {'Authorization': 'Bearer ' + apikey})

    if (r.status_code != requests.codes.ok):
        handle_api_error(r)

    fmt = "{:>10} | {:<30} | {:}"
    print(fmt.format("id", "name", "notes"))
    print("-" * 60)
    for proj in r.json():
        print(fmt.format(proj['id'], proj["name"], proj["notes"]))

@project.command()
@click.argument('id_or_name')
@click.pass_context
def show(ctx, id_or_name):
    """Show details of the project identified by ID or NAME"""

    # grab API key
    apikey = ctx.obj['apikey']

    click.echo("Project details")

    id = get_project_id(apikey, id_or_name)

    r = requests.get("https://www.meistertask.com/api/projects/%s" % id,
            headers= {'Authorization': 'Bearer ' + apikey})

    if (r.status_code != requests.codes.ok):
        handle_api_error(r)

    json = r.json()
    for key in json:
        print("{:>20} : {:}".format(key, json[key]))


@project.command()
@click.argument('id_or_name')
@click.option("--name",
        help="Set the name of the project")
@click.option("--notes",
        help="Set the notes on the project")
@click.option("--status",
        type=click.Choice(["active", "archived", "trashed"]),
        help="Set the status of the project")
@click.pass_context
def set(ctx, id_or_name, name, notes, status):
    """Set fields in a project given by ID or NAME"""

    apikey = ctx.obj['apikey']

    if (name is None and notes is None and status is None):
        print("At least one option of [--name, --notes, --status] is required.")
        exit(1)

    id = get_project_id(apikey, id_or_name)

    post_data = {}
    if (name is not None):
        post_data['name'] = name
    if (notes is not None):
        post_data['notes'] = notes
    if (status is not None):
        post_data['status'] = project_status_to_id[status]

    r = requests.put("https://www.meistertask.com/api/projects/%s" % id,
            data=post_data,
            headers= {'Authorization': 'Bearer ' + apikey})

    if (r.status_code != requests.codes.ok):
        handle_api_error(r)

    json = r.json()
    for key in json:
        print("{:>20} : {:}".format(key, json[key]))


