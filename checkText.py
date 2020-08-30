# coding: utf8

##Copyright (c) 2017 Лобов Евгений
## <ewhenel@gmail.com>
## <evgenel@yandex.ru>

## This file is part of txt_to_XLgraphs.
##
##    txt_to_XLgraphs is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    txt_to_XLgraphs is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with txt_to_XLgraphs.  If not, see <http://www.gnu.org/licenses/>.
##
##  (Этот файл — часть txt_to_XLgraphs.
##
##   txt_to_XLgraphs - свободная программа: вы можете перераспространять ее и/или
##   изменять ее на условиях Стандартной общественной лицензии GNU в том виде,
##   в каком она была опубликована Фондом свободного программного обеспечения;
##   либо версии 3 лицензии, либо (по вашему выбору) любой более поздней
##   версии.
##
##   txt_to_XLgraphs распространяется в надежде, что она будет полезной,
##   но БЕЗО ВСЯКИХ ГАРАНТИЙ; даже без неявной гарантии ТОВАРНОГО ВИДА
##   или ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННЫХ ЦЕЛЕЙ. Подробнее см. в Стандартной
##   общественной лицензии GNU.
##
##   Вы должны были получить копию Стандартной общественной лицензии GNU
##   вместе с этой программой. Если это не так, см.
##   <http://www.gnu.org/licenses/>.)

# coding: utf8

import re
import io
import sys
from definedExceptions import *

class FileChecker:

	def __init__(self):
		self.textStruct = None
		self.patterns = None
		self.elemCollect = []
		self.periodEnd = None
		self.periodStart = None
		self.reList = None
		self.structName = None
		self.dateFlag = None
		self.internFormat = None

	def loadPatterns(self):
		try:
			fileObj = io.open("structure_patterns.txt", mode="r", encoding="utf-8")
			self.patterns = fileObj.read()
			fileObj.close()
		except:
			raise loadFileError("<<load file error>>", "\r\n    Файл 'structure_patterns.txt' не загружается!\r\nВот:" + str(sys.exc_info()[1]))

	def compilePatterns(self):
		try:
			regKeyCount = re.compile(r"^(?:[\t]|[\s])*key[:]", re.MULTILINE)
			resKeyCount = regKeyCount.findall(self.patterns)
			if len(resKeyCount) == 0:
				raise parseFileError("<<no keys error>>", "\r\n    Ни одного ключа формата в файле \'structure_patterns.txt\'")
			regNameCount = re.compile(r"^(?:[\t]|[\s])*name[:]", re.MULTILINE)
			resNameCount = regNameCount.findall(self.patterns)
			regPatternCount = re.compile(r"^(?:[\t]|[\s])*pattern[:]", re.MULTILINE)
			resPatternCount = regPatternCount.findall(self.patterns)
			if (len(resPatternCount) != len(resKeyCount)) or (len(resNameCount) != len(resKeyCount)):
				raise parseFileError("<<missed statement error>>", "\r\n    Не запелнено(коммент) значение для key:, name:, pattern: в файле \'structure_patterns.txt\'")
			regCompl = re.compile(r"^(?:[\t]|[\s])*key:.+?[#]", re.DOTALL|re.MULTILINE)
			resCompl = regCompl.findall(self.patterns)
			for j in resCompl:
				regComplComm = re.compile(r"^(?:[\t]|[\s])*pattern:.", re.MULTILINE)
				resComplComm = regComplComm.findall(j)
				if len(resComplComm) == 0:
					raise parseFileError("<<statements misplaced error>>", "\r\n    Не все key:, name:, pattern: заполнены для формата в файле \'structure_patterns.txt\'")
			regGetKeys = re.compile(r"^(?:[\t]|[\s])*key[:](?:[\t]|[\s])*[<](.*?)[>]\n", re.DOTALL|re.MULTILINE)
			resGetKeys = regGetKeys.findall(self.patterns)
# Непонятное поведение - далее коллекция reList сортируется произвольным образом
# Повторный вызов списка, покольку с принтом срабатывает
			tmpVar = resGetKeys
			del tmpVar
			regGetNames = re.compile(r"^(?:[\t]|[\s])*name[:](?:[\t]|[\s])*[<](.*?)[>]\n", re.DOTALL|re.MULTILINE)
			resGetNames = regGetNames.findall(self.patterns)
			regGetPatterns = re.compile(r"^(?:[\t]|[\s])*pattern[:](?:[\t]|[\s])*\<regular_start\>(.*?)\<regular_end\>\n", re.DOTALL|re.MULTILINE)
			resGetPatterns = regGetPatterns.findall(self.patterns)
			for i in resGetPatterns:
				try:
					regTest = re.compile(i, re.MULTILINE)
				except:
					raise compileRegError(str(sys.exc_info()[0])+" "+str(sys.exc_info()[1]), "\r\n"+i)
			self.reList = {item:resGetPatterns[resGetKeys.index(item)] for item in resGetKeys}
			self.structName = {item:resGetNames[resGetKeys.index(item)] for item in resGetKeys}
			self.structName[None] = 'Неизвестно'
		except:
			raise

	def loadText(self, text="test"):
		self.textToTest = text

	def getFormat(self):
		self.elemCollect = []
		self.textStruct = None
		tmpReList = self.reList.copy()
