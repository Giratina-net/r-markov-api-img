import io
import flask
import json
from PIL import Image, ImageDraw, ImageFont
from waitress import serve

app = flask.Flask(__name__)

font_path = "./assets/ZenMaruGothic-Medium.ttf"
fontsize = 368

@app.route('/', methods=['GET'])
def index():
    return ""

@app.route('/v1/raikaimg', methods=['GET'])
def raikaimg():
    text = flask.request.args.get('text')
    if text is None:
        return flask.Response(json.dumps({'error': 'text is required'}), status=400)
    text = '\n'.join(text[:35][i:i+7] for i in range(0, len(text[:35]), 7))
    try:
        img = Image.open('./assets/base.webp')
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype(font_path, fontsize)

        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        width, height = img.size
        text_x = (width - text_width) / 4 * 3
        text_y = (height - text_height) / 3 * 1

        draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='webp', optimize=True, quality=50)
        img_byte_arr = img_byte_arr.getvalue()
        response = flask.make_response(img_byte_arr)
        response.headers['Content-Type'] = 'image/webp'
        return response

    except Exception as e:
        return flask.Response(f'Error: {str(e)}', status=500)

if __name__ == '__main__':
    serve(app, port=80) 