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

import os
import sys
import re
import subprocess

def parse_sprint_close(issue):
    """
      customfield_10005 = [
        u'com.atlassian.greenhopper.service.sprint.Sprint@540cefa8[id=3319,rapidViewId=1014,state=CLOSED,name=NOS Sprint 24,startDate=2017-06-15T03:24:11.235Z,endDate=2017-06-28T16:43:00.000Z,completeDate=2017-06-29T03:04:12.831Z,sequence=3319]', 
        u'com.atlassian.greenhopper.service.sprint.Sprint@1cf94455[id=3493,rapidViewId=1014,state=CLOSED,name=NOS Sprint 25,startDate=2017-06-29T03:14:31.405Z,endDate=2017-07-12T16:33:00.000Z,completeDate=2017-07-13T03:07:13.698Z,sequence=3493]']
    """ 
    rawArry = None
    for a in dir(issue.fields):
        if a.startswith('_') is True:
            continue

        a = str(a)
        raw = getattr(issue.fields, a)
        if isinstance(raw, list) and str(raw[0]).startswith('com.atlassian.greenhopper.service.sprint.Sprint@'):
            sprintField = a
            rawArry = raw
            break

    for raw in rawArry:
        raw = str(raw)
        match = re.match(r'.+,state=([^,]+),.*name=([^,]+),.*endDate=([^,]+),.+', raw)
        if match is not None:
            state = match.group(1)
            if state == 'ACTIVE':
                name = match.group(2)
                print "Found ACTIVE sprint: %s" % name
                end=match.group(3)[:-5]
                return end

    return None

def get_password(passkey):
    """ Retrieve password from `pass` for the given key"""

    command = "pass %s" % passkey
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    if p.returncode == 0:
        return p.stdout.readline().strip().decode('utf-8')
    else:
        die("Error retrieving password: `{command}` returned '{error}'".format(command=command, error=p.stderr.read().strip()))

def die(error_msg):
    print error_msg
    sys.exit(1)

def run(command):
    print command
    p = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
    p.wait()
    if p.returncode != 0:
        # die("Error running command.\nCommand: `{command}`\nReturned:\n\n'{error}'\n\n".format(command=command, error=p.stderr.read().strip()))
        return False
    return True

def demote(issues):
    for issue in issues:
        run("task jiraid:%s mod due:" % str(issue.key))

def promote(issues):
    for issue in issues:
        close_date = parse_sprint_close(issue)
        run("task jiraid:%s mod priority:M due:%s rc.dateformat:Y-M-DTH:N:S" % (str(issue.key), close_date))


