from Components.VariableText import VariableText
from enigma import eLabel
from Renderer import Renderer

class valioPosition(Renderer, VariableText):

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)

    GUI_WIDGET = eLabel

    def changed(self, what):
        orb_pos = self.suspended or ' '
        service = self.source.service
        feinfo = service and service.frontendInfo()
        if feinfo is not None:
            if feinfo:
                frontendData = feinfo.getAll(True)
                if frontendData is not None:
                    if frontendData.get('tuner_type') == 'DVB-S':
                        orbital_pos = int(frontendData['orbital_position'])
                        if orbital_pos > 1800:
                            orb_pos = str(float(3600 - orbital_pos) / 10.0) + '\xb0W'
                        elif orbital_pos > 0:
                            orb_pos = str(float(orbital_pos) / 10.0) + '\xb0E'
                    elif frontendData.get('tuner_type') == 'DVB-T':
                        orb_pos = 'DVB-T'
                    elif frontendData.get('tuner_type') == 'DVB-C':
                        orb_pos = 'DVB-C'
            self.text = orb_pos

    def onShow(self):
        self.suspended = False
        self.changed(None)

    def onHide(self):
        self.suspended = True

