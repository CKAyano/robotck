import json
import os
import sys
from pathlib import Path

import jsonschema

from ..base import Robot
from ..base.dh_types import DHAngleType, DHType
from .conf.jsonschema import SCHEMA
from .exception import BlankValueError, DHValueError
from .msg_box import warning_msg_box

# dirname = os.path.dirname(__file__)
if getattr(sys, "frozen", False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)
application_path = application_path.replace(os.sep, "/")

CONFIG_PATH = f"{application_path}/conf"
DH_CONFIG_PATH = f"{CONFIG_PATH}/dh.json"
DH_STYLE_PATH = f"{CONFIG_PATH}/df_style.css"
ICON_PATH = f"{CONFIG_PATH}/ico/icon.png"
TMP_PATH = f"{application_path}/tmp"
print(application_path)

HTML_STRING = """
        <html>
        <head><title>HTML Pandas Dataframe with CSS</title></head>
        <link rel="stylesheet" type="text/css" href="css_file_path"/>
        <body>
            {table}
        </body>
        </html>.
        """
HTML_STRING = HTML_STRING.replace("css_file_path", f"file:///{DH_STYLE_PATH}")


def is_blank(element: str):
    if len(element) == 0:
        return True
    return False


def is_str_style(element: str):
    if is_blank(element):
        return False
    str_prefix = ['"', "'"]
    if element[0] in str_prefix and element[0] == element[-1]:
        return True
    return False


def is_float(element: str):
    if is_blank(element):
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


def error_handling_str(element: str, msg: str):
    if is_str_style(element):
        return element
    raise DHValueError(msg)


def error_handling_float(element: str, msg: str):
    if is_float(element):
        return float(element)
    raise DHValueError(msg)


def error_handling_blank(name: str, msg: str):
    if is_blank(name):
        raise BlankValueError(msg)


def highlight_str(val):
    color = (
        f'<p style="background-color:grey; color:white; font-weight: bold">"{val}"</p>'
        if isinstance(val, str)
        else str(val)
    )
    return color


def mkdir_if_folder_not_exist():
    Path(CONFIG_PATH).mkdir(parents=True, exist_ok=True)
    Path(TMP_PATH).mkdir(parents=True, exist_ok=True)
    Path(ICON_PATH).parent.mkdir(parents=True, exist_ok=True)


def is_validated_config(json_path):
    if not os.path.exists(json_path) or os.stat(json_path).st_size == 0:
        with open(json_path, "w") as file:
            file.write("[]")
            return True
    try:
        with open(json_path) as file:
            config = json.load(file)
    except json.decoder.JSONDecodeError:
        return False
    try:
        jsonschema.validate(instance=config, schema=SCHEMA)
        return True
    except jsonschema.ValidationError:
        return False


def check_validated_config(json_path):
    if not is_validated_config(json_path):
        warning_msg_box("設定檔格式有誤")
        sys.exit(0)


def get_robot_instance_from_robot_dict(robot_dict: dict) -> Robot:
    if robot_dict["is_std"]:
        dh_type = DHType.STANDARD
    else:
        dh_type = DHType.MODIFIED

    if robot_dict["is_rad"]:
        dh_angle = DHAngleType.RAD
    else:
        dh_angle = DHAngleType.DEG

    return Robot(robot_dict["dh"], robot_dict["robot_name"], dh_angle, dh_type, robot_dict["is_revol"])
