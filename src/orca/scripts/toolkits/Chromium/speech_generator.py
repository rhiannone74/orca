# Orca
#
# Copyright 2018 Igalia, S.L.
#
# Author: Joanmarie Diggs <jdiggs@igalia.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., Franklin Street, Fifth Floor,
# Boston MA  02110-1301 USA.

"""Custom speech generator for Chromium."""

# Please note: ATK support in Chromium needs much work. Until that work has been
# done, Orca will not be able to provide access to Chromium. This generator is a
# work in progress.

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2018 Igalia, S.L."
__license__   = "LGPL"

import pyatspi

from orca import debug
from orca import orca_state
from orca.scripts import web


class SpeechGenerator(web.SpeechGenerator):

    def __init__(self, script):
        super().__init__(script)

    def generateSpeech(self, obj, **args):
        if self._script.utilities.inDocumentContent(obj):
            return super().generateSpeech(obj, **args)

        oldRole = None
        if self._script.utilities.treatAsMenu(obj):
            msg = "CHROMIUM: HACK? Speaking menu item as menu %s" % obj
            debug.println(debug.LEVEL_INFO, msg, True)
            oldRole = self._overrideRole(pyatspi.ROLE_MENU, args)

        result = super().generateSpeech(obj, **args)
        if oldRole is not None:
            self._restoreRole(oldRole, args)

        return result