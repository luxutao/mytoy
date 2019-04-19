#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@__Create Time__ = 17-7-2 下午12:34
@__Description__ = "获取一个oid下的多个值（第二种方法） "
"""

from pysnmp.hlapi.twisted import *
from twisted.internet.task import react
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

    def success(self,args):
        (errorStatus, errorIndex, varBindTable) = args
        print(errorStatus, errorIndex, varBindTable)

    def failure(self,errorIndication):
        print(errorIndication)

    def processmonitor(self,reactor):
        d = bulkCmd(self.snmpengine, self.communitydata, self.udptransporttarget, self.contextdata, 0, 99999,
                self.objecttype)
        d.addCallback(self.success).addErrback(self.failure)
        return d


if __name__ == '__main__':
    q = SnmpLinuxServer('.1.3.6.1.2.1.25.4.2.1.2')
    react(q.processmonitor)