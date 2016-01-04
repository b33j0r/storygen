#! /usr/bin/env python
from __future__ import (absolute_import, division, print_function, unicode_literals)

import os


def project_path(*parts):
    this_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(this_dir, "..", "..", "..", *parts))
