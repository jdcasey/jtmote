#
# Copyright (C) 2017 Red Hat, Inc. (jdcasey@commonjava.org)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import click
import os
from jira import JIRA
import yaml
import jtmote.util as util

URL='url'
USER='user'
PASSKEY='passkey'

@click.command()
@click.option('--config-file', '-C', 
              type=click.Path(exists=True), 
              help='Specify the configuration file (default: $HOME/.config/jtmote/config.yml)', 
              default=os.path.join(os.environ.get('HOME'), '.config/jtmote/config.yml'))
def sync(config_file):
    with open(config_file) as f:
        config = yaml.safe_load(f)

    jira=JIRA(config[URL], basic_auth=(config[USER], util.get_password(config[PASSKEY])))

    out_of_sprint_issues = jira.search_issues('sprint != NULL and sprint not in openSprints() and assignee = currentUser()')
    in_sprint_issues = jira.search_issues('sprint != NULL and sprint in openSprints() and assignee = currentUser()')

    util.demote(out_of_sprint_issues)
    util.promote(in_sprint_issues)

