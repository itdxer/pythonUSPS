# -*- coding: utf-8 -*-
from base import USPSServiceSender


class Tracking(USPSServiceSender):

    api_key = "TrackV2"
    root_tag = "TrackRequest"
    xml_tag_names = ("TrackID",)

    def get_tracking_information(self, xml_response):
        """
        Return all tracking information in string format
        """
        track_info = xml_response.find("TrackInfo")
        information = []

        for info_part in track_info:
            information.append(info_part.text)

        return " ".join(information)