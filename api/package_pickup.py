# -*- coding: utf-8 -*-
from base import USPSServiceSender


class PickupAvailabilityPackage(USPSServiceSender):

    api_key = "CarrierPickupAvailability"
    xml_tag_names = ("FirmName", # max length 50
                     "SuiteOrApt", # max length 50
                     "Address2", # max length 50
                     "Urbanization", # max length 28
                     "City", # max length 30
                     "State", # max length 2
                     "ZIP4", # 4 digits
                     "ZIP5", # 5 digits
                     "Date", # Use this tag to request a pickup date/time
                    )

    def get_available_date_info(self, xml_response):
        """ (class xml.etree.ElementTree.Element) -> dict
        Return pickup date information in dictionary
        """
        date_info = {}

        # Day of week for pickup
        date_info['DayOfWeek'] = xml_response.find("DayOfWeek").text
        # Scheduled date for pickup 
        date_info['Date'] = xml_response.find("Date").text
        # Can be C for City, H for Highway, R for Rural
        date_info['CarrierRoute'] = xml_response.find("CarrierRoute").text 

        return date_info


class PickupSchedulePackage(PickupAvailabilityPackage):

    api_key = "CarrierPickupSchedule"
    xml_tag_names = ("FirmName", # max length 50
                     "LastName", # max length 50
                     "FirstName", # max length 50
                     "SuiteOrApt", # max length 50
                     "Address2", # max length 50
                     "Urbanization", # max length 28
                     "City", # max length 30
                     "State", # max length 2
                     "ZIP4", # 4 digits
                     "ZIP5", # 5 digits
                     "Phone", # Two formats are allowed: (###) 123-4567 or ###-123-4567 (max 14)
                     "Extention", # max length 4 
                     "Package", # parent tag for ServiceType and Count
                     "ServiceType", # 1 of 5 services types (you can check with method 'check_service_type')
                     "Count", # can be between 1 and 999
                     "EstimatedWeight", # weight from all packages being picked up (max length 5)
                     "PackageLocation",
                     "SpecialInstructions", #max length 255
                     "EmailAddress", # If provided, email notifications will be sent confirming package pickup
                    )

    package_locations = ("Front Door", 
                         "Back Door", 
                         "Side Door", 
                         "Knock on Door/Ring Bell",
                         "Mail Room",
                         "Office",
                         "Reception",
                         "In/At Mailbox",
                         "Other", # Other information must be indicate in tag SpecialInstructions
                        )


    def is_package_loc_correct(self, package_location):
        """ (str) -> bool
        Return True if correct package location
        """
        return package_location in self.package_locations

    def get_confirmation_number(self, xml_response):
        """ (class xml.etree.ElementTree.Element) -> str
        It's ID for pickup and with this information you can cancel pickup
        """
        return xml_response.find("ConfirmationNumber").text



class PickupCancelPackage(USPSServiceSender):

    api_key = "CarrierPickupCancel"
    xml_tag_names = ("FirmName", # max length 50
                     "SuiteOrApt", # max length 50
                     "Address2", # max length 50
                     "Urbanization", # max length 28
                     "City", # max length 30
                     "State", # max length 2
                     "ZIP5", # 5 digits
                     "ZIP4", # 4 digits
                     "ConfirmationNumber", # Enter exact Confirmation Number returned with Package Pickup Schedule request
                    )

    def get_status(self, xml_response):
        """ (class xml.etree.ElementTree.Element) -> str
        Return status information after Pickup cancel
        """
        return xml_response.find("Status").text