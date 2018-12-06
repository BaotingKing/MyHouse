#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/11/20
# https://blog.csdn.net/hawksoft/article/details/44700697
"""=============================================================================="""
import threading
# 用户错误类，用于抛出自定义的异常


class CustomError(RuntimeError):
    def __init__(self, args):
        self.args = args


# 实体的基类.
class EntityB:
    def __init__(self):
        self.CurrFields = []

    # 根据属性名获取属性值
    def GetValueByName(self, FieldName):
        if hasattr(self, FieldName):
            return getattr(self, FieldName)
        return None

    # 根据属性名设置属性值
    def SetValueByName(self, FieldName, Value):
        if hasattr(self, FieldName):
            return setattr(self, FieldName, Value)

    # 定义了该属性，对象可枚举.
    def __getitem__(self, key):
        if type(key) == type('abc'):
            return self.GetValueByName(key)
        if type(key) == type(1):
            theFld = self.CurrFields[key]
            return self.GetValueByName(theFld)
        return None

    # 设置属性值,key可以是索引，也可以是属性名.
    def __setitem__(self, key, value):
        if type(key) == type('abc'):
            self.SetValueByName(key, value)
        if type(key) == type(1):
            theFld = self.CurrFields[key]
            self.SetValueByName(theFld, value)

    # 获取实体的表名.
    def GetTableName(self):
        theType = type(self)
        if hasattr(theType, 'TableName'):
            return getattr(theType, 'TableName')
        return ''

    # 获取关键字段名
    def GetKeyField(self):
        theType = type(self)
        if hasattr(theType, 'KeyField'):
            return getattr(theType, 'KeyField')
        return ''

    # 获取字段名集合
    def GetFields(self):
        theType = type(self)
        if hasattr(theType, 'Fields'):
            return getattr(theType, 'Fields')
        return []

    InsertCondition = threading.Condition()
    InsertLockSign = False

    DeleteCondition = threading.Condition()
    DeleteLockSign = False

    UpdateAllCondition = threading.Condition()
    UpdateAllLockSign = False

    InsertSqlName = '__InsertSql'
    UpdateAllSqlName = '__UpdateSql'
    DelByPKSqlName = '__DelByPKSql'
    DefaultSelectSQL = '__DefaultSelectSql'

    # 根据属性名获取类型的属性值。
    def _GetClassValue(self, AttrName):
        theSelfType = type(self)
        theValue = ''
        if hasattr(theSelfType, AttrName):
            theValue = getattr(theSelfType, AttrName)
        return theValue

    # 根据属性名设置类型的属性值.
    def _SetClassValue(self, AttrName, value):
        theSelfType = type(self)
        theValue = ''
        if hasattr(theSelfType, AttrName):
            setattr(theSelfType, AttrName, value)

    # 获取字段参数
    def GetFieldParams(self):
        return self._GetClassValue('FieldParams')

    # 获取插入的SQL
    def GetInsertSQL(self):
        theSQL = self._GetClassValue(EntityB.InsertSqlName)
        if (theSQL == None or theSQL == ''):
            EntityB.InsertCondition.acquire()
            try:
                if EntityB.InsertLockSign:
                    EntityB.InsertCondition.wait()
                InsertLockSign = True
                theSQL = self._GetClassValue(EntityB.InsertSqlName)
                if (theSQL == None or theSQL == ''):
                    theTableName = self.GetTableName()
                    theFields = self.GetFields()
                    if theTableName == '' or theFields == []:
                        raise CustomError('表名或字段为空！')
                    theSQL = 'INSERT INTO ' + theTableName
                    theFlds = ''
                    theVals = ''
                    theFldParams = self.GetFieldParams()
                    for theF in theFields:
                        if theFlds == '':
                            theFlds += theF
                            theVals += theFldParams[theF]['DSFmt']
                        else:
                            theFlds += ',' + theF
                            theVals += ',' + theFldParams[theF]['DSFmt']
                    theSQL += '(' + theFlds + ') values(' + theVals + ')'
                    self._SetClassValue(EntityB.InsertSqlName, theSQL)
                return theSQL
            finally:
                InsertLockSign = False
                EntityB.InsertCondition.notify()
                EntityB.InsertCondition.release()
        else:
            return theSQL

    # 获取根据主键删除SQL
    def GetDelByPKSQL(self):
        theSQL = self._GetClassValue(EntityB.DelByPKSqlName)
        if (theSQL == None or theSQL == ''):
            EntityB.DeleteCondition.acquire()
            try:
                if EntityB.DeleteLockSign:
                    EntityB.DeleteCondition.wait()
                DeleteLockSign = True
                theSQL = self._GetClassValue(EntityB.DelByPKSqlName)
                if (theSQL == None or theSQL == ''):
                    theTableName = self.GetTableName()
                    theKeyField = self.GetKeyField()
                    if theTableName == '' or theKeyField == '':
                        raise CustomError('表名或主键为空！')
                    theFldParams = self.GetFieldParams()
                    theSQL = 'DELETE FROM ' + theTableName + ' WHERE ' + theKeyField + '=' + theFldParams[theKeyField][
                        'DSFmt']
                    self._SetClassValue(EntityB.DelByPKSqlName, theSQL)
                return theSQL
            finally:
                DeleteLockSign = False
                EntityB.DeleteCondition.notify()
                EntityB.DeleteCondition.release()
        else:
            return theSQL

    # 获取更新所有字段的SQL语句(根据主键更新)
    def GetUpdateAllSQL(self):
        theSQL = self._GetClassValue(EntityB.UpdateAllSqlName)
        if (theSQL == None or theSQL == ''):
            EntityB.UpdateAllCondition.acquire()
            try:
                if EntityB.UpdateAllLockSign:
                    EntityB.UpdateAllCondition.wait()
                UpdateAllLockSign = True
                theSQL = self._GetClassValue(EntityB.UpdateAllSqlName)
                if (theSQL == None or theSQL == ''):
                    theTableName = self.GetTableName()
                    theFields = self.GetFields()
                    theKeyField = self.GetKeyField()
                    if theTableName == '' or theFields == [] or theKeyField == '':
                        raise CustomError('表名、主键或字段为空！')
                    theSQL = 'UPDATE ' + theTableName + ' SET '
                    theFlds = ''
                    theFldParams = self.GetFieldParams()
                    for theF in theFields:
                        if (theF != theKeyField):
                            if theFlds == '':
                                theFlds += theF + '= ' + theFldParams[theF]['DSFmt']
                            else:
                                theFlds += ',' + theF + '= ' + theFldParams[theF]['DSFmt']
                    theSQL += theFlds + ' WHERE ' + theKeyField + '=' + theFldParams[theKeyField]
                    self._SetClassValue(EntityB.UpdateAllSqlName, theSQL)
                return theSQL
            finally:
                UpdateAllLockSign = False
                EntityB.UpdateAllCondition.notify()
                EntityB.UpdateAllCondition.release()
        else:
            return theSQL

    # 获取缺省的查询SQL
    def GetDefaultSelectSQL(self):
        theTableName = self.GetTableName()
        return 'SELECT * FROM ' + theTableName + ' WHERE 1=1'
    # def __delitem__(self)


