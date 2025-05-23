# Copyright (C) 2012 Canonical Ltd.
# Copyright (C) 2012, 2013 Hewlett-Packard Development Company, L.P.
# Copyright (C) 2012 Yahoo! Inc.
#
# Author: Scott Moser <scott.moser@canonical.com>
# Author: Juerg Haefliger <juerg.haefliger@hp.com>
# Author: Joshua Harlow <harlowja@yahoo-inc.com>
#
# This file is part of cloud-init. See LICENSE file for license information.

import logging

from cloudinit import util
from cloudinit.distros.parsers.sys_conf import SysConf

LOG = logging.getLogger(__name__)


# Helper function to update a RHEL/SUSE /etc/sysconfig/* file
def update_sysconfig_file(fn, adjustments, allow_empty=False):
    if not adjustments:
        return
    (exists, contents) = read_sysconfig_file(fn)
    updated_am = 0
    for k, v in adjustments.items():
        if v is None:
            continue
        v = str(v)
        if (not v) and (not allow_empty):
            continue
        contents[k] = v
        updated_am += 1
    if updated_am:
        lines = [
            str(contents),
        ]
        if not exists:
            lines.insert(0, util.make_header())
        util.write_file(fn, "\n".join(lines) + "\n", 0o644)


# Helper function to read a RHEL/SUSE /etc/sysconfig/* file
def read_sysconfig_file(fn):
    exists = False
    try:
        contents = util.load_text_file(fn).splitlines()
        exists = True
    except IOError:
        contents = []
    return (exists, SysConf(contents))
