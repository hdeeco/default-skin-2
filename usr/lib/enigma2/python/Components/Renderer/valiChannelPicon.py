# -*- coding: utf-8 -*-
import os
from Renderer import Renderer
from enigma import ePixmap
from enigma import ePixmap, ePicLoad
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename

PICON_FILE = "picon_default"

class valiChannelPicon(Renderer):
	searchPaths = ('/%s/', '/media/hdd/%s/', '/media/usb/%s/', '/media/usb2/%s/', '/media/usb3/%s/', '/media/card/%s/', '/media/cf/%s/', '/etc/%s/', '/usr/share/enigma2/%s/')
		
	def __init__(self):
		Renderer.__init__(self)
		self.PicLoad = ePicLoad()
		self.PicLoad.PictureData.get().append(self.updatePicon)
		self.piconsize = (0,0)
		self.path = "picon"
		self.nameCache = { }
		self.pngname = ""

	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "path":
				self.path = value
			else:
				attribs.append((attrib,value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap

	def updatePicon(self, picInfo=None):
		ptr = self.PicLoad.getData()
		if ptr is not None:
			self.instance.setPixmap(ptr.__deref__())
			self.instance.show()
			
	def changed(self, what):
		if self.instance:
		      pngname = ""
		      if what[0] != self.CHANGED_CLEAR:
			      service = self.source.service
			      sname = service.toString()
			      # strip all after last :
			      pos = sname.rfind(':')
			      if pos != -1:
				      sname = sname[:pos].rstrip(':').replace(':','_')
			      pngname = self.nameCache.get(sname, "")
			      if pngname == "":
				      pngname = self.findPicon(sname)
				      if pngname != "":
					      self.nameCache[sname] = pngname
		      if pngname == "": # no picon for service found
			      pngname = self.nameCache.get("default", "")
			      if pngname == "": # no default yet in cache..
				      pngname = self.findPicon(PICON_FILE)
				      if pngname == "":
					      tmp = resolveFilename(SCOPE_CURRENT_SKIN, PICON_FILE + ".png")
					      if fileExists(tmp):
						      pngname = tmp
					      else:
						      pngname = resolveFilename(SCOPE_SKIN_IMAGE, PICON_FILE)
				      self.nameCache["default"] = pngname
		      if self.pngname != pngname:
			      if pngname:
				      self.PicLoad.setPara((100, 60, 0, 0, 1, 1, "#FF000000"))
				      self.PicLoad.startDecode(pngname)
			      else:
				      self.instance.hide()
			      self.pngname = pngname


	def findPicon(self, serviceName):
		for path in self.searchPaths:
			pngname = (path % self.path) + serviceName + ".png"
			if fileExists(pngname):
				return pngname
		return ""
