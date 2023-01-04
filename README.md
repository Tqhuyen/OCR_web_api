Deploy
1. Cài đặt thư viện PaddlePaddle

Nếu máy có GPU
```bash
python3 -m pip install paddlepaddle-gpu -i https://mirror.baidu.com/pypi/simple
```

Nếu máy chỉ có CPU
```bash
python3 -m pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
```

2. Cài đặt thư viện PaddleOCR

```bash
pip install "paddleocr>=2.0.1" # Recommend to use version 2.0.1+
```

3. Cài đặt thư viện Flask
```bash
pip install flask
```

4. Tạo file có tên <.env> cùng đường dẫn với project với cấu trúc giống trong file .env.example

5. Run
```bash
python ocr_api.py
```
