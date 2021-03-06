#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string
from string import Template
import json

class ds2markdown():

    def __init__(self, content, thumbnail):
        self.thumbnail = thumbnail
        self.source = ""
        self.thdescription = "{0} {1} {2} {3} {4} {5} {6}".format(
            "**Scope:** {0}\n\n**Type:** {1}\n\n**Occurred:** {2}\n\n**Verified:** {3}\n\n**Modified:** {4}\n\n**Published:** {5}\n\n**Identifier:** {6}\n\n**Tags:** {7}\n\n".format(
                    content.get('scope',"None"),
                    content.get('type',"None"),
                    content.get('occurred',"None"),
                    content.get('verified',"None"),
                    content.get('modified',"None"),
                    content.get('published',"None"),
                    str(content.get('id',"None")),
                    self.tags(content)
            ),"----\n\n#### Summary ####  \n\n{}\n\n".format(content.get('summary')),
            "----\n\n#### Description ####  \n\n{}\n\n".format(content.get('description')),
            "{}\n\n".format(self.impactDescription(content)),
            "{}\n\n".format(self.mitigation(content)),
            "{}\n\n".format(self.entitySummary(content)),
            "{}\n\n".format(self.lci(content))

        )



    def entitySummary(self, content):
        source = ""
        if 'entitySummary' in content:
            c = content.get('entitySummary',"None")
            source += self.information(c)

            if 'summaryText' in c:
                summaryText = c.get('summaryText',"None")
                source += "\n\n----\n\n#### Source data #### \n\n" + \
                        "```\n{}\n```\n\n".format(summaryText)

        if 'IpAddressEntitySummary' in content:
            c = content.get('IpAddressEntity',"None")
            source = self.information(c)

            if 'IpAddressDetails' in c:
                details = c.get('IpAddressDetails',"None")
                source += "\n\n----\n\n" + \
                        "#### IP address details #### \n\n" + \
                        "**IP:** {0}\n\n**AS:** {1}\n\n**Reverse Domain Name:** {2}\n\n**Service Provider:** {3}\n\n".format(
                            details.get('ipAddress',"None"),
                            details.get('autonomousSystemNumber',"None"),
                            details.get('reverseDomainName',"None"),
                            details.get('serviceProvider',"None")
                             )
                if 'location' in details:
                    source += "**Geolocation:** " + details['location']['country'] + \
                                +"/"+ details['location']['city'] + "\n\n"

            if 'ports' in  c:
                port = c['ports']
                source += "\n\n----\n\n" + \
                        " #### Port details #### \n\n" + \
                        "**Port:** {0}/{1}\n\n**Scanned on:** {2}\n\n**Device Type:** {3}\n\n**Banner:** {4}\n\n".format(
                            port.get('portNumber',"None"),
                            port.get('transport',"None"),
                            port.get('scannedOn',"None"),
                            port.get('deviceType',"None"),
                            port.get('banner',"None")
                        )

            if 'vulnerability' in  c:
                vuln = c.get('vulnerability').get('specification').get('specification')
                source += "#### vulnerability Information ####  \n\n**CVE ID:** {0}\n\n**CVE description:** {1}\n\n**Severity:** {2}\n\n**Mitigation:** {3}\n\n".format(
                        vuln.get('cveId',"None"),
                        vuln.get('description',"None"),
                        vuln.get('severity',"None"),
                        vuln.get('mitigation',"None")
                )

        if 'MessageEntitySummary' in content:
            c = content['MessageEntitySummary']
            source += self.information(c)

            if 'conversationFragment' in c:
                conv = c.get('conversationFragment')
                source += "#### Conversation Information #### \n\n**Server:** {0}\n\n**Channel:** {1}\n\n".format(
                        conv.get('server',"None"),
                        conv.get('channel',"None")
                )
                if "Message" in conv:
                    msg = conv.get("Message")
                    source += "**Message**\n\n" + \
                            "**User:** " + \
                            "\"{0}\" - {1}\n\n**Sent:** {2}\n\n**Message**\n\n```\n\n{3}\n\n```".format(
                                msg.get('nickname',"None"),
                                msg.get('username',"None"),
                                msg.get('sent',"None"),
                                msg.get('content',"None")
                                )

        return source


    def information(self, content):
        source = ""
        if self.thumbnail.get('thumbnail') != "":
            source += "----\n\n" + \
                "#### Source Information #### \n\n" + \
                "**Source:** {0}\n\n**Domain:** {1}\n\n**Date:** {2}\n\n**Type:** {3}\n\n![thumbnail][thumb]\n\n[thumb]: {4}\n\n".format(
                        content.get('source',"None"),
                        content.get('domain',"None"),
                        content.get('sourceDate',"None"),
                        content.get('type',"None"),
                        self.thumbnail.get('thumbnail', "None")
                )
        else:
            source += "----\n\n" + \
                "#### Source Information #### \n\n" + \
                "**Source:** {0}\n\n**Domain:** {1}\n\n**Date:** {2}\n\n**Type:** {3}\n\n".format(
                        content.get('source',"None"),
                        content.get('domain',"None"),
                        content.get('sourceDate',"None"),
                        content.get('type',"None")
                )

        if 'dataBreach' in content:
            dataBreach = content.get('dataBreach')

            source += "----\n\n#### Databreach target ####  \n\n" + \
                        "**Title:** {0}\n\n**Target domain:** {1}\n\n**Published:** {2}\n\n**Occured:** {3}\n\n**Modified:** {4}\n\n**Id:** {5}\n\n".format(
                                dataBreach.get('title',"None"),
                                dataBreach.get('domainName',"None"),
                                dataBreach.get('published',"None"),
                                dataBreach.get('occurred',"None"),
                                dataBreach.get('modified',"None"),
                                dataBreach.get('id', "None")
                        )

        if 'secureSocketInspection' in content:
            source += "----\n\n#### Technical information #### \n\n ```\n\n{}\n\n```".format( json.dumps(content.get('secureSocketInspection'),  indent=4))


        return source


    def impactDescription(self, content):
        impact = ""
        if "impactDescription" in content:
            impact = "----\n\n#### Impact Description #### \n\n{}" .format(
                    content.get('impactDescription', "None")
            )

        return impact

    def mitigation(self, content):
        mitigation = ""
        if "mitigation" in content:
            mitigation = "----\n\n#### Mitigation #### \n\n{}".format(content.get('mitigation', "None"))
        return mitigation


    def lci(self, content):
        linkedContentIncidents = "----\n\n#### Linked incidents #### \n\n"
        if content.get("linkedContentIncidents"):
            for lci in content["linkedContentIncidents"]:
                linkedContentIncidents += "- {} \n\n".format(lci)
        else:
            linkedContentIncidents += "None"
        return linkedContentIncidents


    def tags(self, content):
        if 'tags' in content:
            t = ""
            for tag in content['tags']:
                if tag.get('name'):
                    if t != "":
                        t +=", "
                    t += "_{}_".format(tag['name'])
            return t
        return "-"

def databreach_message(ioc):
    """
    Return description for an observable created from a databreach record
    :param ioc: dict
    :return: str
    """
    databreach_observable_message_template = "**Databreach record from DigitalShadows** \n\n"+\
              "Password: $password\n\n"+\
              "Published: $published\n\n\n\n"+\
              "**Seen in previous breaches**\n\n"+\
              "  - Raw text: $rawtext\n\n"+\
              "  - Username: $username\n\n"+\
              "  - Username & password: $usernamepassword"
    message = Template(databreach_observable_message_template).substitute(
        password=ioc.get('password', '-- No password found -- '),
        published=ioc.get('published', 'None'),
        rawtext=ioc.get('priorRowTextBreachCount', "0"),
        username=ioc.get('priorUsernameBreachCount', "0"),
        usernamepassword=ioc.get('priorUsernameBreachCount', "0"))
    return message


