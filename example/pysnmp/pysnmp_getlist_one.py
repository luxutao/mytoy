#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@__Create Time__ = 17-7-2 下午12:11
@__Description__ = " 获得一个oid下面的多个值（第一种方法）"
"""

from pysnmp.hlapi.asyncore import *
import time


class SnmpLinuxServer(object):
    def __init__(self,oid):
        self.oid = oid
        # self.model = model
        self.snmpengine = SnmpEngine()
        self.communitydata = CommunityData('public')
        self.udptransporttarget = UdpTransportTarget(('192.168.1.100', 161))
        self.contextdata = ContextData()
        self.objecttype = ObjectType(ObjectIdentity(self.oid))
        self.time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def cpumonitor(self):
        errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(
            self.snmpengine, self.communitydata, self.udptransporttarget, self.contextdata, self.objecttype))
        value = varBinds[-1][-1]
        print(value)
        p = self.model.objects.create(time=self.time, value=value)
        p.save()

    def cbFun(self,snmpEngine, sendRequestHandle, errorIndication, errorStatus, errorIndex, varBinds, cbCtx):
        print(errorIndication, errorStatus, errorIndex, varBinds)

    def processmonitor(self):
        bulkCmd(
            self.snmpengine,
            self.communitydata,
            self.udptransporttarget,
            self.contextdata,
            0, 99999,
            self.objecttype,
            cbFun=self.cbFun
        )
        self.snmpengine.transportDispatcher.runDispatcher()


if __name__ == '__main__':
    q = SnmpLinuxServer('.1.3.6.1.2.1.25.4.2.1.2')
    q.processmonitor()
