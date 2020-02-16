from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

from datetime import datetime


class Yml:
    def __init__(self, name, company, parser, yml_name,
                 url=None, platform=None, shop_version=None,
                 shop_agency=None, shop_email=None, shop_currencies=None):

        self.parser = parser
        self.categories = list(parser.get_categories())

        self.yml_name = yml_name

        self.shop_name = name
        self.shop_company = company
        self.shop_url = url
        self.shop_platform = platform
        self.shop_version = shop_version
        self.shop_agency = shop_agency
        self.shop_email = shop_email
        self.shop_currencies = shop_currencies

    def assemble_shop(self, yml_catalog):
        shop = SubElement(yml_catalog, "shop")

        shop_name = SubElement(shop, "name")
        shop_name.text = self.shop_name

        shop_company = SubElement(shop, "company")
        shop_company.text = self.shop_company

        if self.shop_url:
            shop_url = SubElement(shop, "url")
            shop_url.text = self.shop_url

        if self.shop_platform:
            shop_platform = SubElement(shop, "platform")
            shop_platform.text = self.shop_platform

        if self.shop_version:
            shop_version = SubElement(shop, "version")
            shop_version.text = self.shop_platform

        if self.shop_agency:
            shop_agency = SubElement(shop, "agency")
            shop_agency.text = self.shop_platform

        if self.shop_email:
            shop_email = SubElement(shop, "version")
            shop_email.text = self.shop_platform

        if self.shop_currencies:
            shop_currencies = SubElement(shop, "currencies")
            shop_currencies.text = self.shop_platform

        return shop

    def assemble_categories(self, yml_catalog):
        categories = SubElement(yml_catalog, "categories")
        # TODO ... +-
        for i, category in enumerate(self.categories):
            categories_ = Element('category', id=str(i))
            categories_.text = category
            categories.append(categories_)

        return categories

    def assemble_offer(self, offer_json, offer):
        for i in offer_json:

            if i["type"] == "category":
                type = Element("categoryId")
                type.text = str(self.categories.index(i["content"]))
                offer.append(type)
                break

            a = {}

            if i.get("unit"):
                a["unit"] = i["unit"]

            type = Element(i["type"], **a)
            type.text = str(i["content"])
            offer.append(type)

        return offer

    def assemble_param(self, params, offer):
        for key in params:

            print("-------")
            print(key)
            print(params[key])

            if len(params[key]) == 2:
                try:
                    float(params[key][0])
                    param_yml = Element("param", name=key, unit=params[key][-1])
                    param_yml.text = params[key][0]
                except:

                    param_yml = Element("param", name=key)
                    param_yml.text = " ".join(params[key][1])

            else:
                param_yml = Element("param", name=key)
                param_yml.text = " ".join(params[key])

            offer.append(param_yml)
        return offer

    def assemble_offers_params(self, yml_catalog):
        offers = SubElement(yml_catalog, "offers")

        for offer_, param in self.parser.parse():

            offer = Element("offer")
            self.assemble_offer(offer_, offer)
            self.assemble_param(param, offer)
            offers.append(offer)

        return offers

    def assemble(self):
        yml_catalog = Element("yml_catalog")#, date=None)
        self.assemble_shop(yml_catalog)
        self.assemble_categories(yml_catalog)
        self.assemble_offers_params(yml_catalog)

        yml_catalog = ElementTree(yml_catalog)

        yml_catalog.write(open(self.yml_name, 'wb'), xml_declaration=True ,  encoding='windows-1251')#,  encoding='UTF-8')
        return yml_catalog


import parser

if __name__ == '__main__':
    parser = parser.Parser("data/esus.xlsx",
                    [{"type": "a1", "required": True}, {"type": "a2", "unit": "a1", "required": True},
                     {"type": "param", "unit": "1", "required": True},
                     None, {"type": "a5", "unit": "1", "required": True},
                     {"type": "a6", "unit": "1", "required": True},
                     {"type": "a7", "unit": "1", "required": True}, {"type": "a8", "unit": "1", "required": True},
                     {"type": "image", "unit": "1", "required": True},
                     {"type": "a10", "unit": "1", "required": True}, {"type": "a11", "unit": "1", "required": True},
                     {"type": "a12", "unit": "1", "required": True},
                     {"type": "a13", "unit": "1", "required": True}, {"type": "a14", "unit": "1", "required": True},
                     {"type": "a15", "unit": "1", "required": True},
                     {"type": "a16", "unit": "1", "required": True},
                     {"type": "category", "unit": "1", "required": True}])

    name = "name"
    company = "company"
    yml_name = "yml.xml"
    Yml = Yml(name, company, parser, yml_name)
    Yml.assemble()
