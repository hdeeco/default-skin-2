from Components.VariableText import VariableText
from Components.Sensors import sensors
from Tools.HardwareInfo import HardwareInfo
from enigma import eLabel
from Renderer import Renderer

class valioSystem(Renderer, VariableText):

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)
        if '8000' in HardwareInfo().get_device_name() or '500' in HardwareInfo().get_device_name() or '800se' in HardwareInfo().get_device_name():
            self.ZeigeTemp = True
        else:
            self.ZeigeTemp = False

    GUI_WIDGET = eLabel

    def changed(self, what):
        if not self.suspended:
            maxtemp = 0
            try:
                templist = sensors.getSensorsList(sensors.TYPE_TEMPERATURE)
                tempcount = len(templist)
                for count in range(tempcount):
                    id = templist[count]
                    tt = sensors.getSensorValue(id)
                    if tt > maxtemp:
                        maxtemp = tt

            except:
                pass

            loada = 0
            try:
                out_line = open('/proc/loadavg').readline()
                loada = out_line[:4]
            except:
                pass

            fan = 0
            try:
                fanid = sensors.getSensorsList(sensors.TYPE_FAN_RPM)[0]
                fan = sensors.getSensorValue(fanid)
            except:
                pass

            if self.ZeigeTemp:
                self.text = 'cpu ' + loada + '\ntmp ' + str(maxtemp) + '\xb0C\nfan ' + str(int(fan / 2))
            else:
                self.text = 'cpu loads\n' + loada

    def onShow(self):
        self.suspended = False
        self.changed(None)

    def onHide(self):
        self.suspended = True

