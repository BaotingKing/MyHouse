#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Zhang.Baoting
# Time: 2018/7/30
import sys
import sqlite3


def UpdateSqlData(sqldata, refinedResult, isWarning, isSingle, isStable, carChannel):
    """&& 更新数据库"""
    if isWarning:
        warning_tag = 1
    else:
        warning_tag = 0
    if isSingle:
        single_tag = 1
    else:
        single_tag = 2
    if isStable:
        stable_tag = 1
    else:
        stable_tag = 0

    sqldata_cu = sqldata.cursor()
    sqldata_cu.execute(
        "update ContainerInfo set Cam1Result='%s',Cam2Result='%s', CarLineNO = '%d',isWarning='%d',ReserveInt1='%d',ReserveInt2='%d' where rowid = 1" % (
        refinedResult[0], refinedResult[1], carChannel, warning_tag, single_tag, stable_tag))
    sqldata.commit()
    sqldata_cu.close()


def UpdateImgPath(sqldata, imname1, imname2):
    """&& 更新图片路径"""
    sqldata_cu = sqldata.cursor()
    sqldata_cu.execute("update ContainerInfo set ImgPath='%s'" % (imname1 + ' ' + imname2))
    sqldata.commit()
    sqldata_cu.close()