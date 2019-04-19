#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@__Create Time__ = 17-7-1 下午10:32
@__Description__ = "获得空闲CPU单个值 "
"""

from pysnmp.hlapi import *
errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(
    SnmpEngine(),CommunityData('public'),UdpTransportTarget(('192.168.1.100', 161)),
    ContextData(),ObjectType(ObjectIdentity('. 1.3.6.1.4.1.2021.11.11.0'))))
print(varBinds)