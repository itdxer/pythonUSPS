# -*- coding: utf-8 -*-
import logging
from xml.dom.minidom import parseString
from default.settings import *
from api.tracking import Tracking
from api.package_pickup import (PickupCancelPackage, 
                                PickupSchedulePackage,
                                PickupAvailabilityPackage)
from api.shipping import DomesticShipping, InternationalShipping
from api.rate_calculator import (DomesticRateCalculator, 
                                 InternationalRateCalculator)

def track_test():
    print "-" * 50
    print "Track Test"
    usps = Tracking(USPS_CONNECTION_TEST_PRODUCTION)
    data = [{"name": "TrackID",
             "text": "",
             "attribute": {"name": "ID", "value": "EJ958083578US"}}]

    tracking_response = usps.send_request(data, USERNAME)
    print type(tracking_response)
    print "Track status:\n%s" % usps.get_tracking_information(tracking_response)


def domestic_rate_test():
    print "-" * 50
    print "Domestic Rate Test"
    usps = DomesticRateCalculator(USPS_CONNECTION)
    data = [{"name": "Revision", "text": "2"},
            {"name": "Package",
             "attribute": {"name": "ID", "value": "1"},
             "inner_tags": [
                  {"name": "Service", "text": "PRIORITY"},
                  {"name": "ZipOrigination", "text": "44106"},
                  {"name": "ZipDestination", "text": "20770"},
                  {"name": "Pounds", "text": "1"},
                  {"name": "Ounces", "text": "8"},
                  {"name": "Container", "text": "NONRECTANGULAR"},
                  {"name": "Size", "text": "LARGE"},
                  {"name": "Width", "text": "35"},
                  {"name": "Length", "text": "30"},
                  {"name": "Height", "text": "15"},
                  {"name": "Girth", "text": "55"}
             ]}]

    domestic_rate_response = usps.send_request(data, USERNAME)
    rate_info = usps.get_postage_from_response(domestic_rate_response)

    for info in rate_info:
      print "Rate: %s" % info["Rate"]


def international_rate_test():
    print "-" * 50
    print "International Rate Test"
    usps = InternationalRateCalculator(USPS_CONNECTION)
    data = [{"name": "Revision", "text": "2"},
            {"name": "Package",
             "attribute": {"name": "ID", "value": "1"},
             "inner_tags": [
                  {"name": "Pounds", "text": "15"},
                  {"name": "Ounces", "text": "0"},
                  {"name": "Machinable", "text": "True"},
                  {"name": "MailType", "text": "Package"},
                  {"name": "ValueOfContents", "text": "200"},
                  {"name": "Country", "text": "Canada"},
                  {"name": "Container", "text": "RECTANGULAR"},
                  {"name": "Size", "text": "LARGE"},
                  {"name": "Width", "text": "10"},
                  {"name": "Length", "text": "15"},
                  {"name": "Height", "text": "10"},
                  {"name": "Girth", "text": "0"},
                  {"name": "CommercialFlag", "text": "N"},
             ]}]

    international_rate_response = usps.send_request(data, USERNAME)
    for x in  international_rate_response.getchildren()[0].getchildren():
        # print '-'*50, x.tag
        # print x.text or x.getchildren()
        pass
    services_info = usps.get_postage_from_response(international_rate_response)

    for rate_info in services_info:
      print "Rate: %s" % rate_info


