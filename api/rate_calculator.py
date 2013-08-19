# -*- coding: utf-8 -*-
from base import USPSServiceSender


class DomesticRateCalculator(USPSServiceSender):

    api_key = 'RateV4'
    xml_tag_names = ('Package', # can bebetween 1 to 25 packages (must be unique ID)
                     'Revision', # For full RateV4 functionality use Revision=“2”
                     'Service', # one from list 'services'
                     'FirstClassMailType', # one from list 'class_mail_type'
                     'ZipOrigination', # max length 5
                     'ZipDestination', # max length 5
                     'Pounds', # max 70 pounds
                     'Ounces', # max 120 ounces (and max 10 digits)
                     'Container', # choose on from list 'containers'
                     'Size', # getted from method 'get_package_size_type'
                     'Width', # if Size is LARGE
                     'Length', # if Size is LARGE
                     'Height', # if Size is LARGE
                     'Girth', # if Size is LARGE and Container is NONRECTANGULAR or VARIABLE
                     'Value', # max digits 10
                     'AmountToCollect', # max digits 10
                     'Machinable', 
                     'ReturnLocations', 
                     'ShipDate')

    services = ("FIRST CLASS",
                "FIRST CLASS COMMERCIAL",
                "FIRST CLASS HFP COMMERCIAL",
                "PRIORITY",
                "PRIORITY COMMERCIAL",
                "PRIORITY CPP",
                "PRIORITY HFP COMMERCIAL",
                "PRIORITY HFP CPP",
                "EXPRESS",
                "EXPRESS COMMERCIAL",
                "EXPRESS CPP",
                "EXPRESS SH",
                "EXPRESS SH COMMERCIAL",
                "EXPRESS HFP",
                "EXPRESS HFP COMMERCIAL",
                "EXPRESS HFP CPP",
                "STANDART POST",
                "MEDIA",
                "LIBRARY",
                "ALL",
                "ONLINE",
                "PLUS"
               )

    def is_service_name_correct(self, service):
        """ (str) -> bool
        Return True if correct service name
        """
        return service in self.services

    class_mail_types = ("LETTER",
                        "FLAT",
                        "PARCEL",
                        "POSTCARD",
                        "PACKAGE SERVICE"
                       )

    def is_class_mail_types_correct(self, class_mail_type):
        """ (str) -> bool
        Return True if correct class mail type
        """
        return class_mail_type in self.class_mail_types

    containers = ("VARIABLE",
                  "FLAT RATE ENVELOPE",
                  "PADDED FLAT RATE ENVELOPE",
                  "LEGAL FLAT RATE ENVELOPE",
                  "SM FLAT RATE ENVELOPE",
                  "WINDOW FLAT RATE ENVELOPE",
                  "GIFT CARD FLAT RATE ENVELOPE",
                  "FLAT RATE BOX",
                  "SM FLAT RATE BOX",
                  "MD FLAT RATE BOX",
                  "LG FLAT RATE BOX",
                  "REGIONALRATEBOXA",
                  "REGIONALRATEBOXB",
                  "REGIONALRATEBOXC",
                  "RECTANGULAR",
                  "NONRECTANGULAR",
                 )

    def is_container_type_correct(self, container):
        """ (str) -> bool
        Return True if correct container type
        """
        return container in self.containers

    def get_postage_from_response(self, xml_response):
        """ (class xml.etree.ElementTree.Element) -> list
        Return dictionary with all Postage information
        """
        postages = xml_response.find("Package").findall("Postage")
        postages_list = []

        if postages:
            for postage in postages:
                postages_list.append(self.get_response_information(postage))

        return postages_list


class InternationalRateCalculator(USPSServiceSender):
    
    api_key = 'IntlRateV2'
    xml_tag_names = ('Package', # can bebetween 1 to 25 packages (must be unique ID)
                     'Revision', # Optional for base IntlRateV2 functionality (value 2) 
                     'Pounds', # max 70 pounds
                     'Ounces', # max 70 pounds
                     'Machinable',
                     'Country',
                     'Container', # use when LARGE size (RECTANGULAR or NONRECTANGULAR)
                     'Size', # getted from method 'get_package_size_type'
                     'Width', # if Size is LARGE
                     'Length', # if Size is LARGE
                     'Height', # if Size is LARGE
                     'Girth', # if Size is LARGE and Container is NONRECTANGULAR or VARIABLE
                     'OriginZip', # length 5
                     'CommercialFlag', # Returns commercial base postage. Can be Y or N
                     'CommercialPlusFlag', # Returns commercial plus postage. Can be Y or N
                     'MailType',
                     'Length',
                     'Width',
                     'Height',
                     'POBoxFlag',
                     'GiftFlag',
                     'ValueOfContents',
                     'Country')

    mail_types = ("All",
                  "Package",
                  "Postcards or aerogrammes",
                  "Envelope",
                  "LargeEnvelope",
                  "FlatRate",
                 )

    def is_mail_types_correct(self, mail_type):
        """ (str) -> bool
        Return True if correct mail type
        """
        return mail_type in self.mail_types

    def get_postage_from_response(self, xml_response):
        """ (class xml.etree.ElementTree.Element) -> list
        Return dictionary with all Postage information
        """
        services = xml_response.find("Package").findall("Service")
        postages_list = []

        if services:
            for postages in services:
                postages_list.append(postages.find("Postage").text)

        return postages_list