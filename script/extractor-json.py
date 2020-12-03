import json
import glob
from lxml import etree

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}


def data_extractor(descs_list, output_dict):
	"""
	This function extract all the data from each desc.
	:param entries_list: a list of all descs
	:return: a dict with the data
	"""
	# For each desc, a dict retrieve all the data.
	for desc in descs_list:
		data = {}
		desc_id = desc.xpath('./@xml:id', namespaces=ns)[0]

		if desc.xpath('parent::tei:item/tei:measure[@quantity]', namespaces=ns):
			data["price"] = desc.xpath('parent::tei:item//tei:measure[@commodity="currency"]/@quantity', namespaces=ns)[0]
		else:
			data["price"] = None

		if desc.xpath('parent::tei:item/tei:name[@type="author"]/text()', namespaces=ns):
			data["author"] = desc.xpath('parent::tei:item/tei:name[@type="author"]/text()', namespaces=ns)[0]
		else:
			data["author"] = None

		if desc.xpath('./tei:date[@when]', namespaces=ns):
			data["date"] = desc.xpath('./tei:date/@when', namespaces=ns)[0]
		else:
			data["date"] = None

		if desc.xpath('./tei:measure[@type="length"]', namespaces=ns):
			data["number_of_pages"] = desc.xpath('./tei:measure[@type="length"]/@n', namespaces=ns)[0]
		else:
			data["number_of_pages"] = None

		if desc.xpath('./tei:measure[@type="format"]', namespaces=ns):
			data["format"] = desc.xpath('./tei:measure[@type="format"]/@ana', namespaces=ns)[0]
		else:
			data["format"] = None

		if desc.xpath('./tei:term', namespaces=ns):
			data["term"] = desc.xpath('./tei:term/@ana', namespaces=ns)[0]
		else:
			data["term"] = None

		if desc.xpath('ancestor::tei:TEI/tei:teiHeader//tei:sourceDesc//tei:date[@when]', namespaces=ns):
			data["sell_date"] = desc.xpath('ancestor::tei:TEI/tei:teiHeader//tei:sourceDesc//tei:date/@when', namespaces=ns)[0]
		else:
			data["sell_date"] = None

		# In order to check the data, we add its text in the dict.
		etree.strip_tags(desc, '{http://www.tei-c.org/ns/1.0}*')
		data["desc"] = desc.text

		output_dict[desc_id] = data

	return output_dict



if __name__ == "__main__":

	files = glob.glob("../Catalogues/**/*.xml", recursive=True)

	output_dict = {}

	for file in files:
		file = etree.parse(file)
		descs_list = file.xpath('//tei:text//tei:item//tei:desc', namespaces=ns)
		output_dict = data_extractor(descs_list, output_dict)


	with open('../output/export.json', 'w') as outfile:
		outfile.truncate(0)
		json.dump(output_dict, outfile)
    
