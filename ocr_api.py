from flask import Flask, request, jsonify, send_file
from PIL import Image
import io
from base64 import encodebytes
import subprocess
from paddleocr import PaddleOCR, draw_ocr

app = Flask(__name__)

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

def predict(img_path, use_gpu=True):
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
  im_show = draw_ocr(image, boxes, txts, scores, font_path='E:\Hekate\OCR_Project\web_api\simfang.ttf')
  im_show = Image.fromarray(im_show)
  im_show.save('result.jpg')
  return im_show, txts

@app.route("/predict", methods=["POST"])
def process_image():
    file = request.files['image']
    file.save('im-received.jpg')
    gpu_use = request.values['gpu_use']

    # Read the image via file.stream
    # img = Image.open(file.stream)
    image, message = predict(img_path='im-received.jpg', use_gpu=bool(gpu_use))
    image_path = '.\\result.jpg' # point to your image location
    encoded_img = get_response_image(image_path)
    my_message = message # create your message as per your need


    response =  { 'Status' : 'Success', 'Text': my_message , 'ImageBytes': encoded_img}
    return jsonify(response) # send the result to client


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')