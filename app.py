from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Загружаем предобученный классификатор для лиц (каскад Хаара)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


# Функция для захвата и обработки видеопотока
def gen_frames():
    cap = cv2.VideoCapture(0)  # Захватываем видео с веб-камеры
    while True:
        success, frame = cap.read()  # Считываем кадр
        if not success:
            break

        # Преобразуем изображение в оттенки серого
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Обнаруживаем лица
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Рисуем прямоугольники вокруг лиц
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Кодируем изображение в формат JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Возвращаем кадры в формате, который можно транслировать в браузер
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index1.html')


@app.route('/video_feed')
def video_feed():
    # Трансляция видео на веб-страницу
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

