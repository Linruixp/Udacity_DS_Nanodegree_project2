# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 00:07:13 2015

@author: LinRui
"""

import xml.etree.ElementTree as ET
import pprint
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

def get_user(element):
    return


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if element.attrib.get('uid'):
            users.add(element.attrib['uid'])
        pass

    return users


def test():

    users = process_map('example.osm')
    pprint.pprint(users)
    assert len(users) == 6



if __name__ == "__main__":
    test()