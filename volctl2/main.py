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

from button_listener import MouseButtonListener
from volume_notification import VolumeNotification

import sys

try:
    import gtk
    import pygtk
    import pynotify
    pygtk.require('2.0')
except:
    print "Error: need python-notify, python-gtk2 and gtk"


if not pynotify.init("Volume Control v2.0"):
    sys.exit(1)

notification = VolumeNotification()

MouseButtonListener(notification).start()

gtk.gdk.threads_init()
gtk.main()
