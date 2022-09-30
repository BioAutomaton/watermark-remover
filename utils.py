import io
import os
import zipfile

import cv2
import numpy as np
from fastapi import Response


def process_image(watermarked_image):
    """
    Apply simple thresholding to an image
    :param watermarked_image: cv2 image
    :return: processed cv2 image
    """
    _, unwatermarked_image = cv2.threshold(watermarked_image, 150, 255, cv2.THRESH_BINARY)  # process image
    return unwatermarked_image


def image_from_bytes(data):
    """
    Get cv2 image from bytes
    :param data: Image bytes. For example, from request data
    :return: cv2 image
    """
    encoded_image_numpy_array = np.frombuffer(data, np.uint8)
    decoded_image = cv2.imdecode(encoded_image_numpy_array, cv2.IMREAD_COLOR)
    return decoded_image


def zip_files(filenames: list):
    """
    Creates a zip file archive and returns it as a response
    :param filenames: List of files to be zipped
    :return: fastapi.Response object
    """
    zip_filename = "unwatermarked_images.zip"

    bytes_buffer = io.BytesIO()
    zipped_file = zipfile.ZipFile(bytes_buffer, "w")

    for filepath in filenames:
        # Calculate path for file in zip
        directory, filename = os.path.split(filepath)

        # Add file, at correct path
        zipped_file.write(filepath, filename)

    # Must close zip for all contents to be written
    zipped_file.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    response = Response(bytes_buffer.getvalue(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment;filename={zip_filename}'
    })

    return response
