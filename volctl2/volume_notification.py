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

try:
    import alsaaudio
except:
    print "Error: need python-pyalsaaudio"
try:
    import pygtk
    import pynotify
    pygtk.require('2.0')
except:
    print "Error: need python-notify, python-gtk2 and gtk"


class VolumeNotification():

    def __init__(self):
        self._notification = pynotify.Notification("Volume", self.get_volume(), "audio-volume-medium")
        self._notification.add_action("increase", "+", self.increase_volume)
        self._notification.add_action("decrease", "-", self.decrease_volume)
        self._notification.add_action("mute", "Mute", self.toggle_mute)
        self._notification.show()

    def get_volume(self):
        volume = str(alsaaudio.Mixer().getvolume()[0])
        return volume + "%"

    def alter_volume(self, delta):
        previous_volume = long(alsaaudio.Mixer().getvolume()[0])

        new_volume = long(previous_volume + long(delta))
        print 'Volume was {}, setting to : {}'.format(previous_volume, new_volume)
        if new_volume > 100:
            new_volume = 100
        if new_volume < 0:
            new_volume = 0

        alsaaudio.Mixer().setvolume(new_volume)
        self.update()

    def increase_volume(self, notification=None, action=None, data=None):
        self.alter_volume(3L)

    def decrease_volume(self, notification=None, action=None, data=None):
        self.alter_volume(-3L)

    def toggle_mute(self, notification=None, action=None, data=None):
        if alsaaudio.Mixer().getmute()[0] == 0:
            alsaaudio.Mixer().setmute(1)
        elif alsaaudio.Mixer().getmute()[0] == 1:
            alsaaudio.Mixer().setmute(0)
        self.update()

    def update(self):
        if alsaaudio.Mixer().getmute()[0] == 0:
            self._notification.update("Volume", self.get_volume(), "audio-volume-medium")
        elif alsaaudio.Mixer().getmute()[0] == 1:
            self._notification.update("Volume", self.get_volume() + " (Muted)", "audio-volume-muted")
        self._notification.show()
