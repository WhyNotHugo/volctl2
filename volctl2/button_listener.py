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

from Xlib import X, display
from Xlib.ext import record
from Xlib.protocol import rq
from volume_modifier import VolumeModifierThread

import threading
import sys


class MouseButtonListener(threading.Thread):
    """
    Thread that listens to mouse buttons presses.
    """

    volume_modifier = None
    display = None
    notification = None

    def __init__(self, notification):
        super(MouseButtonListener, self).__init__()
        self.volume_modifier = VolumeModifierThread(notification)
        self.notification = notification

        self.display = display.Display()
        if not self.display.has_extension("RECORD"):
            print("RECORD extension not found")
            sys.exit(-1)

        r = self.display.record_get_version(0, 0)
        print("RECORD extension version %d.%d" % (r.major_version, r.minor_version))

    def run(self):
        ctx = self.display.record_create_context(
                0,
                [record.AllClients],
                [{
                        'core_requests': (0, 0),
                        'core_replies': (0, 0),
                        'ext_requests': (0, 0, 0, 0),
                        'ext_replies': (0, 0, 0, 0),
                        'delivered_events': (0, 0),
                        'device_events': (X.ButtonPress, X.ButtonRelease),
                        'errors': (0, 0),
                        'client_started': False,
                        'client_died': False,
                }])

        # Enable the context; this only returns after a call to record_disable_context,
        # while calling the callback function in the meantime
        self.display.record_enable_context(ctx, self.callback)

        # Finally free the context
        self.display.record_free_context(ctx)

    def callback(self, reply):
        if reply.category != record.FromServer:
            return
        if reply.client_swapped:
            print("* received swapped protocol data, cowardly ignored")
            return
        if not len(reply.data) or ord(reply.data[0]) < 2:
            return  # not an event

        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data, self.display.display, None, None)

            if event.detail not in [10, 13]:
                return
            if event.type == X.ButtonPress:
                if not self.volume_modifier.is_alive():
                    self.volume_modifier = VolumeModifierThread(self.notification)
                if event.detail == 10:
                    self.volume_modifier.delta = -3
                elif event.detail == 13:
                    self.volume_modifier.delta = +3
                if not self.volume_modifier.is_alive():
                    self.volume_modifier.start()
            elif event.type == X.ButtonRelease and event.detail in [10, 13]:
                if self.volume_modifier.is_alive():
                    self.volume_modifier.stop()
