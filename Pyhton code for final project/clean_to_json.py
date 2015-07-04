# -*- coding: utf-8 -*-
"""
Created on Sun May 31 21:47:36 2015

@author: LinRui
"""

"""
This Pyhton script cleans the dataset from file HongKong.osm and then
saves the clean data to a JSON file hongkong.json.
The cleannig job includes two steps:
1. Filter out all the wrong located elements and just omit them when saving
 to the JSON file.
2. Update the over-abbreviated street names.
 
 Noted that the 'wrong located elements' are elements actually locate in Macau and 
 Shenzhen (two China cities adjacent to Hongkong), they should not appear in the
 dataset of the Hongkong area. You can see details in the pdf document.
"""

import xml.etree.cElementTree as ET
import codecs
import json
import re
import os

wdir='/Users/LinRui/Documents/Learning/Data_Science/Udacity/Data_Science_NanoDegree/project2'
file_in = 'HongKong.osm'
file_out = 'Hongkong-clean.json'

mapping = { "St": "Street",
            "St.": "Street",
            "Rd.": "Road",
            "Rd": "Road",
            "str": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "ave": "Avenue",
            "Bd": "Boulevard",
            "Blvd": "Boulevard"
            }

valid_element = {'node', 'way', 'relation'}            
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
wrong_el_re = re.compile(u'深圳|Shen Zhen|澳門|Macau', re.IGNORECASE)

# This method is to correct the over-abbriviate street name
def update_street_name(name, mapping):
    # Find the last word of 'name' and then replace it with the better word from mapping
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if street_type in mapping:
            better_word = mapping[street_type]
        sub_name = name[0:m.start()]
        better_name = sub_name + better_word
    else:
        better_name = name

    return better_name

# This method is to check if the element is wrong located in this Hong Kong city. 
# Some wrong located elements are from  Shenzhen and Macau, which are another two China cities adjacent to Hong Kong. 
def is_wrong_located_el(el):
    if el.find('tag') != None:
        sub_tag = el.find("tag[@k='tag']")
        if sub_tag != None:
            m = wrong_el_re.search(sub_tag.attrib['v'])
            if m:
                return True
    return False

# This method is to do the cleaning jobs and convert the dataset to JSON.
# Wrong located elements should by omitted when generateing the JSON file.
def clean_and_save(file_in, file_out):
        node = {}
        fo = codecs.open(file_out, "w", 'utf-8')
        with codecs.open(file_in, 'r') as fin:
            for _, el in ET.iterparse(fin):
                # Element should be "way", "node" or "relation"
                if el.tag not in valid_element:
                    continue 
                #To check if this element is a wrong located element. If yes, just ommit it.               
                elif is_wrong_located_el(el): 
                    continue
                else:
                    node['id'] = el.get('id')
                    node['type'] = el.tag
                    node['visible'] = el.get('visible')
                    node['created'] = {
                                      'version': el.get('version'),
                                      'changeset': el.get('changeset'),
                                      'timestamp': el.get('timestamp'),
                                      'user': el.get('user'),
                                      'uid': el.get('uid')
                                      }
                    sub_tags = el.findall('tag')
                    if sub_tags != []:                    
                        list_tag = []
                        for item in sub_tags:
                            k = item.attrib['k']
                            v = item.attrib['v']
                            # Update the over-abbreviated street name
                            if k == "addr:street":
                                v = update_street_name(v, mapping)
                            list_tag.append({'k': k, 'v': v})
                        node['tags'] = list_tag
                    members = el.findall('member')
                    if members != []:
                        list_member = []
                        for item in members:
                            list_member.append({'ref': item.attrib['ref'], 'role': item.attrib['role'], 'type': item.attrib['type']})
                        node['members'] = list_member
                    fo.write(json.dumps(node, ensure_ascii=False, indent = 0)+"\n")
        fo.close()
        
if __name__ == "__main__":
    os.chdir(wdir)    
    clean_and_save(file_in, file_out)        
                    
                    
                    
                
    
        