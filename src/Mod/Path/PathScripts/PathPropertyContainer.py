# -*- coding: utf-8 -*-
# ***************************************************************************
# *   Copyright (c) 2020 sliptonic <shopinthewoods@gmail.com>               *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

import FreeCAD
import PySide

__title__ = 'Generic property container to store some values.'
__author__ = 'sliptonic (Brad Collette)'
__url__ = 'https://www.freecadweb.org'
__doc__ = 'A generic container for typed properties in arbitrary categories.'

def translate(context, text, disambig=None):
    return PySide.QtCore.QCoreApplication.translate(context, text, disambig)


class PropertyContainer(object):
    '''Property container object.'''

    CustomPropertyGroups       = 'CustomPropertyGroups'
    CustomPropertyGroupDefault = 'User'

    def __init__(self, obj):
        self.obj = obj
        obj.addProperty('App::PropertyStringList', self.CustomPropertyGroups, 'Base', PySide.QtCore.QT_TRANSLATE_NOOP('PathPropertyContainer', 'List of custom property groups'))
        obj.setEditorMode(self.CustomPropertyGroups, 2)  # hide

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        for obj in FreeCAD.ActiveDocument.Objects:
            if hasattr(obj, 'Proxy') and obj.Proxy == self:
                self.obj = obj
                obj.setEditorMode(self.CustomPropertyGroups, 2)  # hide
                break
        return None

    def onDocumentRestored(self, obj):
        obj.setEditorMode(self.CustomPropertyGroups, 2)  # hide

    def getCustomProperties(self):
        '''Return a list of all custom properties created in this container.'''
        return [p for p in self.obj.PropertiesList if self.obj.getGroupOfProperty(p) in self.obj.CustomPropertyGroups]

    def addCustomProperty(self, propertyType, name, group=None, desc=None):
        '''addCustomProperty(propertyType, name, group=None, desc=None) ... adds a custom property and tracks its group.'''
        if desc is None:
            desc = ''
        if group is None:
            group = self.CustomPropertyGroupDefault
        groups = self.obj.CustomPropertyGroups
        if not group in groups:
            groups.append(group)
            self.obj.CustomPropertyGroups = groups
        self.obj.addProperty(propertyType, name, group, desc)

def Create(name = 'PropertyContainer'):
    obj = FreeCAD.ActiveDocument.addObject('App::FeaturePython', name)
    obj.Proxy = PropertyContainer(obj)
    return obj

def IsPropertyContainer(obj):
    '''Returns True if the supplied object is a property container (or its Proxy).'''

    if type(obj) == PropertyContainer:
        return True
    if hasattr(obj, 'Proxy'):
        return IsPropertyContainer(obj.Proxy)
    return False