def domestic_shipping_test():
    print "-" * 50
    print "Domestic Shipping Test"
    usps = DomesticShipping(USPS_CONNECTION_SECURE)
    data = [{"name": "Revision", "text": "2"},
            {"name": "FromFirstName", "text": "Adam"},
            {"name": "FromLastName", "text": "Smith"},
            {"name": "FromFirm"},
            {"name": "FromAddress1", "text": "2"},
            {"name": "FromAddress2", "text": "2"},
            {"name": "FromCity", "text": "Washington"},
            {"name": "FromState", "text": "DC"},
            {"name": "FromZip5", "text": "20260"},
            {"name": "FromZip4"},
            {"name": "FromPhone", "text": "2125551234"},
            {"name": "ToFirstName", "text": "Janice"},
            {"name": "ToLastName", "text": "Dickens"},
            {"name": "ToFirm", "text": "XYZ Corporation"},
            {"name": "ToAddress1", "text": "Ste 100"},
            {"name": "ToAddress2", "text": "2 Massachusetts Ave NE"},
            {"name": "ToLastName", "text": "Dickens"},
            {"name": "ToCity", "text": "Washington"},
            {"name": "ToState", "text": "DC"},
            {"name": "ToZip5", "text": "20212"},
            {"name": "ToZip4"},
            {"name": "ToPhone", "text": "2125551234"},
            {"name": "WeightInOunces", "text": "105"},
            {"name": "ImageType", "text": "GIF"},
            {"name": "LabelDate", "text": "10/19/2010"},
            {"name": "SenderName", "text": "Adam Smith"},
            {"name": "SenderEMail", "text": "asmith@email.com"},
            {"name": "RecipientName", "text": "Janice Dickens"},
            {"name": "RecipientEMail", "text": "jdickens@email.com"},
            {"name": "Container", "text": "NONRECTANGULAR"},
            {"name": "Size", "text": "LARGE"},
            {"name": "Width", "text": "7"},
            {"name": "Length", "text": "20.5"},
            {"name": "Height", "text": "15"},
            {"name": "Girth", "text": "60"},
           ]

    shipping_response = usps.send_request(data, USERNAME, PASSWORD)
    shippining_info = usps.get_shipping_info(shipping_response)

    print 'Postage: %s' % shippining_info['postage']
    print 'Confirmation Number: %s' % shippining_info['confirm_number']

    usps.save_image_label_to(shipping_response, './test_image_domestic.gif')


def international_shipping_test():
    print "-" * 50
    print "International Shipping Test"
    usps = InternationalShipping(USPS_CONNECTION_SECURE)
    data = [{"name": "Revision", "text": "2"},
            {"name": "FromFirstName", "text": "Adam"},
            {"name": "FromLastName", "text": "Smith"},
            {"name": "FromFirm"},
            {"name": "FromAddress1", "text": "2"},
            {"name": "FromAddress2", "text": "2"},
            {"name": "FromCity", "text": "Washington"},
            {"name": "FromState", "text": "DC"},
            {"name": "FromZip5", "text": "20260"},
            {"name": "FromZip4"},
            {"name": "FromPhone", "text": "2125551234"},
            {"name": "ToFirstName", "text": "Janice"},
            {"name": "ToLastName", "text": "Dickens"},
            {"name": "ToFirm", "text": "XYZ Corporation"},
            {"name": "ToAddress1", "text": "Ste 100"},
            {"name": "ToAddress2", "text": "2 Massachusetts Ave NE"},
            {"name": "ToLastName", "text": "Dickens"},
            {"name": "ToCity", "text": "Washington"},
            {"name": "ToState", "text": "DC"},
            {"name": "ToZip5", "text": "20212"},
            {"name": "ToZip4"},
            {"name": "ShippingContents",
             "inner_tags": [
                  {"name": "ItemDetail",
                   "inner_tags": [
                      {"name": "Description", "text": "Description 1"},
                      {"name": "Quantity", "text": "1"},
                      {"name": "Value", "text": "1.11"},
                      {"name": "NetPounds", "text": "1"},
                      {"name": "NetOunces", "text": "1"},
                      {"name": "CountryOfOrigin", "text": "Brazil"}
                  ]},
             ]},
            {"name": "ToPhone", "text": "2125551234"},
            {"name": "ImageType", "text": "TIF"},
            {"name": "LabelDate", "text": "10/19/2010"},
            {"name": "Size", "text": "LARGE"},
            {"name": "Width", "text": "7"},
            {"name": "Length", "text": "20.5"},
            {"name": "Height", "text": "15"},
            {"name": "Girth", "text": "60"}
           ]

    shipping_response = usps.send_request(data, USERNAME, PASSWORD)
    shippining_info = usps.get_shipping_info(shipping_response)

    print 'Postage: %s' % shippining_info['postage']
    print 'Confirmation Number: %s' % shippining_info['confirm_number']

    usps.save_image_label_to(shipping_response, './test_image_intl.tif')


