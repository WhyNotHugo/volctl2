#!/usr/bin/env python2

# -*- coding: utf-8 -*-

# Copyright (c) 2012 Hugo Osvaldo Barrera <hugo@osvaldobarrera.com.ar>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from listener import MouseButtonListener, MediaKeyListener
from volume_notification import VolumeNotification

from Xlib import display
from threading import Thread
import sys

import json
import os
from xdg import BaseDirectory

try:
    import gtk
    import pygtk
    import pynotify
    pygtk.require('2.0')
except:
    print("Error: need python-notify, python-gtk2 and gtk")

__version__ = "2.0.0"

config_file = os.path.join(BaseDirectory.xdg_config_home,
                           "volctl2/settings.json")
if os.path.exists(config_file):
    config = json.load(open(config_file))
    cardindex = config["cardindex"]
else:
    cardindex = 0


class GtkThread(Thread):
    """
    This thread needs to run separately to handle button clicks on the volume
    """
    def __init__(self):
        super(GtkThread, self).__init__()
        gtk.gdk.threads_init()

    def run(self):
        gtk.main()


def run():
    print("Volume Control v{}".format(__version__))

    if not pynotify.init("Volume Control v{}".format(__version__)):
        sys.exit(1)

    if not display.Display().has_extension("RECORD"):
        print("RECORD extension not found")
        sys.exit(1)

    notification = VolumeNotification(cardindex=cardindex)
    MouseButtonListener(notification).start()
    MediaKeyListener(notification).start()
    GtkThread().start()


if __name__ == "__main__":
    run()
