# -*- coding: utf-8 -*-

class USPSXMLError(Exception):

    def __init__(self, element):
        self.info = {}
        for item in element.getchildren():
            self.info[item.tag] = item.text
            
        super(USPSXMLError, self).__init__(self.info['Description'])


class XMLTagNameError(Exception):

    def __init__(self, tag_name):
        error_string = "Tag %s is not defined in self.xml_tag_names" % tag_name
        super(XMLTagNameError, self).__init__(error_string)