"""========================================================================================"""
# Generate entities
import BusinessBase


def GetFmtStr(datatype):
    if datatype.find('varchar') >= 0:
        return '%s'
    elif datatype.find('date') >= 0:
        return '%s'
    else:
        return '%s'


def IntToStr(iData=0):
    if iData == None:
        return '0'
    return '%d' % iData;


theFile = open(r"EntitiesL.py", "w")
try:
    theDb = BusinessBase.BusinessBase(object)
    # 这里需改为从你自己的数据库XXXX
    theTabs = theDb.GetDbTables('XXXX')
    theFile.write("import EntityBase\n")

    for theTab in theTabs:
        theFile.write('class M_' + theTab.TableName.upper() + '(EntityBase.EntityB):\n')
        theFile.write('    def __init__(self):\n')
        theFile.write('        M_' + theTab.TableName.upper() + '.Count += 1\n')
        theFile.write('        self.RefDict={}\n')
        theFile.write('        self.CurrFields=[]\n')
        theFile.write('    Count=0\n')
        theFile.write('    TableName =\'' + theTab.TableName + '\'\n')
        theKeyField = ''
        theFlds = ''
        theFile.write('    FieldParams={\n')
        theFields = theDb.GetTabFields('tian', theTab.TableName)
        theIndex = 0
        for theF in theFields:
            if theF.iskey == 1:
                theKeyField = theF.column_name

            theIndex += 1
            if (theIndex > 1):
                theFile.write('                        ,\n')
                theFlds += ',\'' + theF.column_name + '\''
            else:
                theFlds = '\'' + theF.column_name + '\''
            theFile.write('                  \'' + theF.column_name + '\':\n')
            theFile.write('                        {\n')
            theFile.write('                        \'DSFmt\':\'' + GetFmtStr(theF.data_type) + '\',\n')
            theFile.write('                        \'DataType\':\'' + theF.data_type + '\',\n')
            theFile.write('                        \'Length\':' + IntToStr(theF.lengthb) + ',\n')
            theFile.write('                        \'Precision\':' + IntToStr(theF.precisionlen) + ',\n')
            theFile.write('                        \'Scale\':' + IntToStr(theF.scalelen) + '\n')
            theFile.write('                        }\n')
        theFile.write('                }\n')
        theFile.write('    KeyField =\'' + theKeyField + '\'\n')
        theFile.write('    Fields =[' + theFlds + ']\n')

finally:
    theFile.close()


