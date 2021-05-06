import subprocess
import base64


def latex2image(latex):
    subprocess.call(['tex2im','-r', '128x128',  '-o', 'static/tex2im', latex])
    with open('static/tex2im.png', 'rb') as f:
        image = f.read()
        image_base64 = str(base64.b64encode(image), encoding='utf-8')
        return image_base64


if __name__ == '__main__':
    latex = 'x^2 + y^2 = 1'
    print(latex2image(latex))
