# -*- Mode: Python; test-case-name: flumotion.test.test_feedcomponent010 -*-
# vi:si:et:sw=4:sts=4:ts=4

# Flumotion - a streaming media server
# Copyright (C) 2004,2005,2006,2007,2008,2009 Fluendo, S.L.
# Copyright (C) 2010,2011 Flumotion Services, S.A.
# All rights reserved.
#
# This file may be distributed and/or modified under the terms of
# the GNU Lesser General Public License version 2.1 as published by
# the Free Software Foundation.
# This file is distributed without any warranty; without even the implied
# warranty of merchantability or fitness for a particular purpose.
# See "LICENSE.LGPL" in the source distribution for more information.
#
# Headers in this file shall remain intact.

"""
Properties tab in the component UI
"""

import gettext
import os

import gtk
import gobject

from flumotion.component.base.baseadminnode import BaseAdminGtkNode

_ = gettext.gettext
__version__ = "$Rev$"


class PropertiesAdminGtkNode(BaseAdminGtkNode):
    gladeFile = os.path.join('flumotion', 'component', 'base',
        'properties.glade')

    uiStateHandlers = None
    _properties = {}

    def __init__(self, state, admin):
        BaseAdminGtkNode.__init__(self, state, admin, title=_("Properties"))

    def haveWidgetTree(self):
        self.widget = gtk.VBox()
        self.widget.set_border_width(6)

        self.properties = gtk.TreeView(gtk.TreeStore(
            gobject.TYPE_STRING, gobject.TYPE_STRING))
            #[Column('name'),
            # Column('value')])
        #self.properties.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        self.widget.pack_start(self.properties, False, False)

        self._reloadProperties(self.state.get('config')['properties'])
        return self.widget

    # IStateListener Interface

    def stateSet(self, object, key, value):
        if key == 'properties':
            self._reloadProperties(value)

    ### Private methods

    def _reloadProperties(self, properties):
        if properties is None:
            return
        propertyNames = properties.keys()[:]
        propertyNames.sort()
        properties_model = self.properties.get_model()
        tIter = properties_model.get_iter_first()
        for ind, name in enumerate(propertyNames):
            if tIter is not None:
                properties_model.set_value(tIter, ind, properties[name])
                tIter = properties_model.iter_next(tIter)
            else:
                properties_model.append(None, [name, properties[name]])