def pickup_available_test():
    print "-" * 50
    print "Pickup Test"
    usps = PickupAvailabilityPackage(USPS_CONNECTION_SECURE)
    data = [{"name": "FirmName", "text": "ABC Corp."},
            {"name": "SuiteOrApt", "text": "Suite 777"},
            {"name": "Address2", "text": "1390 Market Street"},
            {"name": "Urbanization", "text": ""},
            {"name": "City", "text": "Houston"},
            {"name": "State", "text": "TX"},
            {"name": "ZIP5", "text": "77058"},
            {"name": "ZIP4", "text": "1234"},
            {"name": "Date", "text": "2006-05-04T18:13:51.0Z"},
           ]
    pickup_response = usps.send_request(data, USERNAME)
    print usps.get_available_date_info(pickup_response)


def pickup_schedule_test():
    print "-" * 50
    print "Pickup Test"
    usps = PickupSchedulePackage(USPS_CONNECTION_SECURE)
    data = [{"name": "FirstName", "text": "John"},
            {"name": "LastName", "text": "Doe"},
            {"name": "FirmName", "text": "ABC Corp."},
            {"name": "Extention"},
            {"name": "SuiteOrApt", "text": "Suite 777"},
            {"name": "Address2", "text": "1390 Market Street"},
            {"name": "Urbanization", "text": ""},
            {"name": "City", "text": "Houston"},
            {"name": "State", "text": "TX"},
            {"name": "ZIP5", "text": "77058"},
            {"name": "ZIP4", "text": "1234"},
            {"name": "Phone", "text": "(555) 555-1234"},
            {"name": "Extention", "text": "201"},
            {"name": "Package",
             "inner_tags": [
                  {"name": "ServiceType", "text": "ExpressMail"},
                  {"name": "Count", "text": "2"},
             ]},
            {"name": "Package",
             "inner_tags": [
                  {"name": "ServiceType", "text": "PriorityMail"},
                  {"name": "Count", "text": "1"},
             ]},
            {"name": "EstimatedWeight", "text": "14"},
            {"name": "PackageLocation", "text": "Front Door"},
            {"name": "SpecialInstructions", "text": "Packages are behind the screen door."},

           ]
    pickup_schedule_response = usps.send_request(data, USERNAME)
    print "Confirmation Number: %s" % usps.get_confirmation_number(pickup_schedule_response)


def pickup_cancel_test():
    print "-" * 50
    print "Pickup Cansel Test"
    usps = PickupCancelPackage(USPS_CONNECTION_SECURE)
    data = [{"name": "FirmName", "text": "ABC Corp."},
            {"name": "SuiteOrApt", "text": "Suite 777"},
            {"name": "Address2", "text": "1390 Market Street"},
            {"name": "Urbanization", "text": ""},
            {"name": "City", "text": "Houston"},
            {"name": "State", "text": "TX"},
            {"name": "ZIP5", "text": "77058"},
            {"name": "ZIP4", "text": "1234"},
            {"name": "ConfirmationNumber", "text": "WTC123456789"},
           ]
    pickup_cancel_response = usps.send_request(data, USERNAME)
    print usps.get_status(pickup_cancel_response)


if __name__ == '__main__':
    # Test Shippining
    # domestic_shipping_test() # not active now
    # international_shipping_test() # not active now

    # Test Track
    # track_test() # active

    # Test Rate
    # domestic_rate_test() # active
    # international_rate_test() # active

    # Test Pickup features
    # pickup_available_test() # not active
    pickup_schedule_test() # not active
    pickup_cancel_test() # not active