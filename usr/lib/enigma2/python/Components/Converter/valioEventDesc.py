# Source Generated with Decompyle++
# File: valioEventDesc.pyo (Python 2.6)

from Components.Converter.Converter import Converter
from Components.Element import cached

class valioEventDesc(Converter, object):
    NAME = 0
    SHORT_DESCRIPTION = 1
    EXTENDED_DESCRIPTION = 2
    ID = 3
    FULL = 4
    
    def __init__(self, type):
        Converter.__init__(self, type)
        if type == 'Description':
            self.type = self.SHORT_DESCRIPTION
        elif type == 'ExtendedDescription':
            self.type = self.EXTENDED_DESCRIPTION
        elif type == 'ID':
            self.type = self.ID
        elif type == 'Full':
            self.type = self.FULL
        else:
            self.type = self.NAME

    
    def getText(self):
        event = self.source.event
        if event is None:
            return ''
        if self.type == self.NAME:
            return event.getEventName()
        if self.type == self.SHORT_DESCRIPTION:
            return event.getShortDescription()
        if self.type == self.EXTENDED_DESCRIPTION:
            return event.getExtendedDescription()
        if self.type == self.ID:
            return str(event.getEventId())
        if self.type == self.FULL:
            text = ''
            short = event.getShortDescription()
            ext = event.getExtendedDescription()
            if short and short != text:
                text += short
            
            if ext:
                if text:
                    text += '\n'
                
                text += ext
            
            return text

    getText = cached(getText)
    text = property(getText)

