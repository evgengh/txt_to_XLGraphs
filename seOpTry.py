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

import os
import tkinter
import datetime
import re
from tkinter import ttk
from checkText import FileChecker
from textToTable import ConvertToXL
from definedExceptions import *
import io
import sys

class SearchFile(tkinter.Frame):

	def __init__(self):
## Нужно вернуться в основную директорию приложения
## бинарник для запуска приложения должен быть в одной директории с библиотеками
## тут можно не править весь код на предмет os.chdir(...), а положить файл к библиотекам
## и добавить символьную ссылку из корня. Особенности Linux+PyInstaller+_tkinter
###		os.chdir('../')
##
		tkinter.Frame.__init__(self, master=None)
		self.pack()
		self.mainForm()
		self.loadSide()
		self.loadAdd()
# какие-то трудности с импортом zipimport при работе с функциями даты времени, 
# если предварительно было снавигировано за пределы корневого каталога программы
# Такая ситуация наблюдается в уе сбилдинном проекте
# Попытка дернуть методы датывремени до загрузки элементов навиганции
		tmpVar = datetime.datetime.strptime('01/13/17', '%x')
		del tmpVar

	def mainForm(self):
		self.mainFrame = tkinter.Frame(master=self, background="#778899")
		self.mainFrame.pack()
		self.upButFr = tkinter.Frame(master=self.mainFrame, background="#778899")
		self.upButFr.pack(side="top")
		self.bOpen = tkinter.Button(master=self.upButFr)
		self.bOpen["text"] = "Искать_*"
		self.bOpen["command"] = self.pathSearch
		self.bWhat = tkinter.Button(master=self.upButFr, text="Для чего>?>", command=self.helpAndInfo)
		self.bOpen.pack(side="left", anchor="nw")
		self.bWhat.pack(side="left", anchor="ne")
		self.lowButFr = tkinter.Frame(self.mainFrame, borderwidth=1, background="#778899")
		self.lowButFr.pack(side="bottom")
		self.fillerFrame = tkinter.Frame(master=self.mainFrame)
		self.fillerFrame.pack(side="left", anchor="center")
		self.osFrame = tkinter.Frame(master=self.fillerFrame, background="#778899")
		print(os.getcwd())
		self.gplPng = tkinter.PhotoImage(file="license/velosph_sm_cmx.png")
		self.titleWin = tkinter.Text(master=self.fillerFrame, background = "#F0F8FF", font=("Times", 11, "italic"))
		titleText = "Из истории:\n\tИдею электронных таблиц впервые сформулировал американский учёный\n\tавстрийского происхождения"
		titleText = titleText + "Рихард Маттезих (нем. Richard Mattesich),\n\tопубликовав в 1961 г. исследование под названием"
		titleText = titleText + "\n\t«Budgeting Models and System Simulation»[3].\n\tКонцепцию дополнили в 1970 г. Пардо (англ. Rene Pardo)"
		titleText = titleText + "\n\tи Ландау (англ. Remy Landau)...\nМатериал из WikiPedia.org"
		self.titleWin.insert(index="end", chars=titleText)
		self.titleWin.pack(side="left", anchor="center")
		self.infoWin = tkinter.Frame(master=self.fillerFrame)
		self.gplLabel = tkinter.Label(master=self.infoWin, image=self.gplPng)
		self.gplLabel.pack(side="bottom", anchor="center")
		self.bQuit = tkinter.Button(master=self.lowButFr, text="Завершить&", command=self.quit)
		self.bQuit.pack(side="left", anchor="nw")
		self.bOperate = tkinter.Button(master=self.lowButFr, text="Работать-->", state="disabled", command=self.workOperations)
		self.bOperate.pack(side="left", anchor="ne")

	def handleFormErr(self, errText="Error: Empty exception"):
		titleSlaves = self.fillerFrame.pack_slaves()
		for jWidget in titleSlaves:
			jWidget.pack_forget()
		allSlaves = self.mainFrame.pack_slaves()
		for jButton in allSlaves:
			if jButton not in (self.fillerFrame, self.upButFr, self.lowButFr):
				jButton.pack_forget()
		self.titleWin.delete(index1="1.0", index2="end")
		self.titleWin.insert(index="end", chars=errText)
		self.titleWin.config(fg="red")
		self.titleWin.pack()
		self.bOpen.config(state="disabled")
		self.bWhat.config(state="disabled")
		self.bOperate.config(state="disabled")

	def loadSide(self):
		self.helpText = "Место для файла помощи"
		self.licenseText = "Место для файла лицензии"
		self.authorText = "Место для авторской странички"
		self.errString = "### НЕЖЕЛАТЕЛЬНО, НО ВЕРОЯТНО (ошибка) ###:\r\n"
		regLicense1 = re.compile(r"(Евгений[\s]Лобов)")
		regLicense2 = re.compile(r"(Evgeny[\s]Lobov)")
		regLicense3 = re.compile("ewhenel@gmail.com")
		regLicense4 = re.compile("evgenel@yandex.ru")
		regLicense5 = re.compile("txt_to_XLgraphs")
		regLicense6 = re.compile("http://www.gnu.org/licenses/")
		regAuthor1 = re.compile("\W{1}")
		regAuthor2 = re.compile("\w{1}")
		regHelp1 = re.compile("ФАЙЛЫ\n[\-]{28}")
		regHelp2 = re.compile("УСТАНОВКА\n[\-]{28}")
		regHelp3 = re.compile("РАБОТА С ПРИЛОЖЕНИЕМ\n[\-]{28}")
		regHelp4 = re.compile("ИНТЕРФЕЙС ПРИЛОЖЕНИЯ\n[\-]{28}")
		regHelp5 = re.compile("ОСОБЕННОСТИ\s[\(]масштабируемость[\)]\n[\-]{28}")
		regHelp6 = re.compile("ОГРАНИЧЕНИЯ\n[\-]{28}")
		regHelp7 = re.compile("ЛИЦЕНЗИЯ\n[\-]{28}")
		regHelp8 = re.compile("ОСОБЕННОСТИ\s[\(]масштабируемость[\)]\n[\-]{28}(.*)ОГРАНИЧЕНИЯ\n[\-]{28}", re.DOTALL)
		regHelp9 = re.compile("[\(][!]{3}[\)]")
		regHelpRows = re.compile("\n")
		regHelpStruct = re.compile(r"(Структура[\s]файла[:].*?)\n$", re.DOTALL|re.MULTILINE)
		regStructKey = re.compile("key[:]")
		regStructName = re.compile("name[:]")
		regStructPattern = re.compile("pattern[:]")
		try:
