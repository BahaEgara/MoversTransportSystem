import os
from datetime import datetime

import imghdr
from werkzeug.utils import secure_filename
from mimetypes import MimeTypes


ALLOWED_EXTENSIONS = ["jpg", "gif", "jpeg", "png"]


def validate_image(stream):
    """
    Reads the first 512 bytes from the input stream and attempts to determine
    the image format.

    :param stream: binary stream - The input stream representing the image.

    :return: str - A file extension based on the detected image format.
    """
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)

    if not format:
        return None

    return format


def is_allowed_file(image_file):
    """
    Check if the provided image file has an allowed extension or is a valid
    image.

    :param image_file: werkzeug.datastructures.FileStorage - FileStorage object
    representing the uploaded image.

    :return: bool - True if the image has an allowed extension or is a valid
    image, False otherwise.
    """
    filename = image_file.filename
    if "." in filename:
        extension = filename.rsplit(".", 1)[1].lower()
        # Check if the extension is allowed or image is valid
        if extension in ALLOWED_EXTENSIONS or extension == validate_image(
            image_file.stream
        ):
            return True

        return False

    return False


def save_image(image_file, folder=None):
    """
    Save the provided image file to the specified folder.

    :param image_file: werkzeug.datastructures.FileStorage - The image file
    to be saved.

    :param folder: str, optional - The folder where the image will be saved. If
    not provided, the image will not be saved.

    :return (filename | None): str, optional - The full path to the saved image
    if successful, None otherwise.
    """
    if image_file and folder:
        if not os.path.exists(folder):
            os.makedirs(folder)

        filename = secure_filename(image_file.filename)
        image_path = os.path.join(folder, filename)
        image_file.save(image_path)

        return filename

    return None


def save_file(file, folder=None):
    """
    Save the provided file to the specified folder.

    :param file: werkzeug.datastructures.FileStorage - The file to be saved.

    :param folder: str, optional - The folder where the file will be saved.
    If not provided, the file will not be saved.

    :return filename: str | None - The full path to the saved file if
    successful, None otherwise.
    """
    if file and folder:
        if not os.path.exists(folder):
            os.makedirs(folder)

        filename = secure_filename(file.filename)
        file_path = os.path.join(folder, filename)
        file.save(file_path)

        return file_path

    return None


def allowed_file(filename, allowed_extensions=set()):
    """
    Checks if a filename has an allowed file extension.

    :param filename: str - The name of the file to be checked.
    :param allowed_extensions: set - A set of allowed extensions.

    :return: bool - True if the filename has an allowed extension, False
    otherwise.
    """
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in allowed_extensions
    )