"""=============================================================="""
# 这个类用于获取对象的自定义属性。
import inspect
import types
class ObjOpt:
    @staticmethod
    def IsProperty(obj):
        if(obj.__class__ is types.FunctionType):
            return False
        else:
            return True
    @staticmethod
    def GetPropertyNames(obj):
        theAttrs = inspect.getmembers(obj,ObjOpt.IsProperty)
        theRetAttrs = []
        for attr in theAttrs:
            bb=attr[0].startswith('__')
            if bb==False:
                theRetAttrs.append(attr[0])
        return theRetAttrs;
    #获取类名
    @staticmethod
    def GetClassName(Obj):
        return Obj.__name__


"""=============================================================="""
# 这是一个自动生成的实体类例子
class M_SS01_SYS_USR(EntityBase.EntityB):
    def __init__(self):
        M_SS01_SYS_USR.Count += 1
        self.RefDict={}
        self.CurrFields=[]
    Count=0
    TableName ='SS01_SYS_USR'
    KeyField='USR_ID'
    Fields=['USR_ID','USR_NAME','USR_PWD']
    FieldParams={'USR_ID':
                 {
                     'DSFmt':'%s',
                     'DataType':'varchar',
                     'Length':50,
                     'Precision':0,
                     'Scale':0
                 },
                 'USR_NAME':
                 {
                   'DSFmt':'%s',
                   'DataType':'varchar',
                     'Length':50,
                     'Precision':0,
                     'Scale':0
                 },
                 'USR_PWD':
                 {
                     'DSFmt':'%s',
                     'DataType':'varchar',
                     'Length':50,
                     'Precision':0,
                     'Scale':0
                 }
                 }


"""========================================================================"""
# 数据库访问层
import pymysql
import os

# 用于测试
class EmptyModel:
    def __init__(self, name=None):
        self.TableName = name


# 数据库帮助基类，相当于接口。其实对于python这种语言，这个类完全没必要存在.
# 不过对于多种数据库支持时，还是有点用.
# 注意：这里的参数是格式化到字符串，无法防止SQL注入。为了防止SQL注入，可以对SQL进行处理。
# 一般来说最好的办法是真正参数化，但我看了一下pymysql,并没有提供真正参数化的方法。
class DbHelper:
    def QueryByParam(self, sql, pms, EntityName, conn=None):
        return []

    def ExecuteCommand(self, sql, pms, conn=None):
        return 0


# Mysql的访问类，基于pymysql.
class DbHelperMySql(DbHelper):
    def __init__(self, CharsetName='utf8'):
        self.CharsetName = CharsetName
        if (self.CharsetName == ''):
            self.CharsetName = 'utf8'

    def ExecuteCommand(self, sql, pms, conn=None):
        theNeedCloseConn = False
        if (conn == None):
            conn = self.GetMySqlDbConnDefault()
            theNeedCloseConn = True
        theCursor = conn.cursor()
        try:
            theCursor.execute("set NAMES " + self.CharsetName)  # 保证字符集正确.
            theRet = theCursor.execute(sql, pms)
        finally:
            theCursor.close()
            if theNeedCloseConn:
                conn.close()
        return theRet

    @staticmethod
    def GetMySqlDbConn(host, port, user, pwd, dbname):
        return pymysql.connect(host=host, port=port, user=user, passwd=pwd, db=dbname)

    @staticmethod
    def GetMySqlDbConnDefault():
        return DbHelperMySql.GetMySqlDbConn('127.0.0.1', 3306, 'xxxxx', 'xxxxx', 'dbname')

    # pms 为Dict类型.
    def QueryByParam1(self, sql, pms, EntityName, conn=None):
        theNeedCloseConn = False
        if (conn == None):
            conn = self.GetMySqlDbConnDefault()
            theNeedCloseConn = True
        theCursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            theCursor.execute("set NAMES " + self.CharsetName)  # 保证字符集正确.
            theCursor.execute(sql, pms)
            rows = theCursor.fetchall()
            models = []
            for r in rows:
                m = EmptyModel(EntityName)
                for fld in r.items():
                    setattr(m, fld[0], fld[1])
                models.append(m)
            return models
        finally:
            theCursor.close()
            if theNeedCloseConn:
                conn.close()
        return []

    # pms 为Dict类型.
    def QueryByParam2(self, EntityType, sql, pms, conn=None):
        theNeedCloseConn = False
        if (conn == None):
            conn = self.GetMySqlDbConnDefault()
            theNeedCloseConn = True
        theCursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            theCursor.execute("set NAMES " + self.CharsetName)  # 保证字符集正确.
            theCursor.execute(sql, pms)
            rows = theCursor.fetchall()
            models = []
            for r in rows:
                m = EntityType()
                for fld in r.items():
                    setattr(m, fld[0], fld[1])
                    m.CurrFields.append(fld[0])
                models.append(m)
            return models
        finally:
            theCursor.close()
            if theNeedCloseConn:
                conn.close()
        return []
