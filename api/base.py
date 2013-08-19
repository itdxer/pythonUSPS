# -*- coding: utf-8 -*-
import urllib
import urllib2
from xml.etree import ElementTree
from xml.dom.minidom import *
from default.errors import USPSXMLError, XMLTagNameError


class USPSServiceSender(object):

    service_types = ("ExpressMail", 
                     "PriorityMail", 
                     "Returns", 
                     "International",
                     "OtherPackages",
                    )

    def __init__(self, url):
        self.url = url

    @property
    def root_tag(self):
        return "%sRequest" % self.api_key


    def send_request(self, list_of_xml_tags, user_id=None, password=None):
        """ " (dict, str, str) -> (class xml.etree.ElementTree.Element)
        Send request on USPS server and eturn object with XML tags
        """
        xml = self.build_xml(list_of_xml_tags, user_id, password)
        data = {'API': self.api_key, 'XML': xml}
        print "XML=" + xml

        response = urllib2.urlopen(self.url, urllib.urlencode(data))
        response_type = ElementTree.parse(response).getroot()

        if response_type.tag == 'Error':
            raise USPSXMLError(response_type)

        return response_type


    def build_xml_level(self, list_of_xml_tags, document, root):

        for iterator, xml_tag in enumerate(list_of_xml_tags):

            if not xml_tag["name"] in self.xml_tag_names:
                raise XMLTagNameError(xml_tag["name"])

            xml_tag_name = xml_tag["name"]
            this_xml_tag = document.createElement(xml_tag_name)

            xml_from_tag_dict = list_of_xml_tags[iterator]
            this_xml_tag_text = xml_from_tag_dict.get("text", None)

            # add attribute to tag
            if xml_from_tag_dict.get("attribute", None):
                xml_tag_attribute = xml_from_tag_dict["attribute"]

                tag_attr = document.createAttribute(xml_tag_attribute["name"])
                tag_attr.value = xml_tag_attribute["value"]

                this_xml_tag.setAttributeNode(tag_attr)

            if xml_from_tag_dict.get("inner_tags", None):
                this_xml_tag = self.build_xml_level(
                                    xml_from_tag_dict["inner_tags"],
                                    document, this_xml_tag
                               )
            elif this_xml_tag_text != None:
                this_xml_tag_text = document.createTextNode(this_xml_tag_text)
                this_xml_tag.appendChild(this_xml_tag_text)

            root.appendChild(this_xml_tag)
        return root


    def build_xml(self, list_of_xml_tags, user_id=None, password=None):
        """ (dict, str, str) -> (str)
        Get dictionary with XML tags and there parametrs
        Return XML in string format
        """
        document = Document()
        root = document.createElement(self.root_tag)

        if user_id is not None:
            user_id_attr = document.createAttribute('USERID')
            user_id_attr.value = user_id
            root.setAttributeNode(user_id_attr)

            if password is not None:
                user_id_attr = document.createAttribute('PASSWORD')
                user_id_attr.value = password
                root.setAttributeNode(user_id_attr)


        root = self.build_xml_level(list_of_xml_tags, document, root)

        document.appendChild(root)

        return document.toxml()


    def get_response_information(self, xml_response):
        """ (class xml.etree.ElementTree.Element) -> dict
        Return dictionary with all XML response information
        """
        response_info = {}

        for xml_tag in xml_response.getchildren():

            if xml_tag.tag == 'Error':
                raise USPSXMLError(xml_tag)

            if xml_tag.getchildren():
                response_info[xml_tag.tag] = self.get_response_information(xml_tag)
            elif xml_tag is not None:
                response_info[xml_tag.tag] = xml_tag.text

        return response_info

    def is_service_type_correct(self, service_type):
        """ (str) -> bool
        Return True if correct name of service type
        """
        return service_type in self.service_types

    def get_package_size_type(self, size):
        """ (int) -> str
        Return string type from size
        """
        return "REGULAR" if size <= 12 else "LARGE"


if __name__ == '__main__':
    pass