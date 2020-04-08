# import the necessary packages
from pyzbar import pyzbar
import argparse
import cv2
import xml.etree.ElementTree as ET
from PIL import Image


def get_aadhar_card_details(image_path):
	
	#image = cv2.imread(image_path)
	# find the barcodes in the image and decode each of the barcodes
	#img = cv2.resize(img, (640, 640))
	image = Image.open(image_path)
	barcodes = pyzbar.decode(image)

	print("len barcode", len(barcodes))
	if len(barcodes) == 0:
		details = {}
		details['Name'] = ''
		details['Father Name'] = ''
		details['Date of Birth'] = ''
		details['Number'] = ''
		details['Address'] = ''
		return {"status":False,
				"details":details}
	else:
		for barcode in barcodes:
			print("in barcode")
			# the barcode data is a bytes object so if we want to draw it on
			# our output image we need to convert it to a string first
			barcodeData = barcode.data.decode("utf-8")
			# barcodeType = barcode.type

			# converting data from string to xml
			tree = ET.ElementTree(ET.fromstring(barcodeData))
			root = tree.getroot()
			aadhar_data = root.attrib
			aadhar_number = aadhar_data['uid']
			name = aadhar_data['name']
			fname = aadhar_data['co'].replace("S/O", "")
			fname = fname.strip()
			if aadhar_data.get("dob"):
				dob = aadhar_data['dob']
			else:
				dob = aadhar_data['yob']

			address = aadhar_data['house'] + "," + aadhar_data['street'] + "," + aadhar_data['loc'] + "," + aadhar_data['vtc'] + "," + aadhar_data['dist'] + "," +\
					  aadhar_data['state'] + "," + aadhar_data['pc']
			details = {}
			details['Number'] = aadhar_number
			details['Name'] = name.upper()
			details['Father Name'] = fname.upper()
			details['Date of Birth'] = dob
			# details['Address'] = address.upper()
			details['Address'] = aadhar_data

			return {"status":True,
					"details":details}

