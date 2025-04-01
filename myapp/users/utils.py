import os
import secrets
from PIL import Image
from flask_login import current_user
from flask import current_app
from wtforms.validators import ValidationError



def save_picture(form_picture):
    # print(form_picture)     # <FileStorage: 'wallll.jpeg' ('image/jpeg')>
    # print(type(form_picture))   # <class 'werkzeug.datastructures.FileStorage'>
    # print(form_picture.filename)    # wallll.jpeg

    random_hex = secrets.token_hex(nbytes=8)
    _, f_ext = os.path.splitext(form_picture.filename)  # splits pathname into a pair (root, extension) ex: desktop/file.py --> (desktop/file, .py)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    previous_img_path = os.path.join(current_app.root_path, 'static/profile_pics', current_user.image_file)

    if current_user.image_file != 'default.jpg' and os.path.isfile(previous_img_path):    # delete users old pic if exist
        os.remove(previous_img_path)

    # form_picture.save(picture_path)

    output_size = (160, 160)    # if you don't want large image then resize them
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def no_leading_trailing_spaces(form, field):    # (form, field) automatically passed by WTForms
    if field.data != field.data.strip():
        raise ValidationError("Field cannot have leading or trailing spaces.")

    if field.name == "password" and " " in field.data:
        raise ValidationError("Password cannot contain spaces.")