#			self.errString = "### НЕЖЕЛАТЕЛЬНО, НО ВЕРОЯТНО (ошибка) ###:\r\n"
			fileObj = io.open("README.txt", mode="r", encoding="utf-8")
			self.helpText = fileObj.read()
			fileObj.close()
			fileObj = io.open("license/license.txt", mode="r", encoding="utf-8")
			self.licenseText = fileObj.read()
			fileObj.close
			fileObj = io.open("About.txt", mode="r", encoding="utf-8")
			self.authorText = fileObj.read()
			fileObj.close()
## License check
			resLicense1 = regLicense1.findall(self.licenseText)
			resLicense2 = regLicense2.findall(self.licenseText)
			resLicense3 = regLicense3.findall(self.licenseText)
			resLicense4 = regLicense4.findall(self.licenseText)
			resLicense5 = regLicense5.finditer(self.licenseText)
			resLicense6 = regLicense6.finditer(self.licenseText)
			resLicense = len([iter for iter in resLicense1]) + len([iter for iter in resLicense2])
			resLicense = len([iter for iter in resLicense3]) + len([iter for iter in resLicense4])/resLicense
			checkLicense5 = [[iterItem.start(), iterItem.end()] for iterItem in resLicense5]
			checkLicense6 = [[iterItem.start(), iterItem.end()] for iterItem in resLicense6]
			try: 
				checkLicense_11 = [jItem[0] for jItem in checkLicense5][6] + [iItem[1] for iItem in checkLicense6][0]
				checkLicense11_ = [jItem[1] for jItem in checkLicense5][0] + [iItem[0] for iItem in checkLicense6][1]
			except IndexError:
				raise licenseCheckError("<<license error>>", "Не тот файл с лицензией или измененный")
			chkPos = checkLicense5[len(checkLicense5)-1][0]/(resLicense*268)
			divDif = round(float(checkLicense_11/checkLicense11_-checkLicense_11//checkLicense11_), round(chkPos))*1000*((round(chkPos,6)-round(chkPos))+1)
			divLicense = divDif*(len(checkLicense5)-len(checkLicense6))
			sumLicenseStart = sum([jItem[0] for jItem in checkLicense5 if jItem!=checkLicense5[0] and jItem!=checkLicense5[len(checkLicense5)-1]])
			sumLicenseEnd = sum([jItem[1] for jItem in checkLicense5 if jItem!=checkLicense5[0] and jItem!=checkLicense5[len(checkLicense5)-1]])
			sumDif = sumLicenseEnd-sumLicenseStart
			sumLicense = sumDif*((len(checkLicense5)*len(checkLicense6))-len(checkLicense6))
			if sumLicense != divLicense:
				raise licenseCheckError("<<license error>>", "Не тот файл с лицензией или измененный")
## Author check
			resAuthor1 = regAuthor1.split(self.authorText)
			countAuth1 = set(resAuthor1)
			resAuthor2 = regAuthor2.split(self.authorText)
			countAutn2 = set(resAuthor2)
			if len(countAuth1)+len(countAutn2) != 87:
				raise licenseCheckError("<<license error>>", "Не тот файл с инфо о программе или измененный")
			resLicense1 = regLicense1.finditer(self.authorText)
			statLicense1 = [[iterItem.start(), iterItem.end()] for iterItem in resLicense1]
			resLicense3 = regLicense3.finditer(self.authorText)
			statLicense3 = [[iterItem.start(), iterItem.end()] for iterItem in resLicense3]
			resLicense4 = regLicense4.finditer(self.authorText)
			statLicense4 = [[iterItem.start(), iterItem.end()] for iterItem in resLicense4]
			if len(statLicense1)+len(statLicense3)+len(statLicense4) != 3:
				raise licenseCheckError("<<license error>>", "Не тот файл с инфо о программе или измененный")
			statLicense1 = statLicense1.pop(0)
			statLicense3 = statLicense3.pop(0)
			statLicense4 = statLicense4.pop(0)
			startStat = (statLicense1[0]+statLicense3[0]+statLicense4[0])
			endStat = (statLicense1[1]+statLicense3[1]+statLicense4[1])
			if statLicense4[0] - (endStat - startStat) - statLicense3[0] != -5:
				raise licenseCheckError("<<license error>>", "Не тот файл с инфо о программе или измененный")
## README check
			resHelp1 = regHelp1.findall(self.helpText)
			resHelp2 = regHelp2.findall(self.helpText)
			resHelp3 = regHelp3.findall(self.helpText)
			resHelp4 = regHelp4.findall(self.helpText)
			resHelp5 = regHelp5.findall(self.helpText)
			resHelp6 = regHelp6.findall(self.helpText)
			resHelp7 = regHelp7.findall(self.helpText)
			if len(resHelp1)+len(resHelp2)+len(resHelp3)+len(resHelp4)+len(resHelp5)+len(resHelp6)+len(resHelp7) != 7:
				raise licenseCheckError("<<help-file error>>", "Не тот файл помощи или не все нужные поля в нем")
			resHelp8 = regHelp8.search(self.helpText)
			txtRes8 = resHelp8.group(1)
			resHelp2 = regHelp9.findall(txtRes8)
			if len(resHelp2) < 11:
				raise licenseCheckError("<<help-file error>>", "В разделе Осоебенности некоторые пункты с (!!!) не найдены")
			resLicense1 = regLicense1.findall(self.helpText)
			if len(resLicense1) != 1:
				raise licenseCheckError("<<help-file error>>", "Что-то отстутствует в файле")
			resLicense5 = regLicense5.findall(self.helpText)
			if len(resLicense5) < 3:
				raise licenseCheckError("<<help-file error>>", "Что-то отстутствует в файле")
			resHelpRows = regHelpRows.findall(self.helpText)
			if len(resHelpRows) > 250:
				raise licenseCheckError("<<help-file error>>", "Длинный файл")
			resHelpStruct = regHelpStruct.search(self.helpText)
			resHelpStruct = resHelpStruct.group(1)
			resStructKey = regStructKey.findall(resHelpStruct)
			if len(resStructKey) != 2:
				raise licenseCheckError("<<help-file error>>", "Описание структуры неверное")
			resStructName = regStructName.findall(resHelpStruct)
			if len(resStructName) != 2:
				raise licenseCheckError("<<help-file error>>", "Описание структуры неверное")
			resStructPattern = regStructPattern.findall(resHelpStruct)
			if len(resStructPattern) != 2:
				raise licenseCheckError("<<help-file error>>", "Описание структуры неверное")
			self.txtObj = FileChecker()
			self.txtObj.loadPatterns()
			self.txtObj.compilePatterns()
		except licenseCheckError as err:
			self.errString = self.errString + "Тут: " + err.typeValue + " - " + err.strValue
			self.handleFormErr(self.errString)
		except compileRegError as err:
			self.errString = self.errString + "Тут: " + err.typeValue + " - " + err.strValue
			self.handleFormErr(self.errString)
		except parseFileError as err:
			self.errString = self.errString + "Тут: " + err.typeValue + " - " + err.strValue
			self.handleFormErr(self.errString)
		except loadFileError as err:
			self.errString = self.errString + "Тут: " + err.typeValue + " - " + err.strValue
			self.handleFormErr(self.errString)
		except:
			self.errString = self.errString + "Тут: " + str(sys.exc_info()[0]) + " - " + str(sys.exc_info()[1])
			self.handleFormErr(self.errString)

	def loadAdd(self):
		self.treeWindow()
		self.helpMenu()
		

	def helpAndInfo(self):
		self.osFrame.pack_forget()
		self.titleWin.pack_forget()
		self.bOpen.config(state="active")
		self.infoWin.pack(side="left", anchor="center")

	def helpMenu(self):
		self.menuFrame = tkinter.Frame(master=self.infoWin)
		self.menuFrame.pack(side="top", anchor="center")
		self.pagesInfo = tkinter.ttk.Notebook(master=self.menuFrame)
		self.helpPageFrame = tkinter.Frame(master=self.pagesInfo)
		self.helpPageFrame.pack()
		self.helpPage = tkinter.Text(master=self.helpPageFrame, bg="DarkSeaGreen1")
		self.yScrollHelp = tkinter.Scrollbar(master=self.helpPageFrame, orient="vertical")
		self.helpPage.insert(index="end", chars=self.helpText)
		self.helpPage.config(yscrollcommand=self.yScrollHelp.set)
		self.pagesInfo.add(self.helpPageFrame, text="Справка(+)")
		self.licensePageFrame = tkinter.Frame(master=self.pagesInfo)
		self.licensePageFrame.pack()
		self.licensePage = tkinter.Text(master=self.licensePageFrame, bg="DarkSeaGreen1")
		self.yScrollLicense = tkinter.Scrollbar(master=self.licensePageFrame, orient="vertical")
		self.licensePage.insert(index="end", chars=self.licenseText)
		self.licensePage.config(yscrollcommand=self.yScrollLicense.set)
		self.pagesInfo.add(self.licensePageFrame, text="Лицензия(c)")
		self.authorPageFrame = tkinter.Frame(master=self.pagesInfo)
		self.authorPageFrame.pack()
		self.authorPage = tkinter.Text(master=self.authorPageFrame, bg="DarkSeaGreen1")
		self.authorPage.config(fg="SteelBlue4", font={"Times", 12})
		self.authorPage.insert(index="end", chars=self.authorText)
		self.pagesInfo.add(self.authorPageFrame, text="Титры(\")")
		self.pagesInfo.pack(side="left")
		self.yScrollHelp.config(command=self.helpPage.yview)
		self.yScrollHelp.pack(side="right", fill="y")
		self.helpPage.pack(fill="both",expand=1)
		self.yScrollLicense.config(command=self.licensePage.yview)
		self.yScrollLicense.pack(side="right", fill="y")
		self.licensePage.pack(fill="both",expand=1)
		self.authorPage.pack()

	def treeWindow(self):
		self.exstdNodes = {}
		self.treeFrame = tkinter.Frame(master=self.osFrame, relief="solid", borderwidth="1")
		self.treeFrame.pack(side="top")
		self.winSearch = tkinter.ttk.Treeview(master=self.treeFrame, columns=('type', 'size'), selectmode="browse")
		self.yScroll = tkinter.Scrollbar(master=self.treeFrame, orient="vertical")
		self.winSearch.pack(side="left", fill="y")
		self.yScroll.pack(side="right", fill="y")

	def walkTree(self, path=os.getcwd()):
		parentLst = []
		dirsLst = []
		filesLst = []
		i = 0
		for parDir, dirs, files in os.walk(path, topdown=False, onerror=None, followlinks=False):
			parentLst.append(parDir)
			dirsLst.append(dirs)
			filesLst.append(files)
		return parentLst, dirsLst, filesLst

	def tryOpen(self, event, nodesLst={'default':'default'}):
		self.bOperate.config(state="disabled")
		if self.__dict__.get('winFile') is not None:
			self.fileFrame.destroy()
		iid = self.winSearch.selection()[0]
		fileToOpen = self.winSearch.item(iid, option="text")
		nodeIid = self.winSearch.parent(iid)
		lstValues = list(nodesLst.values())
		lstKeys = list(nodesLst.keys())
		pathToOpen = lstKeys[lstValues.index(nodeIid)] + "/" + fileToOpen
		try:
			try:
				fileObj = io.open(pathToOpen, "r", encoding="utf-8")
			except PermissionError:
				raise readPermisError("<<no read permission>>", "\r\n    Похоже нет прав на чтение файла!")
		except readPermisError as err:
			self.helpAndInfo()
			self.errString = self.errString + "Тут: " + err.typeValue + " - " + err.strValue
			self.errString = self.errString + "\r\n    файл: " +  pathToOpen
			self.handleFormErr(self.errString)
		self.fileFrame = tkinter.Frame(master=self.osFrame, borderwidth="20", background="#B0C4DE")
		self.fileFrame.pack(side="bottom", anchor="center")
		self.frameTitle = tkinter.Entry(master=self.fileFrame, background="#B0C4DE", justify="left", relief="flat")
		self.frameTitle.config(font=("Courier", 10))
		self.frameTitle.insert(index="end", string="Предварительно - " + fileToOpen)
		self.frameTitle.pack(side="top", fill="x")
		self.winFile = tkinter.Text(master=self.fileFrame, background="Beige")
		self.yScrollFile = tkinter.Scrollbar(master=self.fileFrame, orient="vertical")
		self.winFile.config(yscrollcommand=self.yScrollFile.set)
		try:
			self.winFile.insert(index="end", chars=fileObj.read())
			self.fileFrame.event_generate(sequence="<<setFocusOnFile>>")
		except UnicodeDecodeError:
			self.winFile.insert(index="end", chars="НеОбычный текстовый формат...")
			self.fileFrame.event_generate(sequence="<<setFocusOnFile>>")
		finally:
			fileObj.close()
		self.yScrollFile.config(command=self.winFile.yview)
		self.yScrollFile.pack(side="right", fill="y")
		self.winFile.pack()
		self.bOperate.config(state="active")
		fileObj.close()
		self.bind(sequence="<<setFocusOnFile>>", func=self.frameDestroy(), add=None)

	def upperPath(self, event):
#		self.osFrame.destroy()
		_topDir_ = os.getcwd()
		_topDir_
		if (_topDir_ == '/'):
			pass
		elif (len(_topDir_) == 3) and (_topDir_.find(':\\') != 0):
			pass
		else:
			self.treeFrame.destroy()
			self.treeWindow()
			os.chdir('..')
			self.pathSearch()

	def frameDestroy(self):
		if self.__dict__.get('workFrame') is not None:
			self.workFrame.destroy()

	def workOperations(self):
		self.bOperate.config(state="disabled")
		self.workFrame = tkinter.Frame(master=self.mainFrame, borderwidth="1")
		self.operFrame = tkinter.Frame(master=self.workFrame, background="#778899")
		self.opTitInd = tkinter.Entry(master=self.operFrame, background="#778899", relief="flat", font=(12), width=12)
		self.bCheckF = tkinter.Button(master=self.operFrame, text="Подходит?", relief="groove")
		self.bAnalyze = tkinter.Button(master=self.operFrame, text="Разобраться=>", relief="groove")
		self.bTable = tkinter.Button(master=self.operFrame, text="В таблицу::", relief="groove")
		self.allGraphs = tkinter.Button(master=self.operFrame, text="Все пункты-^", relief="groove")
		self.comGraphs = tkinter.Button(master=self.operFrame, text="Основные/-", relief="groove")
		self.bTable.config(state="disabled", command=None)
		self.bAnalyze.config(state="disabled", command=None)
		self.allGraphs.config(state="disabled", command=None)
		self.comGraphs.config(state="disabled", command=None)
		self.txtObj.loadText(self.winFile.get(index1="1.0", index2="end"))
		self.bCheckF.config(command=self.passCheck)
		self.titFStruct1 = tkinter.Entry(master=self.operFrame, background="#778899", relief="flat")
		self.titFStruct1.config(width=12, justify="center", foreground="#A9A9A9")
		self.titFStruct2 = tkinter.Entry(master=self.operFrame, background="#778899", relief="flat")
		self.titFStruct2.config(width=12, justify="center", foreground="#A9A9A9")
		self.titFStruct3 = tkinter.Entry(master=self.operFrame, background="#778899", relief="flat")
		self.titFStruct3.config(width=12, justify="center", foreground="#A9A9A9")
		self.titFStruct4 = tkinter.Entry(master=self.operFrame, background="#778899", relief="flat")
		self.titFStruct4.config(width=12, justify="center", foreground="#A9A9A9")
		self.grFStruct1 = tkinter.Entry(master=self.operFrame, background="#778899", relief="flat")
		self.grFStruct1.config(width=12, justify="center", foreground="#A9A9A9")
		self.grFStruct2 = tkinter.Entry(master=self.operFrame, background="#778899", relief="flat")
		self.grFStruct2.config(width=12, justify="center", foreground="#A9A9A9")
		self.grFStruct3 = tkinter.Entry(master=self.operFrame, background="#778899", relief="flat")
		self.grFStruct3.config(width=12, justify="center", foreground="#A9A9A9")
		self.grFStruct4 = tkinter.Entry(master=self.operFrame, background="#778899", relief="flat")
		self.grFStruct4.config(width=12, justify="center", foreground="#A9A9A9")
		self.finFStruct1 = tkinter.Entry(master=self.operFrame, background="#778899", relief="flat")
		self.finFStruct1.config(width=12, justify="center", foreground="#A9A9A9")
		self.finFStruct2 = tkinter.Entry(master=self.operFrame, background="#778899", relief="flat")
		self.finFStruct2.config(width=12, justify="center", foreground="#A9A9A9")
		self.finFStruct2_1 = tkinter.Text(master=self.operFrame, background="#778899", relief="flat")
		self.finFStruct2_1.config(width=12, borderwidth=0, height=0, foreground="#A9A9A9")
		self.finFStruct3 = tkinter.Entry(master=self.operFrame, background="#778899", relief="flat")
		self.finFStruct3.config(width=12, justify="center", foreground="#A9A9A9")
		self.finFStruct4 = tkinter.Entry(master=self.operFrame, background="#778899", relief="flat")
		self.finFStruct4.config(width=12, justify="center", foreground="#A9A9A9")
		strStruct1 = "||"
		strStruct2 = "Пусто"
		strStruct3 = "\\v/"
		strStruct4 = "Представить"
		strStruct5 = "==Готово=="
		strStruct6 = "Файл здесь:\n"
		self.titFStruct1.insert(index="end", string=strStruct1)
		self.titFStruct2.insert(index="end", string=strStruct2)
		self.titFStruct3.insert(index="end", string=strStruct1)
		self.titFStruct4.insert(index="end", string=strStruct3)
		self.grFStruct1.insert(index="end", string=strStruct1)
		self.grFStruct2.insert(index="end", string=strStruct4)
		self.grFStruct3.insert(index="end", string=strStruct1)
		self.grFStruct4.insert(index="end", string=strStruct3)
		self.finFStruct1.insert(index="end", string=strStruct1)
		self.finFStruct2.insert(index="end", string=strStruct6)
		self.finFStruct3.insert(index="end", string=strStruct1)
		self.finFStruct4.insert(index="end", string=strStruct5)
		self.workFrame.pack(side="right", anchor="center", fill="y")
		self.operFrame.pack(side="left", anchor="center", fill="y")
		self.opTitInd.pack(side="top")
		self.bCheckF.pack()
		self.titFStruct1.pack()
		self.titFStruct2.pack()
		self.titFStruct3.pack()
		self.titFStruct4.pack()
		self.bAnalyze.pack()
		self.bTable.pack()
		self.grFStruct1.pack()
		self.grFStruct2.pack()
		self.grFStruct3.pack()
		self.grFStruct4.pack()
		self.allGraphs.pack()
		self.comGraphs.pack()
		self.finFStruct1.pack()
		self.finFStruct2.pack()
		self.finFStruct2_1.pack()
		self.finFStruct3.pack()
		self.finFStruct4.pack()

	def passCheck(self):
		self.txtObj.getFormat()
		self.titFStruct1.config(width=12, justify="center", foreground="#EEE8AA")
		self.titFStruct2.delete(first=0, last="end")
		self.titFStruct2.insert(index="end", string=self.txtObj.attrReturn())
		self.titFStruct2.config(width=12, justify="center", foreground="#EEE8AA")
		self.titFStruct3.config(width=12, justify="center", foreground="#EEE8AA")
		self.titFStruct4.config(width=12, justify="center", foreground="#EEE8AA")
		self.bCheckF.config(state="disabled")
		if self.txtObj.textStruct != None:
			self.bAnalyze.config(state="active")
			self.bAnalyze.config(command=self.analyzeStat)
			self.bTable.config(state="active")
			self.bTable.config(command=self.txtToXL)
		elif self.txtObj.textStruct == "sar_statistics":
			pass
		else:
			pass
		self.operFrame.update_idletasks

	def txtToXL(self):
		self.xlObject = ConvertToXL(self.txtObj.attrReturn() + ".otc")
#		self.xlObject.initiateDoc()
		if len(self.txtObj.elemCollect) == 0:
#			self.txtObj.textToStruct(self.winFile.get(index1="1.0", index2="end"))
			try:
				self.txtObj.textToStruct()
			except columnSplitError as err:
				self.helpAndInfo()
				self.errString = self.errString + "Тут: " + err.typeValue + " - " + err.strValue
				self.handleFormErr(self.errString)
		self.bAnalyze.config(state="disabled")
		self.bTable.config(state="disabled")
		self.grFStruct1.config(width=12, justify="center", foreground="#EEE8AA")
		self.grFStruct2.config(width=12, justify="center", foreground="#EEE8AA")
		self.grFStruct3.config(width=12, justify="center", foreground="#EEE8AA")
		self.grFStruct4.config(width=12, justify="center", foreground="#EEE8AA")
		self.allGraphs.config(state="active", command=self.buildAllGraphs)
#		self.comGraphs.config(state="active", command=None)

	def analyzeStat(self):
		try:
			self.txtObj.textToStruct()
		except columnSplitError as err:
			self.helpAndInfo()
			self.errString = self.errString + "Тут: " + err.typeValue + " - " + err.strValue
			self.handleFormErr(self.errString)
		if self.txtObj.dateFlag==1:
			self.txtObj.detalTime()
			self.datetimeStart = datetime.datetime.strptime(self.txtObj.periodStart, '%X')
			self.datetimeEnd = datetime.datetime.strptime(self.txtObj.periodEnd, '%X')
			self.baseDate = datetime.datetime(self.datetimeStart.year, self.datetimeStart.month, self.datetimeStart.day, 0, 0, 0)
			self.baseTime = self.datetimeStart - self.baseDate
			self.bAnalyze.config(state="disabled")
			if self.datetimeStart > self.datetimeEnd:
				self.datetimeEnd = datetime.datetime.strptime(self.txtObj.periodEnd, '%X') + datetime.timedelta(days=1)
			timeVar = datetime.datetime
			self.intervals = 5
			self.durPeriod = datetime.timedelta(minutes=60)
			self.intervCollect = []
			while (self.durPeriod.seconds > 120) or (self.intervals > 1000):
				self.intervals = self.intervals * 2

# python3 on suse has no method total_seconds(), timedelta/int doesnt work
				#self.durPeriod = (self.datetimeEnd - self.datetimeStart) / self.intervals
				self.durPeriod = datetime.timedelta(seconds = int(self.dtTotalSec(self.datetimeEnd - self.datetimeStart) / self.intervals))
#				self.durPeriod = self.timeDltDiv(self.datetimeEnd, self.datetimeStart, self.intervals)
			for i in range(self.intervals):
				interimDate = timeVar.strptime(self.txtObj.periodStart, "%X") + self.durPeriod * i
				secPassed = interimDate - timeVar.strptime(self.txtObj.periodStart, "%X")
				intervElem = (secPassed.seconds, timeVar.strftime(interimDate, "%H:%M"))
				self.intervCollect.append(intervElem)
			self.analyzeFrame = tkinter.Frame(master=self.workFrame, background="#FA8072", borderwidth=2, relief="sunken")
			self.timeAFrame = tkinter.Frame(master=self.analyzeFrame, background="#FA8072", borderwidth=1, relief="groove")
			self.getDataFrame = tkinter.Frame(master=self.analyzeFrame,  background="#FA8072", borderwidth=1, relief="groove")
			self.bGetSetData = tkinter.Button(master=self.getDataFrame, text="Указать(-*<)", relief="groove")
			self.bGetSetData.config(command=self.specifyData)
			self.timeAMainWinFrame = tkinter.Frame(master=self.timeAFrame, background="#FA8072")
			self.timeAIndent = tkinter.Label(master=self.timeAFrame, background="#FA8072", font=("Arial",6))
			self.timeAIndent.config(text="заглушка", bg="#FA8072", fg="#FA8072", bd=1)
			self.leftAFrame = tkinter.Frame(master=self.timeAMainWinFrame, background="#FA8072")
			self.rightAFrame = tkinter.Frame(master=self.timeAMainWinFrame, background="#FA8072")
			self.leftSpinEntry = tkinter.Frame(master=self.leftAFrame, background="#FA8072")
			self.rightSpinEntry = tkinter.Frame(master=self.rightAFrame, background="#FA8072")
			self.analyzeFrame.pack(side="right", fill="y")
			self.startLable = tkinter.Label(master=self.leftAFrame, text="Запуск", background="#FA8072")
			self.startLable.config(font=("Courier",8), fg="#8B4513", justify="center")
			self.startScale = tkinter.Scale(master=self.leftAFrame, from_=self.intervCollect[0][0], to=self.intervCollect[self.intervals-1][0])
			self.startValue = tkinter.Entry(master=self.leftSpinEntry, background="#C0C0C0", relief="groove")
			self.startSpin = tkinter.Spinbox(master=self.leftSpinEntry, from_=None, to=None, state="disabled", disabledbackground="#FA8072")
			self.startSpin.config(width=2, relief="flat", bg="#FA8072", fg="#FA8072", buttonbackground="#228B22")
			self.duratLable = tkinter.Label(master=self.rightAFrame, text="Работало", background="#FA8072")
			self.duratLable.config(font=("Courier",8), fg="#8B4513", justify="center")
			self.duratScale = tkinter.Scale(master=self.rightAFrame, from_=self.intervCollect[0][0], to=self.intervCollect[self.intervals-1][0])
			self.duratSpin = tkinter.Spinbox(master=self.rightSpinEntry, from_=None, to=None, state="disabled", disabledbackground="#FA8072")
			self.duratSpin.config(width=2, relief="flat", bg="#FA8072", fg="#FA8072", buttonbackground="#228B22")
			self.duratValue = tkinter.Entry(master=self.rightSpinEntry, background="#C0C0C0", relief="groove")
			self.precisBut = tkinter.Button(master=self.timeAFrame, background="#FFDAB9", text="Точнее[+]", relief="groove")
			self.precisBut.config(command=self.spinEnable)
			self.duratValue.config(justify="center", foreground="#00008B", width=6, font=("courier", 10))
			self.startValue.config(justify="center", foreground="#00008B", width=6, font=("courier", 10))
			self.contVar = tkinter.IntVar()
			self.duratVar = tkinter.IntVar()
			self.startScale.config(command=self.sScaleSpark, variable=self.contVar, orient="vertical", width=8)
			self.startScale.config(resolution=self.durPeriod.seconds, showvalue=0, background="#FA8072")
			self.duratScale.config(command=self.dScaleSpark, variable=self.duratVar, orient="vertical", width=8)
			self.duratScale.config(resolution=datetime.timedelta(minutes=5).seconds, showvalue=0, background="#FA8072")
			self.startScale.config(length=140)
			self.duratScale.config(length=140)
			self.duratScale.set(self.intervCollect[self.intervals-1][0])
			self.timeAFrame.pack(side="top")
			self.timeAMainWinFrame.pack(side="top")
			self.leftAFrame.pack(side="left")
			self.rightAFrame.pack(side="left")
			self.getDataFrame.pack(side="bottom", fill="x")
			self.bGetSetData.pack()
			self.startLable.pack()
			self.startScale.pack()
			self.leftSpinEntry.pack()
			self.startValue.pack(side="right")
			self.startSpin.pack(side="left")
			self.duratLable.pack()
			self.duratScale.pack()
			self.rightSpinEntry.pack()
			self.duratValue.pack(side="right")
			self.duratSpin.pack(side="left")
			self.precisBut.pack(side="bottom", anchor="center")
			self.timeAIndent.pack(side="bottom", anchor="center")
			tkinter.Scale.bind_all(self, sequence="<<SliderMoved>>", func=self.scaleChange)
		elif self.txtObj.dateFlag==0:
			pass
		else:
			pass

	def specifyData(self):
		self.bGetSetData.config(state="disabled")
		sSpinValue = self.startSpin.get()
		if sSpinValue == "":
			sSpinValue = 0
		dSpinValue = self.duratSpin.get()
		if dSpinValue == "":
			dSpinValue = 0
		sDateTime = self.datetimeStart + datetime.timedelta(seconds=self.startScale.get()+int(sSpinValue)*60)
		dDateTime = sDateTime + datetime.timedelta(seconds=self.duratScale.get()+int(dSpinValue)*60)
		for i in self.txtObj.elemCollect[1:]:
			currentDate = datetime.datetime.strptime(i[0], '%X')
			if currentDate < self.datetimeStart:
				currentDate = datetime.datetime.strptime(i[0], '%X') + datetime.timedelta(days=1)
			if (sDateTime <= currentDate) and (dDateTime > currentDate):
				i.append('1')
			else:
				i.append('0')
		self.txtObj.elemCollect[0].append('test_period')
		
	def sScaleSpark(self, event):
		self.startScale.event_generate(sequence="<<SliderMoved>>")
		
	def dScaleSpark(self, event):
		self.duratScale.event_generate(sequence="<<SliderMoved>>")
		
	def scaleChange(self, event):
		currentScale = event.__getattribute__('widget')
		currentFrame = currentScale.__getattribute__('master')
		if currentScale == self.startScale:
			self.startSpin.delete(first=0)
		if currentScale == self.duratScale:
			self.duratSpin.delete(first=0)
		self.fillTimeValue()
		
	def fillTimeValue(self):
		startValue = self.startScale.get()
		startSpin = self.startSpin.get()
		if (startSpin is None) or (startSpin==""):
			startSpin = 0
		duratValue = self.duratScale.get()
		duratSpin = self.duratSpin.get()
		duratResolution = self.duratScale['resolution']
		startResolution = self.startScale['resolution']
		if (duratSpin is None) or (duratSpin==""):
			duratSpin = 0
		newStartValue = self.baseDate + datetime.timedelta(seconds=(self.baseTime.seconds+startValue+int(startSpin)*60))
		plusMin = 0
		while (self.intervCollect[self.intervals-1][0]-(startValue+int(startSpin)*60) < duratValue+int(duratSpin)*60):
			plusMin = plusMin + 1
			self.duratScale.set(self.intervCollect[self.intervals-1][0]-(startValue+(int(startSpin)+plusMin)*60))
			self.duratScale.update
			duratValue = self.duratScale.get()
			if (plusMin > (duratResolution+startResolution)) and (duratSpin != 0):
				duratSpin = 0
				self.duratSpin.delete(first=0)
		self.startValue.config(state="normal")
		self.startValue.delete(first="0", last="end")
		self.startValue.insert(index="end", string=newStartValue.strftime("%H:%M"))
		self.startValue.config(state="readonly")
		self.startValue.update
		self.startScale.update
		newDuratValue = datetime.timedelta(seconds=duratValue+int(duratSpin)*60)
		newDuratHour = newDuratValue.seconds // 3600
		newDuratRest = newDuratValue.seconds - newDuratHour * 3600
		newDuratMinute = newDuratRest // 60
		newDuratValue = None
		self.duratValue.config(state="normal")
		self.duratValue.delete(first="0", last="end")
		self.duratValue.insert(index="end", string=str(newDuratHour)+":"+str(newDuratMinute))
		self.duratValue.config(state="readonly")
		self.duratValue.update
		self.duratScale.update

# python3 on suse has no method total_seconds(), timedelta/int doesnt work
#		def spinEnable(self):
#		restMinutes = (((self.durPeriod.total_seconds() / 60 - self.durPeriod.total_seconds() // 60) + 0.5) // 1)
#		roundMinutes = int(self.durPeriod.total_seconds() // 60 + restMinutes)
#		self.startSpin.config(state="normal", from_=-roundMinutes, to=roundMinutes)
#		self.startSpin.config(command=self.sSpinSpark)
#		self.duratSpin.config(state="normal", from_=int(-datetime.timedelta(minutes=5).total_seconds()//60))
#		self.duratSpin.config(to=int(datetime.timedelta(minutes=5).total_seconds()//60))
#		self.duratSpin.config(command=self.dSpinSpark)
#		tkinter.Spinbox.bind_all(self, sequence="<<ArrowPressed>>", func=self.spinPrecise)

	def spinEnable(self):
		restMinutes = (((self.dtTotalSec(self.durPeriod) / 60 - self.dtTotalSec(self.durPeriod) // 60) + 0.5) // 1)
		roundMinutes = int(self.dtTotalSec(self.durPeriod) // 60 + restMinutes)
		self.startSpin.config(state="normal", from_=-roundMinutes, to=roundMinutes)
		self.startSpin.config(command=self.sSpinSpark)
		self.duratSpin.config(state="normal", from_=int(-self.dtTotalSec(datetime.timedelta(minutes=5))//60))
		self.duratSpin.config(to=int(self.dtTotalSec(datetime.timedelta(minutes=5))//60))
		self.duratSpin.config(command=self.dSpinSpark)
		tkinter.Spinbox.bind_all(self, sequence="<<ArrowPressed>>", func=self.spinPrecise)
		
	def sSpinSpark(self):
		self.startSpin.event_generate(sequence="<<ArrowPressed>>")
		
	def dSpinSpark(self):
		self.duratSpin.event_generate(sequence="<<ArrowPressed>>")

	def spinPrecise(self, event):
		currentSpin = event.__getattribute__('widget')
		currentFrame = currentSpin.__getattribute__('master')
		currentScaleFrame = currentFrame.__getattribute__('master')
		scfElements = currentScaleFrame.slaves()
		for i in scfElements:
			if i.__class__ == tkinter.Scale:
				currentScale = i
		if (currentScale.get() == currentScale['from']) and (int(currentSpin.get()) < 0):
			currentSpin.delete(first=0)
		if (currentScale.get() == currentScale['to']) and (int(currentSpin.get()) > 0):
			currentSpin.delete(first=0)
		self.fillTimeValue()

	def buildAllGraphs(self):
		self.xlObject.createBook()
		self.xlObject.initiateDoc()
		self.xlObject.getData(self.txtObj.elemCollect)
		self.xlObject.insertData()
		self.xlObject.calcAVG()
		self.xlObject.addTips()
		self.xlObject.calcMedian()
		lCols = [i for i in range(self.xlObject.numCols)]
		lCols.pop(0)
		self.xlObject.insertChart(0, lCols)
		if self.txtObj.elemCollect[0][len(self.txtObj.elemCollect[0])-1] == 'test_period':
			self.xlObject.periodLine()
		self.xlObject.closeAndSaveDoc()
		self.allGraphs.config(state="disabled")
		self.comGraphs.config(state="disabled")
		self.finFStruct1.config(width=12, justify="center", foreground="#EEE8AA")
		self.finFStruct2.config(width=12, justify="center", foreground="#EEE8AA")
		self.finFStruct2_1.insert(index="end", chars=os.getcwd())
		#pathChars = self.finFStruct2_1.count(index1=1.0, index2="end")
		pathChars = [len(os.getcwd())]
		pathRows = pathChars[0] // self.finFStruct2_1["width"]
		if pathChars[0] % self.finFStruct2_1["width"] != 0:
			pathRows = pathRows + 1
		self.finFStruct2_1.config(width=12, height=pathRows, foreground="#FFB6C1")
		self.finFStruct3.config(width=12, justify="center", foreground="#EEE8AA")
		self.finFStruct4.config(width=12, justify="center", foreground="#EEE8AA")
		re.purge()

	def pathSearch(self):
		self.bOpen.config(state="disabled")
		currentPath = os.getcwd()
		self.infoWin.pack_forget()
		self.titleWin.pack_forget()
		self.osFrame.pack(side="left", anchor="center")
		if len(self.winSearch.get_children()) == 0:
			self.winSearch.config(yscrollcommand=self.yScroll.set, displaycolumns="#all")
			self.yScroll.config(command=self.winSearch.yview)
			#self.winSearch.heading("name", text="имя")
			self.winSearch.heading("#0", text=os.getcwd())
			self.winSearch.column("type", anchor="c")
			self.winSearch.heading("type", text="тип")
			self.winSearch.heading("size", text="размер")
			self.winSearch.column('size', anchor='e')
			parentLst, dirsLst, filesLst = self.walkTree(currentPath)
#getting sizes for files
#replacing out file filesLst with fLst_w_sizes containing tuples (file, size)
			#try:
			#	fLst_w_sizes = [[(f,str(os.path.getsize(os.path.join(parentLst[p],f)))+' байт') for f in filesLst[p]] for p in range(len(parentLst))]
			#	filesLst = fLst_w_sizes
			#except:
			tmpFlst = self.getWlkFileSize(parentLst, filesLst)
			filesLst = tmpFlst
			del tmpFlst
##
			outIidElemTree = self.winSearch.insert(parent="", index="end", text='..')
			#self.winSearch.set(outIidElemTree, column="name", value="..")
			#print(len(filesLst))
			#print(lst_w_sizes)
			self.winSearch.set(outIidElemTree, column="type", value="")
			self.winSearch.item(outIidElemTree, tag="o")
			rootIidElemTree = self.winSearch.insert(parent="", index="end", text=os.path.split(currentPath)[1])
			#self.winSearch.set(rootIidElemTree, column="name", value=os.path.split(currentPath)[1])
			self.winSearch.set(rootIidElemTree, column="type", value="д")
			self.winSearch.item(rootIidElemTree, open="True", tag="d")
			self.exstdNodes = {}
			self.exstdNodes[currentPath] = rootIidElemTree
			if len(parentLst) == 1:
				for leaf in filesLst[0]:
					iidElemLeaf = self.winSearch.insert(parent=rootIidElemTree, index="end", text=leaf[0])
					self.winSearch.set(iidElemLeaf, column="size", value=leaf[1])
					self.winSearch.set(iidElemLeaf, column="type", value="ф")
					self.winSearch.item(iidElemLeaf, tag="f")
			for k in range(len(parentLst)-1):
				locParPath, locParDir = os.path.split(parentLst[k])
				tempDirLst = dirsLst[k:]
				tempFileLst = filesLst[k:]
				tempParLst = parentLst[k:]
				tempDirLst.pop(0)
				tempFileLst.pop(0)
				tempParLst.pop(0)
				locDirs = ['None']
				locFileLst = ['None']
				locParLst = ['None']
				while locParPath != locParLst:
					locDirs = tempDirLst.pop(0)
					locFileLst = tempFileLst.pop(0)
					locParLst = tempParLst.pop(0)
				parIidElemTree = self.exstdNodes.get(locParLst)
				if parIidElemTree is None:
					parIidElemTree = self.winSearch.insert(parent="", index="end", text=os.path.split(locParLst)[1])
					#self.winSearch.set(parIidElemTree, column="name", value=os.path.split(locParLst)[1])
					self.winSearch.set(parIidElemTree, column="type", value="д")
					self.winSearch.item(parIidElemTree, tag="d")
					self.exstdNodes[locParLst] = parIidElemTree
				chilIidElemTree = self.exstdNodes.get(parentLst[k])
				if chilIidElemTree is None:
					chilIidElemTree = self.winSearch.insert(parent=parIidElemTree, index="end", text=locParDir)
					self.exstdNodes[parentLst[k]] = chilIidElemTree
				else:
					self.winSearch.move(chilIidElemTree, parIidElemTree, index=0)
				for j in filesLst[k]:
					iidElemTree = self.winSearch.insert(parent=chilIidElemTree, index="end", text=j[0])
					self.winSearch.set(iidElemTree, column="size", value=j[1])
					self.winSearch.set(iidElemTree, column="type", value="ф")
					self.winSearch.item(iidElemTree, tag="f")
				#self.winSearch.set(chilIidElemTree, column="name", value=locParDir)
				self.winSearch.set(chilIidElemTree, column="type", value="д")
				self.winSearch.item(chilIidElemTree, tag="d")
				for j in locFileLst:
					iidElemTree = self.winSearch.insert(parent=parIidElemTree, index="end", text=j[0])
					self.winSearch.set(iidElemTree, column="size", value=j[1])
					self.winSearch.set(iidElemTree, column="type", value="ф")
					self.winSearch.item(iidElemTree, tag="f")
				curIndex = parentLst.index(locParLst)
#				filesLst[curIndex].clear()
# python2.7 has no clear() method
				filesLst[curIndex] = []
		self.winSearch.update()
		self.yScroll.update
		self.winSearch.tag_bind("f", sequence="<<TreeviewSelect>>", callback=lambda evt, arg=self.exstdNodes: self.tryOpen(evt, arg))
		self.winSearch.tag_bind("o", sequence="<<TreeviewSelect>>", callback=self.upperPath)

# python3 on linux has no method total_seconds()
# function to do
	def dtTotalSec(self, dateTm1):
		numSeconds = dateTm1.days * 3600 + dateTm1.seconds
		return numSeconds
		
	def getWlkFileSize(self, prntLst, flsLst):
		if len(prntLst)!=len(flsLst):
			print('Ошибка: лист каталогов не соответствует листу файлов')
			raise internalError
		resFlst = []
		for p in range(len(prntLst)):
			tmpFlst = []
			for f in flsLst[p]:
				try:
					fTpl = (f,str(os.path.getsize(os.path.join(prntLst[p],f)))+' байт')
				except FileNotFoundError:
					fTpl = (f, ' ?ссылка')
				except PermissionError:
					fTpl = (f, ' !ссылка недоступно')
				#f = fTpl
				tmpFlst.append(fTpl)
			resFlst.append(tmpFlst)
		#flsLst = resFlst
		del tmpFlst
		return resFlst
