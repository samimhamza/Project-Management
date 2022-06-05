from django.core.files.base import ContentFile
import base64
import uuid


def convertBase64ToImage(base64file):
    if(base64file and base64file != ""):

        format, imgstr = base64file.split(';base64,')
        ext = format.split('/')[-1]
        name = str(uuid.uuid4())+'.' + ext
        imageField = ContentFile(base64.b64decode(
            imgstr), name)
        return imageField
    return ''
