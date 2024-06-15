import cv2
import re
import numpy as np
import json
import easyocr

class KTPInformation():
    def __init__(self):
        self.name = ''
        self.birthPlaceBirthday = ''
        self.address = ''
        self.religion = ''
        self.maritalStatus = ''
        self.occupation = ''
        self.bloodType = ''
        self.gender = ''
        self.district = ''
        self.rtrw = ''
        self.idNumber = ''
        self.village = ''
        self.nationality = ''
        self.province = ''
        self.expiryDate = 'seumur hidup'

class KTPOCR():
    def __init__(self, images, reader):
        # self.images = cv2.imread(images)
        top, right, channels = images.shape

        right = int(right * 0.75)

        self.cropped_img = images[0:top, 0:right]
        
        self.gray = cv2.cvtColor(self.cropped_img, cv2.COLOR_BGR2GRAY)
        self.thresh = cv2.threshold(self.gray, 167, 255, cv2.THRESH_TRUNC)[1]

        self.result = KTPInformation()
        
        self.reader = reader
        self.master_process()

    def text_detection(self, image):
        # reader = easyocr.Reader(['id'])
        list_ocr_result = self.reader.readtext(image, detail=0)
        raw_text = ' '.join(list_ocr_result).lower()

        return raw_text
    
    def replace_word(self, raw_text):
        replacement_dict = {
            'ı': 'i',
            'alamnal': 'alamat',
            'venis kelatruri': 'jenis kelamin',
            'kecamalan': 'kecamatan',
            'agamna': 'agama',
            ';': ':',
            'tempaltgl lahir': 'tempat/tgl lahir',
            ' ama ': ' nama ',
            'jens kelamin': 'jenis kelamin',
            ' aamar ': ' alamat ',
            'aqa': 'agama',
            'tempautgl lahir': 'tempat/tgl lahir',
            'stalus perkawinan': 'status perkawinan',
            'kecarnatan': 'kecamatan',
            'slatus perkawinan': 'status perkawinan',
            'rekefiaan': 'pekerjaan',
            'nona': 'nama',
            'tcmpavtgl lahir': 'tempat/tgl lahir',
            'negaraan': 'kewarganegaraan',
            'naia': 'nama',
            'narna': 'nama',
            ':': '',
            ';': '',
            ',': '',
            '.': '',
            'lempattgl lahir': 'tempat/tgl lahir',
            'empattgl lahir': 'tempat/tgl lahir',
            'nains' : 'nama',
            'empattgi lahir' : 'tempat/tgl lahir',
            'kgama' : 'agama',
            'kewargakewarganegaraan' : 'kewarganegaraan',
            '=' : '-',
            'namo' : 'nama',
            'ternpatftgl lahu' : 'tempat/tgl lahir',
            'ternpatftgl lahir' : 'tempat/tgl lahir',
            'ternpat/tgl lahir' : 'tempat/tgl lahir',
            'jenis kolamin' : 'jenis kelamin',
            'alamal' : 'alamat',
            'kelluesa' : 'keldesa',
            'beraku hingga' : 'berlaku hingga',
            'goldarah' : 'gol darah',
            'col darah' : 'gol darah',
            'coldarah' : 'gol darah',
            'jens kelanun' : 'jenis kelamin',
            'pekerhan' : 'pekerjaan',
            'kecauntan' : 'kecamatan',
            'keldcsa' : 'keldesa',
            'agamamna' : 'agama',
            'perawinan' : 'perkawinan',
            'tempatltgl lahir' : 'tempat/tgl lahir',
            'kcldcsa' : 'keldesa',
            'kcl dcsa' : 'keldesa',
            'tompaltgi lahir' : 'tempat/tgl lahir',
            'perkawvinan' : 'perkawinan',
            'tempal/tgl lahir' : 'tempat/tgl lahir',
            'ł' : 'l',
            'alamnat' : 'alamat',
            'perkawinar' : 'perkawinan',
            'fitrw' : 'rtrw',
            'tempattgl lahr' : 'tempat/tgl lahir',
            'jenis kclamin' : 'jenis kelamin',
            'tempat tql lahir' : 'tempat/tgl lahir',
            'penainan' : 'perkawinan',
            'perejan' : 'pekerjaan',
            'atrw' : 'rtrw',
            'gddarah' : 'gol darah',
            'ataw' : 'rtrw',
            'aona' : 'agama',
            'atw' : 'rtrw',
            'alarnat' : 'alamat',
            'fit/rw' : 'rtrw',
            'kew argakewarganegaraan' : 'kewarganegaraan',
            'empatelgl' : 'tempat/tgl lahir',
            'pelajarimahasiswa' : 'pelajar/mahasiswa',
            'kecaratan' : 'kecamatan',
            ' mik ' : ' nik ',
            'timua ' : 'timur '

        }

        raw_text_replaced = raw_text

        for word_to_be_replaced, new_words in replacement_dict.items():
            raw_text_replaced = raw_text_replaced.replace(word_to_be_replaced, new_words)

        return raw_text_replaced
    
    def refinement(self, raw_text):
        raw_text_replaced = self.replace_word(raw_text)
        # return raw_cleaned_text

        pattern = r'(rtrw|rt/rw|rirw|rtirw)\s+([\d\s/]+\??|[\w\s/]+)\s+k'
        pattern_2 = r'lahir\s+(\w+)\s+(.*?)\s+jenis'
        pattern_3 = r"nik\s+(\S+)\s+n"
        pattern_4 = r'gol\s+darah\s+(-|\w)'

        is_match = re.search(pattern, raw_text_replaced)
        is_match_2 = re.search(pattern_2, raw_text_replaced)
        is_match_3 = re.search(pattern_3, raw_text_replaced)
        is_match_4 = re.search(pattern_4, raw_text_replaced)

        fixed_word = ''
        if is_match:
            fixed_word = is_match.group(2).replace('o', '0').replace('i', '1').replace('?', '2').replace(' ','/')

        fixed_word_2 = ''
        if is_match_2:
            fixed_word_2 = is_match_2.group(2).replace('o', '0').replace('i', '1').replace(' ', '-').replace('e','8')

        fixed_word_3 = ''
        if is_match_3:
            fixed_word_3 = is_match_3.group(1).replace('o','0').replace('l','1').replace('i','1').replace('?','7').replace('s','5').replace('e','3')

        fixed_word_4 = ''
        if is_match_4:
            fixed_word_4 = is_match_4.group(1).replace('e','b').replace('c','o').replace('r','a')


        if is_match:
            raw_text_replaced = re.sub(pattern, f'rtrw {fixed_word} k', raw_text_replaced)

        if is_match_2:
            raw_text_replaced = re.sub(pattern_2,f'lahir {is_match_2.group(1)} {fixed_word_2} jenis', raw_text_replaced)

        if is_match_3:
            raw_text_replaced = re.sub(pattern_3, f'nik {fixed_word_3} n', raw_text_replaced)

        if is_match_4:
            raw_text_replaced = re.sub(pattern_4, f'gol darah {fixed_word_4}', raw_text_replaced)

        return raw_text_replaced

    def extract_information(self, raw_text):
        raw_cleaned_text = self.refinement(raw_text)
        print(raw_cleaned_text)
        # result = {}

        nama_pattern = r'nama\s+(.+?)\s+t'
        tempat_tgl_lahir_pattern =r'(tempat/tgl|tempattgl|tempatitgl|)\s+lahir\s+(\w+)\s+(\S+)\s+j'
        # tempat_tgl_lahir_pattern =r'(tempat/tgl|tempattgl|tempatitgl|tempat\s+tgl)\s+lahir\s+(\w+)\s+(\d{2}-\d{2}-\d{2,4})'
        alamat_pattern = r'(alamat|alamnat)\s+(.*)\s+(rt|ri)'
        agama_pattern = r"agama\s+([^\s]+)"
        status_kawin_pattern = r"perkawinan\s+(.*?)\s+p"
        pekerjaan_pattern = r'pekerjaan\s+(.+?)\s+kewarga'
        berlaku_hingga_pattern = r"berlaku\s+hingga\s+(\d{2}\s\d{2}\s\d{4})"
        golongan_darah_pattern = r'gol\s+darah\s+(-|\w)\s+\w+'
        jenis_kelamin_pattern = r"jenis\s+kelamin\s+([^\s]+)"
        kecamatan_pattern = r'kecamatan\s+(.*?)\s+agama'
        rtrw_pattern = r"(rtrw|rt/rw|rtirw|rirw)\s+(\d{3}\s\d{3}|\d{3}/\d{3})"
        nik_pattern = r"nik\s+(\d+)\s+\w+"
        kel_desa_pattern = r'(keldesa|kel/desa|kelldesa|kevdesa|kel desa)\s+(.*?)\s+kecamatan'
        kewarganegaraan_pattern = r"negaraan\s+(\w+)"
        provinsi_pattern = r'provinsi\s+(.*?)\s+(kota|jakarta timur|kabupaten|jakarta barat|jakarta pusat|jakarta utara|jakarta selatan)'

        # Extract information using regular expressions
        nama_match = re.search(nama_pattern, raw_cleaned_text)
        tempat_tgl_lahir_match = re.search(tempat_tgl_lahir_pattern, raw_cleaned_text)
        alamat_match = re.search(alamat_pattern, raw_cleaned_text)
        agama_match = re.search(agama_pattern, raw_cleaned_text)
        status_kawin_match = re.search(status_kawin_pattern, raw_cleaned_text)
        pekerjaan_match = re.search(pekerjaan_pattern, raw_cleaned_text)
        berlaku_hingga_match = re.search(berlaku_hingga_pattern, raw_cleaned_text)
        golongan_darah_match = re.search(golongan_darah_pattern, raw_cleaned_text)
        jenis_kelamin_match = re.search(jenis_kelamin_pattern, raw_cleaned_text)
        kecamatan_match = re.search(kecamatan_pattern, raw_cleaned_text)
        rtrw_match = re.search(rtrw_pattern, raw_cleaned_text)
        nik_match = re.search(nik_pattern, raw_cleaned_text)
        kel_desa_match = re.search(kel_desa_pattern, raw_cleaned_text)
        kewarganegaraan_match = re.search(kewarganegaraan_pattern, raw_cleaned_text)
        provinsi_match = re.search(provinsi_pattern, raw_cleaned_text)

        # Print extracted information
        if nama_match:
            self.result.name =  nama_match.group(1)

        if tempat_tgl_lahir_match:
            self.result.birthPlaceBirthday = f'{tempat_tgl_lahir_match.group(2)}, {tempat_tgl_lahir_match.group(3)}'
            # print(tempat_tgl_lahir_match.group(2))

        if alamat_match:
            self.result.address = alamat_match.group(2)

        if agama_match:
            self.result.religion =  agama_match.group(1)

        if status_kawin_match:
            self.result.maritalStatus = status_kawin_match.group(1)
            # print(status_kawin_match.group(1))
        try:
            if pekerjaan_match:
                self.result.occupation = pekerjaan_match.group(1)
        except:
            self.result.occupation = ''


        # if berlaku_hingga_match:
        #     result["Berlaku Hingga:"] = berlaku_hingga_match.group(1)

        if golongan_darah_match :
            try:
                if len(golongan_darah_match.group(1)) == 1:
                    self.result.bloodType = golongan_darah_match.group(1)
                else:
                    self.result.bloodType = '-'
            except:
                self.result.bloodType = '-'

            # print(golongan_darah_match.group(1))
        else:
            self.result.bloodType = '-'

        try:
            if 'laki' in raw_cleaned_text:
                self.result.gender = 'laki-laki'
            elif 'perempuan' in raw_cleaned_text:
                self.result.gender = 'perempuan'
        except:
                 self.result.gender= ''

        if kecamatan_match:
            self.result.district= kecamatan_match.group(1)

        if rtrw_match:
            self.result.rtrw= rtrw_match.group(2)

        if nik_match:
            self.result.idNumber= nik_match.group(1)

        if kel_desa_match:
            self.result.village = kel_desa_match.group(2)

        if kewarganegaraan_match:
            self.result.nationality= kewarganegaraan_match.group(1)

        if provinsi_match:
            self.result.province = provinsi_match.group(1)

        self.result.expiryDate = 'seumur hidup'

    def master_process(self):
        raw_text = self.text_detection(self.thresh)
        self.extract_information(raw_text)

    def convert_to_json(self):
        return json.dumps(self.result.__dict__, indent=4)

        