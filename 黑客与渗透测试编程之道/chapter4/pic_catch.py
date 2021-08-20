#-*- coding:utf8 -*-
#尝试从HTTP流量中提取图像文件，然后利用OpenCV对提取出来的图像进行处理，对图像包含人脸的部分进行检测
#涉及:数据包的分割，对数据包进行特定类型的提取和处理
import re
import zlib
import cv2

from scapy.all import *

pictures_directory = "./pictures/"
faces_directory = "./faces/"
pcap_file = "test.pcap"

def get_http_headers(http_payload):
    """
    函数作用：
        get_http_headers函数处理原始的HTTP流，使用正则表达式对头部进行分割。
        extract_image函数解析HTTP头，检测HTTP响应中是否包含图像文件，如果我们检测到Content-Type
        字段中包含image的MIME类型，则对字段值进行分割，提取图像的类型，然后判断图像在传输过程中是否被
        压缩，如果被压缩，则我们在返回图像类型和图像原始数据之前尝试进行解压。
    """
    try:
        #如果为http流量，提取http头
        headers_raw = http_payload[:http_payload.index("\r\n\r\n")+2]

        #对http头进行切分
        headers = dict(re.findall(r"(?P<name>.*?):(?P<value>.*?)\r\n", headers_raw))

    except:
        return None

    if "Content-Type" not in headers:
        return None

    return headers

def extract_image(headers, http_payload):
    image = None
    image_type = None

    try:
        if "image" in headers['Content-Type']:
            #获取图像类型和图像数据
            image_type = headers['Content-Type'].split("/")[1]
            image = http_payload[http_payload.index("\r\n\r\n")+4:]
            #如果数据进行了压缩则解压
            try:
                if "Content-Encoding" in headers.keys():
                    if headers['Content-Encoding'] == "gzip":
                        image = zlib.decompress(image, 16+zlib.MAX_WBITS)
                    elif headers['Content-Encoding'] == "deflate":
                        image = zlib.decompress(image)
            except:
                pass
    except:
        return None, None

    return image,image_type

def face_detect(path, file_name):
    """
    疯狂调库，没啥好说的
    使用组件：OpenCV
    """
    img = cv2.imread(path)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))

    if len(rects) == 0:
        return False

    rects[:, 2:] += rects[:, :2]

    #对图像中的人脸进行高亮的显示处理
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1,y1), (x2,y2), (127,255,0), 2)

    cv2.imwrite("%s／%s-%s" (faces_directory, pcap_file, file_name), img)
    return True

def http_assembler(pcap_file):#处理PCAP文件，将PCAP文件依据是否含有HTTP进行分割，以便后续处理

    carved_images = 0
    faces_detected = 0

    a = rdpcap(pcap_file)#打开需要处理的PCAP文件

    sessions = a.sessions()

    for session in sessions:#利用Scapy的高级特性自动地对TCP中的会话进行分割并保存到一个字典里
        http_payload = ""
        for packet in sessions[session]:
            try:#过滤所有非HTTP的其他流量，然后将HTTP会话的负载内容拼接到一个单独的缓冲区中
                if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                    # 对数据组包
                    http_payload += str(packet[TCP].payload)
            except:
                pass

        headers = get_http_headers(http_payload)#完成HTTP数据的组装后，将缓冲区中的内容作为参数调用
                                                #我们编写的HTTP头分割函数

        if headers is None:
            continue
        image, image_type = extract_image(headers, http_payload)
        #头分割函数：允许我们单独处理HTTP头中的内容.
        #当我们确认在HTTP的响应数据中包含图像内容时，我们提取图像的原始数据
        if image is not None and image_type is not None:
            """
            返回图像类型和图像的二进制流，这种图像的提取方式并不常规,但效果好，将提取的图像保存成文件
            """


            #　存储图像
            file_name = "%s-pic_carver_%d.%s" % (pcap_file, carved_images, image_type)
            fd = open("%s/%s" % (pictures_directory, file_name), "wb")

            fd.write(image)
            fd.close()

            carved_images += 1

            #开始人脸识别
            try:#调用人脸识别函数
                result = face_detect("%s/%s" % (pictures_directory, file_name), file_name)
                if result is True:
                    faces_detected += 1
            except:
                pass

    return carved_images, faces_detected

carved_images, faces_detected = http_assembler(pcap_file)

print("Extracted: %d images" % carved_images)
print ("Detected: %d faces" % faces_detected)