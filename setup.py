#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: jqzhang
# Mail: s_jqzhang@163.com
# Created Time:  2018-11-27 19:17:34
#############################################

from setuptools import setup, find_packages

setup(
    name = "gevent_jobs",
    version = "0.0.2",
    keywords = ("pip","gevent jobs"),
    description = "gevent jobs",
    long_description = "gevent jobs",
    license = "MIT Licence",
    packages=find_packages(),
    url = "https://github.com/sjqzhang/gevent_jobs",
    author = "jqzhang",
    author_email = "s_jqzhang@163.com",
    include_package_data = True,
    platforms = "any",
)
