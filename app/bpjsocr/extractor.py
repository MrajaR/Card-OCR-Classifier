import easyocr
import cv2
import numpy as np
import re
import json

class BPJSInformation():
  def __init__(self):
    self.idCard = ''
    self.name = ''
    self.address = ''
    self.birthDate = ''
    self.nik = ''
    self.faskes = ''

class BPJSOCR():
  def __init__(self, image, reader):
    # self.images = cv2.imread(image)
    height, width, channel = image.shape

    # Calculate the new heights for cropping
    bottom_crop_height = int(0.8* height)  # 75% for the bottom
    upper_crop_height = int(0.4 * height)   # 40% for the upper

    # Crop the bottom 25% of the image
    self.bottom_cropped_img = image[:bottom_crop_height, :]

    # Crop the upper 40% of the remaining image (after the bottom crop)
    self.cropped_img = self.bottom_cropped_img[upper_crop_height:, :]

    self.gray_img = cv2.cvtColor(self.cropped_img, cv2.COLOR_BGR2GRAY)
    self.threshed_img = cv2.threshold(self.gray_img, 120, 255, cv2.THRESH_TRUNC)[1]
    self.wo_noise_img = self.noise_removal(self.threshed_img)

    self.result = BPJSInformation()
    self.reader = reader
    self.master_process()


  def text_detection(self, image):
    list_ocr_result = self.reader.readtext(image, detail=0)
    raw_text = ' '.join(list_ocr_result).lower()

    return raw_text

  def replace_word(self, raw_text):
    replacement_dict = {
        '|' : '',
        'namz' : 'nama',
        'namo' : 'nama',
        'alamal' : 'alamat',
        'alamai' : 'alamat',
        'narna' : 'nama',
        'langgal' : 'tanggal',
        'svarat' : 'syarat',
        ']' : '',
        ':' : '',
        'lanli' : 'lahir',
        'alamnai' : 'alamat',
        'alamnat' : 'alamat',
        'lahlr' : "lahir"

    }

    raw_text_replaced = raw_text

    for word_to_be_replaced, new_words in replacement_dict.items():
        raw_text_replaced = raw_text_replaced.replace(word_to_be_replaced, new_words)

    return raw_text_replaced

  def refinement(self, raw_text):
    raw_text = self.replace_word(raw_text)

    nokartu_pattern = r"kartu\s+(\S+)\s+nama"
    nik_pattern = r'nik\s+(S+)\s+faskes'

    is_match = re.search(nokartu_pattern, raw_text)
    is_match_2 = re.search(nik_pattern, raw_text)


    fixed_word = ''
    if is_match:
      fixed_word = is_match.group(1).replace('o','0').replace('d','0').replace('I','1').replace('l','1')
      raw_text = re.sub(nokartu_pattern, f'kartu {fixed_word} nama', raw_text)

    fixed_word = ''
    if is_match_2:
      fixed_word_2 = is_match.group(1).replace('o','0').replace('d','0').replace('I','1').replace('l','1')
      raw_text = re.sub(nik_pattern, f'nik {fixed_word_2} faskes', raw_text)

    return raw_text
  
  def noise_removal(self, image):
        kernel = np.ones((2,2), np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        kernel = np.ones((2,2), np.uint8)
        image = cv2.erode(image, kernel, iterations=1)
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        image = cv2.medianBlur(image, 3)
        return image

  def extract_information(self, raw_text):
    raw_text = self.refinement(raw_text)
    print(raw_text)

    # Define regular expressions for each value you want to extract
    # nomor_kartu_pattern = r"kartu\s+(\d+)\s+\w+"
    # nama_pattern = r'nama\s+(.+?)\s+alamat'
    # alamat_pattern = r'alamat\s+(.*)\s+tanggal'
    # tanggal_lahir_pattern = r'tanggal\s+lahir\s+(\d+\s\w+\s\d{4})'
    # nik_pattern = r"nik\s+(\d+)\s+\w+"
    # faskes_pattern = r'faskes tingkat\s+([A-Za-z\s]+)'

    nomor_kartu_pattern = r"kartu\s+(\d+)\s+\w+"
    nama_pattern = r'nama\s+(.+?)\s+alamat'
    alamat_pattern = r'alamat\s+(.*)\s+tanggal'
    tanggal_lahir_pattern = r'tanggal\s+lahir\s+(\d+\s\w+\s\d{4})\s+n'
    nik_pattern = r"nik\s+(\d+)\s+\w+"
    faskes_pattern = r'faskes tingkat\s+([A-Za-z\s]+)\s+syarat'

    # Use re.search to find the first match of each pattern in the text
    nomor_kartu_match = re.search(nomor_kartu_pattern, raw_text)
    nama_match = re.search(nama_pattern, raw_text)
    alamat_match = re.search(alamat_pattern, raw_text)
    tanggal_lahir_match = re.search(tanggal_lahir_pattern, raw_text)
    nik_match = re.search(nik_pattern, raw_text)
    faskes_match = re.search(faskes_pattern, raw_text)

    # Extract values if matches are found
    self.result.idCard = nomor_kartu_match.group(1) if nomor_kartu_match else None
    self.result.name = nama_match.group(1) if nama_match else None
    self.result.address = alamat_match.group(1) if alamat_match else None
    self.result.birthDate = tanggal_lahir_match.group(1) if tanggal_lahir_match else None
    self.result.nik = nik_match.group(1) if nik_match else None
    self.result.faskes = faskes_match.group(1) if faskes_match else None


  def master_process(self):
    raw_text =  self.text_detection(self.wo_noise_img)
    self.extract_information(raw_text)

  def convert_to_json(self):
    return json.dumps(self.result.__dict__, indent = 4)




