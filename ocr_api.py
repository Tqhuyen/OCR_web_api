from flask import Flask, request, jsonify, send_file
from PIL import Image
import io
from base64 import encodebytes
import subprocess
from paddleocr import PaddleOCR, draw_ocr
import calendar
import time
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

domain = os.environ['DOMAIN']
def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img

def read_text_file(file_dir: str)->list:
  '''
  input:
  file_dir: đường dẫn của file
  output:
  result: list các điểm đọc được từ đường dẫn của file
  '''
  result = []
  file_data = open(file_dir,'r')
  temp = file_data.read().splitlines()
  for box in temp:
    string_box = box.split(",")
    int_box = []
    for point in string_box:
      int_box.append(int(point))
    result.append(int_box)
  return result

def predict(img_path,name, use_gpu=True):
  ocr = PaddleOCR(use_gpu=use_gpu , use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
  # img_path = './test_data/test_data2.png'
  result_ocr = ocr.ocr(img_path, cls=True)
  # for idx in range(len(result_ocr)):
  #   res = result_ocr[idx]
  #   for line in res:
  #       print(line)
  # draw result
  feature = result_ocr[0]
  image = Image.open(img_path).convert('RGB')
  boxes = [line[0] for line in feature]
  txts = [line[1][0] for line in feature]
  scores = [line[1][1] for line in feature]
  im_show = draw_ocr(image, boxes, txts, scores, font_path='E:\\Hekate\\OCR_Project\\web_api\\fonts\\simfang.ttf')
  im_show = Image.fromarray(im_show)
  image_result_path = f'./static/result_{name}.jpg'
  im_show.save(image_result_path)
  return im_show, txts

@app.route("/predict", methods=["POST"])
def process_image():
    current_GMT = time.gmtime()

    time_stamp = calendar.timegm(current_GMT)
    file = request.files['image']
    img_path = f'./static/im_received_{time_stamp}.jpg'
    file.save(img_path)
    gpu_use = request.values['gpu_use']

    # Read the image via file.stream
    # img = Image.open(file.stream)
    image, message = predict(img_path=img_path,name=time_stamp, use_gpu=bool(gpu_use))
    image_result_path = f'result_{time_stamp}.jpg' # point to your image location
    image_url = domain +'/static/' + image_result_path
    encoded_img = get_response_image('./static/' + image_result_path)
    my_message = message # create your message as per your need


    response =  { 'Status' : 'Success', 'Text': my_message , 'ImageURL': image_url}
    return jsonify(response) # send the result to client


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=2224)