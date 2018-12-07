#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/11/
from sqlalchemy import Column, String, Integer, TEXT
from sqlalchemy.ext.declarative import declarative_base

# echo=True show information
Base = declarative_base()  # Generation ORM base class


class GateInfo(Base):
    __tablename__ = 'Gate_gateinfo'

    id = Column(Integer, primary_key=True)
    PlateResult = Column(String(18))
    Remark = Column(String(18))

    FinalResult1 = Column(String(50))
    DetectFace1 = Column(String(8))
    ContainerImpath1 = Column(String(150))
    FinalResult2 = Column(String(50))
    DetectFace2 = Column(String(8))
    ContainerImpath2 = Column(String(150))

    PlateImpath = Column(String(150))
    DangerousGoods1 = Column(String(150))
    Sealing1 = Column(String(8))
    ExamineImgTop = Column(String(150))
    ExamineImgLeft = Column(String(150))
    ExamineImgRight = Column(String(150))
    ExamineImgFront = Column(String(150))
    ExamineImgBack = Column(String(150))
    Lane = Column(String(8))
    LaneInOut = Column(String(8))
    EmptyFullStatus = Column(String(8))
    HighLowBoard = Column(String(8))
    Token = Column(String(18))
    Timestamp = Column(String(20))
    HangPlateResult = Column(String(18))
    HangPlateImpath = Column(String(150))
    FinalResult1Check = Column(String(18))
    FinalResult2Check = Column(String(18))

    BasicLog = Column(TEXT)

    C1TypeCheck = Column(String(6))
    C2TypeCheck = Column(String(6))
    DangerousGoods2 = Column(String(150))
    PlateCheck = Column(String(6))
    Sealing2 = Column(String(8))
    SideImpath1 = Column(String(255))
    SideImpath2 = Column(String(255))

    def __repr__(self):
        return "<GateInfo(id='%s', PlateResult='%s', Remark='%s', FinalResult1='%s'......)>" % (
            self.id, self.PlateResult, self.Remark, self.FinalResult1)

    def get_value_by_name(self, field_name):
        if hasattr(self, field_name):
            return getattr(self, field_name)
        return None

    def set_value_by_name(self, field_name, value):
        if hasattr(self, field_name):
            return setattr(self, field_name, value)

    def set_value(self, **kwargs):
        for key in kwargs.keys():
            if hasattr(self, key):
                return setattr(self, key, kwargs.get(key))

