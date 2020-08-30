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

import xlsxwriter
from xlsxwriter.utility import xl_col_to_name
from xlsxwriter.utility import xl_range
from xlsxwriter.utility import xl_rowcol_to_cell

class ConvertToXL:

	def __init__(self, nameXlsx="stat.sxc"):
		self.nameXL = nameXlsx
#		self.workBook = xlsxwriter.Workbook(self.nameXL, {'strings_to_numbers': True})
		self.textData = []
		self.activeSheet = None
		self.numRows = None
		self.numCols = None

	def createBook(self):
		self.workBook = xlsxwriter.Workbook(self.nameXL, {'strings_to_numbers': True})

	def addSheet(self, nameSh="default"):
		if nameSh == "default":
			numSh = len(self.workBook.worksheets())
			nameSh=str("Sheet"+numSh)
		self.workBook.add_worksheet(nameSh)

	def initiateDoc(self):
		self.dataSheet = self.addSheet("данные")
		self.returnWorksheet("данные")

	def getData(self, textStruct):
		self.textData = textStruct
		self.numRows = len(self.textData)
		self.numCols = len(self.textData[0])

	def insertData(self):
		cellRow = 0
		cellCol = 0
		for textRow in self.textData:
			for textCell in textRow:
				self.activeSheet.write(cellRow, cellCol, textCell)
				cellCol += 1
			cellCol = 0
			cellRow += 1

	def calcAVG(self):
		avgFrmt = self.workBook.add_format({'bold': True, 'font_color': 'blue'})
		self.activeSheet.write(self.numRows + 2, 0, "Среднее", avgFrmt)
		for itr in range(self.numCols - 1):
			tstRange = xl_range(1,itr + 1,self.numRows - 1,itr + 1)
			tstCell = xl_rowcol_to_cell(self.numRows + 2, itr + 1)
			self.activeSheet.write_formula(tstCell, '=ROUND(AVERAGEA(' + tstRange + '),2)', avgFrmt)
			
	def addTips(self):
		self.activeSheet.write(self.numRows + 3, 0, "Если нули, нужно пересчитать формулы Shft+Cntrl+F9")

	def calcMedian(self):
		avgFrmt = self.workBook.add_format({'bold': True, 'font_color': 'red'})
		self.activeSheet.write(self.numRows + 4, 0, "Медиана", avgFrmt)
		for itr in range(self.numCols - 1):
			tstRange = xl_range(1,itr + 1,self.numRows - 1,itr + 1)
			tstCell = xl_rowcol_to_cell(self.numRows + 4, itr + 1)
			self.activeSheet.write_formula(tstCell, '=ROUND(MEDIAN(' + tstRange + '),2)', avgFrmt)

	def returnWorksheet(self, sheetName="Sheet1"):
		sheets = self.workBook.worksheets()
		for i in sheets:
			if i.__getattribute__("name") == sheetName:
				self.activeSheet = i

	def insertChart(self, xCol, yCol):
		self.addSheet("графики")
		self.returnWorksheet("графики")
		for i in yCol:
			cCol = xl_col_to_name(i)
			self.chart = self.workBook.add_chart({'type': 'line'})
			self.chart.add_series({
				'categories': '=данные!$' + xl_col_to_name(xCol) + '$2:$' + xl_col_to_name(xCol) + '$' + str(self.numRows),
				'values':     '=данные!$' + cCol + '$2:$' + cCol + '$' + str(self.numRows),
				'name':       '=данные!$' + cCol + '$1',
				'line':       {'color': '#008B8B'}
			})
			self.chart.__dict__.__setitem__('id', self.textData[0][i])
			self.chart.set_x_axis({'num_font': {'rotation': -90}})
			self.chart.set_legend({'position': 'bottom'})
			self.chart.set_title({'none': True})
			curXPosition = (i // 3) * 8 + 3
			curYPosition = (i % 3) * 16 + 2
			self.activeSheet.insert_chart(xl_col_to_name(curXPosition) + str(curYPosition), self.chart)
			self.chart = None
	
	def periodLine(self):
		for jChart in self.workBook.__dict__.get('charts'):
			jSeries = jChart.__getattribute__('series')[0]
			jCategories = jSeries['categories']
#			if jSeries['values'] =='=данные!$' + xl_col_to_name(self.numCols-1) + '$2:$' + xl_col_to_name(self.numCols-1) + '$' + str(self.numRows):
			jChart.set_y2_axis({'label_position': 'right',
								'max': 1,
								'visible': None,
								'major_unit': 1})
			jChart.add_series({
					'name':       '=данные!$' + xl_col_to_name(self.numCols-1) + '$1',
					'categories': jCategories,
					'values':     '=данные!$' + xl_col_to_name(self.numCols-1) + '$2:$' + xl_col_to_name(self.numCols-1) + '$' + str(self.numRows),
					'y2_axis':    True,
					'line':       {'dash_type': 'dash',
									'width': 0.5}
					})

	def closeAndSaveDoc(self):
		self.workBook.close()
