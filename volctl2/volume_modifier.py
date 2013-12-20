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

import threading
import time


class VolumeModifierThread(threading.Thread):
    """
    A thread that alters the volume by a certain delta every 100ms, until
    stopped, or the limit is reached; whichever comes first.
    """

    stop = False
    delta = None
    volume = None

    def __init__(self, volume_control):
        super(VolumeModifierThread, self).__init__()
        self.volume = volume_control

    def run(self):
        self._stop = False
        while not self._stop:
            self.change_volume(self.delta)
            self.delta = self.delta * 1.2
            time.sleep(0.1)

    def change_volume(self, delta):
        previous_volume = self.volume.get_volume()

        new_volume = long(previous_volume + delta)
        if new_volume > 100:
            new_volume = 100
        if new_volume < 0:
            new_volume = 0
        print('Delta is {}, volume was {}, setting to : {}'.format(delta,
              previous_volume, new_volume))

        if previous_volume == 100 and delta > 0:
            print("Volume is 100 and requested increase; stopping.")
            self.stop()
        if previous_volume == 0 and delta < 0:
            print("Volume is 0 and requested decrease; stopping.")
            self.stop()

        self.volume.set_volume(new_volume)

    def toggle_mute(self):
        self.volume.toggle_mute()

    def stop(self):
        self._stop = True