#Почему-то не точно определяется формат, берется общий из конца списка, хотя первый из примера подходит
#Почему-то добавлением доп. команды после копирования списка нормально, добавлено pass
		pass
		while (self.textStruct is None) and (len(tmpReList.keys()) > 0):
			keyStruct, regValue = tmpReList.popitem()
			regString = re.compile(regValue)
			if regString.search(self.textToTest) is not None:
				self.textStruct = keyStruct
				tmpReList = {}
			else:
				self.textStruct = None

	def prepCsvAndTsv(self):
		delQuot = re.compile(r"\"", re.M)
		insTab = re.compile(r"\",\"", re.M)
		text = insTab.sub(r"\t", self.textToTest)
		self.textToTest = text
		text = delQuot.sub(r"", self.textToTest)
		self.textToTest = text

	def getDelimDateFormat(self):
		passFRow = re.compile(r".*(\n|\r\n)")
		resFRow = passFRow.search(self.textToTest)
		saveHeaders = resFRow.group(0)
		self.textToTest = passFRow.sub(r"", self.textToTest, count=1)
		delDate = re.compile(r"^([\"]?)[0-9]{2}[/\-\\]{1}[0-9]{2}[/\-\\]{1}[0-9]{2,4}\s", re.M)
		delDifDate = re.compile(r"^([\"]?)[0-9]{2,4}[/\-\\]{1}[0-9]{2}[/\-\\]{1}[0-9]{2}\s", re.M)
		timePart = re.compile(r"^[\"]?[\d]{2}:[\d]{2}:[\d]{2}", re.M)
		delMilSec = re.compile(r"^([\"]?[\d]{2}:[\d]{2}:[\d]{2})[\.][0-9]{3}", re.M)
		ifComQuot = re.compile(r"\",\"")
		inQuotNum = re.compile(r"(?<=[\"][,][\"]).*?(?=[\"][,]?[\"]?)", re.DOTALL)
		ifTabSep = re.compile(r"\t")
		btTabVal = re.compile(r"(?<=[\t]).*?(?=[\t]|\n)", re.DOTALL)
		resTabSep = ifTabSep.findall(self.textToTest)
		resTabVal = btTabVal.findall(self.textToTest)
		resDatePart = delDate.findall(self.textToTest)
		resDDatePart = delDifDate.findall(self.textToTest)
		resComQuot = ifComQuot.findall(self.textToTest)
		resQuotNum = inQuotNum.findall(self.textToTest)
		if len(resDatePart)!=0:
			text = delDate.sub(r"\1", self.textToTest)
			self.textToTest = text
		if len(resDDatePart)!=0:
			text = delDifDate.sub(r"\1", self.textToTest)
			self.textToTest = text
		resTimePart = timePart.findall(self.textToTest)
		if len(resTimePart)!=0:
			self.dateFlag=1
		else:
			self.dateFlag=0
		resMilSec = delMilSec.findall(self.textToTest)
		if len(resMilSec)!=0:
			text = delMilSec.sub(r"\1", self.textToTest)
			self.textToTest = text
		if (len(resComQuot)!=len(resQuotNum)) or (len(resTabSep)!=len(resTabVal)):
			raise columnSplitError("<<data column error>>", "\r\n    Похоже, в загружаемом файле данные слиплись/рассыпались")
		if (len(resComQuot)==0) and (len(resTabSep)==0):
			raise columnSplitError("<<wrong delimiters>>", "\r\n    Неразделенный текст (запятая и кавычки)/файл открылся по ошибке(регулярное выражение)")
		if len(resComQuot)>len(resTabSep):
			self.internFormat = "csv"
		else:
			self.internFormat = "tsv"
		self.textToTest = saveHeaders + self.textToTest

	def textToStruct(self):
		self.getDelimDateFormat()
#		self.elemCollect.clear()
# python 2.7 ho method clear()
		self.elemCollect = []
		if self.internFormat == "csv":
			self.prepCsvAndTsv()
		regRows = re.compile(r".+")
		iterRows = regRows.findall(self.textToTest)
		regElem = re.compile(r"[\t]")
		for i in iterRows:
			self.elemCollect.append(regElem.split(i))

	def detalTime(self):
		if len(self.elemCollect) > 0:
			self.periodStart = self.elemCollect[1][0]
			self.periodEnd = self.elemCollect[len(self.elemCollect)-1][0]
		else:
			self.periodStart = None
			self.periodEnd = None

	def attrReturn(self):
		return self.structName.get(self.textStruct)
