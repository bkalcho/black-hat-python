#!/usr/bin/python
__author__ = 'kalcho'

import re
import zlib
import cv2

from scapy.all import *

pictures_directory = "/home/kalcho/pic_carver/pictures"
faces_directory = "/home/kalcho/pic_carver/faces"
pcap_file = "bhp.pcap"

def get_http_headers(http_payload):
    
    try:
        # split the headers off if it is HTTP traffic
        headers_raw = http_payload[:http_payload.index("\r\n\r\n")+2]

        # break out the headers
        headers = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n",
            headers_raw))
    
    except:
        return None
    
    if "Content-Type" not in headers:
        return None
    
    return headers


def extract_image(headers, http_payload):

    image = None
    image_type = None

    try:
        if "image" in headers["Content-Type"]:

            # grab the image type and image body
            image_type = headers["Content-Type"].split("/")[1]

            image = http_payload[http_payload.index("\r\n\r\n")+4:]

            # if we detect compression decompress the image
            try:
                if "Content-Encoding" in header.keys():
                    if headers['Content-Encoding'] == "gzip":
                        image = zlib.decompress(image, 16+zlib.MAX_WBITS)
                    elif headers['Content-Encoding'] == "deflate":
                        image = zlib.decompress(image)

            except:
                pass
    except:
        return None, None
    
    return image, image_type


def http_assembler(pcap_file):

    carved_images = 0
    faces_detected = 0

    a = rdpcap(pcap_file)

    sessions = a.sessions()

    for session in sessions:
        http_payload = ""
        for packet in sessions[session]:
            try:
                if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                    # reasssemble the stream
                    http_payload += str(packet[TCP].payload)
            
            except:
                pass
        
        headers = get_http_headers(http_payload)

        if headers is None:
            continue

        image, image_type = extract_image(headers, http_payload)

        if image is not None and image_type is not None:
            # store the image
            file_name = "%s-pic_carver_%d.%s" % (pcap_file, carved_images,
                image_type)
            fd = open("%s/%s" % (pictures_directory, file_name), "wb")
            fd.write(image)
            fd.close()

            carved_images += 1

            # now attempt face detection
            try:
                result = face_detect("%s/%s" % (pictures_directory, file_name),
                    file_name)
                if result is True:
                    faces_detected += 1
            except:
                pass
    
    return carved_images, faces_detected


carved_images, faces_detected = http_assembler(pcap_file)

print "Extracted: %d images" % carved_images
print "Detected: %d faces" % faces_detected
