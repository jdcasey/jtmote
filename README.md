# JTmote - JIRA-to-Taskwarrior Task Promotion/Demotion

JTmote is designed to follow a bugwarrior synchronization between JIRA and taskwarrior, when JIRA/Greenhopper agile planning is in use. After bugwarrior synchronizes issues across, it doesn't adjust priorities or due dates in response to the currenly open sprint. JTmote fills this gap.

Essentially, when a new sprint is started anything leftover from the old sprint should be demoted in priority and its due date should be erased...unless it was included in the new sprint. For other issues that are included in the new sprint, their priority should be increased and their due date synchronized with the sprint end date, so taskwarrior will sort them to the top of the stack.

JTmote does two JIRA queries: one for issues that are not in a currently open sprint, and another for issues in the currently open sprints. The queries also filter issues to return those assigned to the current user (the authenticated user). These two groups of issues are then adjusted as described above.

## Prerequisites

* Taskwarrior, obviously
* Bugwarrior, obviously
* `pass`, the Linux command-line password manager
* `gpg`, to support `pass`

## Configuration

JTmote assumes you're keeping your JIRA password safe using the `pass` utility. To do this, you'll need to setup a GPG key for encrypting/decrypting the password. Then, you can store your password using:

```
$ pass init <GPG-private-key-id>  # NOTE: Only do this once!
$ pass insert <jira-password-key>
<type the password twice>
```

To make jtmote work, you should create a YAML configuration file under `$HOME/.config/jtmote/config.yml`, and add the following entries:

```
url: <jira-base-url>
user: <jira-username>
passkey: <key in pass that contains jira password>
```

## Self-Signed SSL and Python `requests`

The requests library contains its own cacerts.pem file, which contains the list of SSL root CAs it uses to validate SSL connections. If you're using your own CA, or a self-signed certificate, you'll need to redirect the requests library to look elsewhere for the CA list. You can accomplish this by setting the `REQUESTS_CA_BUNDLE`. 

On my CentOS machine, I added the following to my `$HOME/.bash_profile` file:

```
export REQUESTS_CA_BUNDLE=/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
```

