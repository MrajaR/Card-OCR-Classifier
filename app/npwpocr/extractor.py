import easyocr
import cv2
import numpy as np
import re
import json

class NPWPInformation():
  def __init__(self):
    self.npwpId = ''
    self.name = ''
    self.nik = ''
    self.address = ''
    self.kpp = ''
    self.registeredDate = ''

class NPWPOCR():
  def __init__(self, image, reader):
    # self.images = cv2.imread(image)
    width, height, _ = image.shape

    # Calculate the new heights for cropping
    cropped = int(0.15* height)  # 75% for the bottom

    # Crop the bottom 25% of the image
    self.cropped_img = image[cropped:, :]

    self.gray_img = cv2.cvtColor(self.cropped_img, cv2.COLOR_BGR2GRAY)
    # self.equalized_image = cv2.equalizeHist(self.gray_img)
    self.threshed_img = cv2.threshold(self.gray_img, 120, 255, cv2.THRESH_TRUNC)[1]

    self.result = NPWPInformation()
    self.reader = reader
    self.master_process()


  def text_detection(self, image):
    list_ocr_result = self.reader.readtext(image, detail=0)
    raw_text = ' '.join(list_ocr_result).lower()

    return raw_text

#   def replace_word(self, raw_text):
#     replacement_dict = {
#         '|' : '',
#         'namz' : 'nama',
#         'namo' : 'nama',
#         'alamal' : 'alamat',
#         'alamai' : 'alamat',
#         'narna' : 'nama',
#         'langgal' : 'tanggal',
#         'svarat' : 'syarat',
#         ']' : '',
#         ':' : '',
#         'lanli' : 'lahir',
#         'alamnai' : 'alamat',
#         'alamnat' : 'alamat',
#         'lahlr' : "lahir"

#     }

#     raw_text_replaced = raw_text

#     for word_to_be_replaced, new_words in replacement_dict.items():
#         raw_text_replaced = raw_text_replaced.replace(word_to_be_replaced, new_words)

#     return raw_text_replaced

#   def refinement(self, raw_text):
#     raw_text = self.replace_word(raw_text)

#     nokartu_pattern = r"kartu\s+(\S+)\s+nama"
#     nik_pattern = r'nik\s+(S+)\s+faskes'

#     is_match = re.search(nokartu_pattern, raw_text)
#     is_match_2 = re.search(nik_pattern, raw_text)


#     fixed_word = ''
#     if is_match:
#       fixed_word = is_match.group(1).replace('o','0').replace('d','0').replace('I','1').replace('l','1')
#       raw_text = re.sub(nokartu_pattern, f'kartu {fixed_word} nama', raw_text)

#     fixed_word = ''
#     if is_match_2:
#       fixed_word_2 = is_match.group(1).replace('o','0').replace('d','0').replace('I','1').replace('l','1')
#       raw_text = re.sub(nik_pattern, f'nik {fixed_word_2} faskes', raw_text)

#     return raw_text
  

  def extract_information(self, raw_text):
    # raw_text = self.refinement(raw_text)
    print(raw_text)

    # Define regular expressions for each value you want to extract
    npwp_pattern = r'npwp\s+(.*?)\s+\w'
    name_pattern = r'npwp\s+(.*?)\s+(.+?)\s+nik'
    nik_pattern = r'nik\s+(\d+)\s+\w+'
    address_pattern = r'(\d+)\s+(.*?)\s+kpp'
    kpp_pattern = r'kpp\s+(.+?)\s+terdaftar'
    registered_pattern = r'terdaftar\s+(\d+\s\w+\s\d{4})'

    npwp_match = re.search(npwp_pattern, raw_text)
    name_match = re.search(name_pattern, raw_text)
    nik_match = re.search(nik_pattern, raw_text)
    address_match = re.search(address_pattern, raw_text)
    kpp_match = re.search(kpp_pattern, raw_text)
    registered_match = re.search(registered_pattern, raw_text)

    self.result.npwpId = npwp_match.group(1) if npwp_match else None
    self.result.name = name_match.group(2) if name_match else None
    self.result.nik = nik_match.group(1) if nik_match else None
    self.result.address = address_match.group(2) if address_match else None
    self.result.kpp = kpp_match.group(1) if kpp_match else None
    self.result.registeredDate = registered_match.group(1) if registered_match else None


  def master_process(self):
    raw_text =  self.text_detection(self.threshed_img)
    self.extract_information(raw_text)

  def convert_to_json(self):
    return json.dumps(self.result.__dict__, indent = 4)




