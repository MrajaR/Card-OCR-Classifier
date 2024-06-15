from ktpocr import KTPOCR
from bpjsocr import BPJSOCR
from npwpocr import NPWPOCR
from app_2 import reader

def read_ocr_ktp(ktppath, reader):
    word = KTPOCR(ktppath,reader).convert_to_json()
    return word

def read_ocr_bpjs(bpjspath, reader):
    word = BPJSOCR(bpjspath, reader).convert_to_json()
    return word

def read_ocr_npwp(npwppath, reader):
    word = NPWPOCR(npwppath, reader).convert_to_json()
    return word