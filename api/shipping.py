from base import USPSServiceSender


class Shippining(USPSServiceSender):

    def is_container_correct(self, container):
        """ (str) -> bool
        Return True if correct container type
        """
        return container in self.containers

    def save_image_label_to(self, xml_response, path):
        """
        Save image in file
        """
        with open(path, 'wb') as f:
            label = xml_response.find(self.image_label).text
            binary = a2b_base64(raw_epl)
            f.write(binary)


class DomesticShipping(Shippining):

    image_label = "EMLabel"
    api_key = "ExpressMailLabelCertify"
    xml_tag_names = ('Revision', # value must be 2
                     'FromFirstName', #max length 26
                     'FromLastName', #max length 26
                     'FromFirm', #max length 26
                     'FromAddress1', #max length 26
                     'FromAddress2', #max length 26
                     'FromCity', #max length 13
                     'FromState', #length 2
                     'FromZip5', #length 5
                     'FromZip4', #length 4
                     'FromPhone', #digits 10
                     'ToFirstName', #max length 26
                     'ToLastName', #max length 26
                     'ToFirm', #max length 26
                     'ToAddress1', #max length 26
                     'ToAddress2', #max length 26
                     'ToCity', #max length 13
                     'ToState', #length 2
                     'ToZip5', #length 5
                     'ToZip4', #length 4
                     'ToPhone', #digits 10
                     'WeightInOunces', #digits 4 (max weight 70 pounds)
                     'POZipCode', #Post Office zip code (max length 5)
                     'FacilityType', #choose in variable 'facility_types'
                     'ImageType', # in PDF or in GIF
                     'LabelDate', # Date Package Will Be Mailed. formats (dd-mmm-yyyy or mm/dd/yyyy)
                     'SenderName', # Name of E-mail Sender.
                     'SenderEMail', # E-mail Address of Sender. Valid e-mail addresses must be used.
                     'SenderEMail', # E-mail Address of Sender. Valid e-mail addresses must be used.
                     'RecipientName', # Name of E-mail Recipient  
                     'RecipientEMail', # E-mail Address of Recipient. Valid e-mail addresses must be used.
                     'InsuredAmount', # Use this tag for entering an insurance amount. max value 9999.99
                     'Container', # choose in variable 'containers'
                     'Size', # get from method 'get_package_size_type
                     'Width', # if Size is LARGE
                     'Length', # if Size is LARGE
                     'Height', # if Size is LARGE
                     'Girth', # if Size is LARGE and Container is NONRECTANGULAR 
                    )

    containers = ("VARIABLE", 
                  "RECTANGULAR",
                  "NONRECTANGULAR ",
                  "FLAT RATE ENVELOPE",
                  "LEGAL FLAT RATE ENVELOPE",
                  "PADDED FLAT RATE ENVELOPE",
                  "FLAT RATE BO")
    
    facility_types = ("DDU", 
                      "SCF", 
                      "BMC", 
                      "ADC", 
                      "ASF")

    def is_facility_type_correct(self, facility_type):
        """ (str) -> bool
        Return True if correct facility type
        """
        return facility_type in self.facility_types

    def get_shipping_info(self, xml_response):
        """
        get shippining information about Postage and Confirmation number
        """
        return {'postage': xml_response.find('Postage'),
                'confirm_number': xml_response.find('EMConfirmationNumber')}


class InternationalShipping(Shippining):

    image_label = "LabelImage"
    api_key = "ExpressMailIntlCertify"
    xml_tag_names = ('Revision', # value must be 2
                     'FromFirstName', #max length 30
                     'FromMiddleInitial', #max length 1
                     'FromLastName', #max length 30
                     'FromFirm', #max length 32
                     'FromAddress1', #max length 32
                     'FromAddress2', #max length 32
                     'FromUrbanization', #max length 32
                     'FromCity', #max length 13
                     'FromState', #length 2
                     'FromZip5', #length 5
                     'FromZip4', #length 4
                     'FromPhone', #digits 10
                     'ToFirstName', #max length 30
                     'ToLastName', #max length 30
                     'ToFirm', #max length 36
                     'ToAddress1', #max length 36
                     'ToAddress2', #max length 36
                     'ToAddress3', #max length 36
                     'ToProvince', #max length 9
                     'ToPostalCode', #max length 9
                     'ToCity', # length 1 - 18
                     'ToState', #length 2
                     'ToZip5', #length 5
                     'ToZip4', #length 4
                     'ToEmail', # max_length 30. pattern=([\w\-\.]+)@(([\w-]+\.)+)[a-zAZ]{2,4} 
                     'ToPhone', # max length 30 (ex. 011 52 (322) 222-0069)
                     'ShippingContents',
                     'ItemDetail',
                     'Description',
                     'Quantity',
                     'Value',
                     'NetPounds',
                     'NetOunces',
                     'CountryOfOrigin',
                     'NetOunces',
                     'ContentType', # get from 'content_types'
                     'ContentTypeOther', # if ContentType is OTHER
                     'ImageType', # PDF or TIF
                     'ImageLayout', # get from 'image_layouts'
                     'LabelDate', # Date the mail will enter the mail stream. No more than 3 days in the future
                     'Size', # get from method 'get_package_size_type
                     'Width', # if Size is LARGE
                     'Length', # if Size is LARGE
                     'Height', # if Size is LARGE
                     'Girth', # if Size is LARGE and Container is NONRECTANGULAR 
                    )

    containers = ("VARIABLE",
                  "FLATRATEENV",
                  "LEGALFLATRATEENV",
                  "PADDEDFLATRATEENV",
                  "FLATRATEBOX",
                  "RECTANGULAR",
                  "NONRECTANGULAR")

    image_layouts = ("ONEPERFILE",
                     "ALLINONEFILE",
                     "TRIMONEPERFILE",
                     "TRIMALLINONEFIL")

    content_types = ("MERCHANDISE",
                     "SAMPLE",
                     "GIFT",
                     "DOCUMENTS",
                     "RETURN",
                     "HUMANITARIAN",
                     "DANGEROUSGOODS",
                     "OTHER")

    def is_content_type_correct(self, content_type):
        """ (str) -> bool
        Return True if correct facility type
        """
        return content_type in self.content_types

    def get_shipping_info(self, xml_response):
        """
        get shippining information from response
        """
        return {'prohibitions': xml_response.find('Prohibitions'),
                'restrictions': xml_response.find('restrictions'),
                'observations': xml_response.find('Observations'),
                'regulations': xml_response.find('Regulations'),
                'barcode_number': xml_response.find('BarcodeNumber'),
                'postage': xml_response.find('Postage'),
                'total_value': xml_response.find('TotalValue'),
                'sdr_value': xml_response.find('SDRValue')}