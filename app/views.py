import asyncio
import json

from django.views.decorators import gzip
import io
from pathlib import Path
from deepface import DeepFace
import base64
from PIL import Image
from .video_cam import *
from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse
from digital_on_boarding.utils.scanned_image import *


def home(request):
    return render(request, 'app/home.html')

def services(request):
    return render(request, 'app/services.html')

def team(request):
    return render(request, 'app/team.html')

def get(request):
    canvas_data_selfie = request.POST.get('imgTagHtml')
    canvas_data_doc = request.POST.get('docTagHtml')
    try:
        if canvas_data_selfie:
            canvas_data_selfie = str(canvas_data_selfie).split(',')[1]
            img = base64.b64decode(canvas_data_selfie)
            img_pil = Image.open(io.BytesIO(img))
            img_pil.save(r"app/static/app/selfie.png")
        if canvas_data_doc:
            canvas_data_selfie = str(canvas_data_doc).split(',')[1]
            img = base64.b64decode(canvas_data_selfie)
            img_pil = Image.open(io.BytesIO(img))
            img_pil.save(r"app/static/app/doc.png")
    except:
        print("Cannot Be Generated")
    return render(request, 'app/index.html')


async def calculate(request):
    req = request.GET
    if req is None:
        await asyncio.sleep(10),
        value = req.get('calculate')
    else:
        value = req.get('calculate')
    json_file = calc()

    return render(request, 'app/result.html', json_file)


@gzip.gzip_page
def video_stream(request):
    cam = VideoCamera()
    front_ = gen(cam)
    return StreamingHttpResponse(front_, content_type="multipart/x-mixed-replace;boundary=frame")


def transform_run(image_path: str, dst_dir) -> Dict:
    config_file_path = CONFIG_PATH
    img_name = Path(image_path).name
    info = dict()
    t_generator = ScannedImage(image_path, config_file_path)
    t_generator.fill_info(info)
    transformer = t_generator.get_best_transformer()
    if transformer is None:
        info["TRANSFORM_INFO"] = "N/A"
        info["PERSONAL_INFO"] = "N/A"
        print("Could not create transformer: document type is:", t_generator.doc_type)
    else:
        transformer.fill_info(info)
        document, portrait = transformer.get_transformed_image(image_path)
        # document.show()
        document.save(f'{dst_dir}/transformed_{img_name}')
        if portrait:
            portrait.save(f'{dst_dir}/portrait_{img_name}')

    dst_json = f"{img_name}_info.json"
    with open(Path(dst_dir) / Path(dst_json), 'w') as f:
        f.write(json.dumps(info, indent=4))
    return info


def verification():
    name1 = r"app\static\app\doc.png"
    name2 = r"app\static\app\selfie.png"
    result = DeepFace.verify(name1, name2)
    return result


def calc():

    img_path = r"app/static/app/doc.png"
    transformed_dict = transform_run(img_path, r"app/static/app")
    try:
        document_type = transformed_dict["DOCTYPE"]
    except:
        document_type = None
    try:
        id_num = transformed_dict["PERSONAL_INFO"]["ID_NUM"]
    except:
        id_num = None
    try:
        first_name = transformed_dict["PERSONAL_INFO"]["FIRST_NAME"]
    except:
        first_name = None
    try:
        last_name = transformed_dict["PERSONAL_INFO"]["LAST_NAME"]
    except:
        last_name = None
    try:
        verification_result = verification()["verified"]
    except:
        verification_result = None

    context = {
        "doc_type": document_type,
        "id_num": id_num,
        "first_name": first_name,
        "last_name": last_name,
        "verifiation": verification_result,
    }
    # json_file = json.dumps(context)
    # print(json_file)
    return context