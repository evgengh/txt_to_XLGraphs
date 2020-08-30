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

class appDefinedError(Exception):
	def __init__(self, typeValue, strValue):
		self.typeValue = typeValue
		self.strValue = strValue
	def __repr__(self):
		return [repr(self.typeValue), repr(self.strValue)]

class compileRegError(appDefinedError):
	pass

class parseFileError(appDefinedError):
	pass

class loadFileError(appDefinedError):
	pass

class licenseCheckError(appDefinedError):
	pass

class columnSplitError(appDefinedError):
	pass
	
class readPermisError(appDefinedError):
	pass

class nullExceptionError(Exception):
	pass
