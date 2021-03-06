#@title Imports and function definitions

# For running inference on the TF-Hub module.
import tensorflow as tf
import tensorflow_hub as hub
# For downloading the image.
import matplotlib.pyplot as plt
import tempfile
#from six.moves.urllib.request import urlopen
#from six import BytesIO

# For drawing onto the image.
import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

# For measuring the inference time.
import time


# ---------------------------------------------
def np_to_float(res):
    float_list=[]
    for i in res['score']:
        float_list.append(float(i))
    return float_list

def display_image(image):
    fig = plt.figure(figsize=(20, 15))
    plt.grid(False)
    plt.imshow(image)
    
def resize_image(img_path, img_suffix='jpeg', new_width=256, new_height=256, display=False):
    _, filename = tempfile.mkstemp(suffix=img_suffix)
    #response = urlopen(url)
    #image_data = response.read()
    
    #image_data = mpimg.imread(f'{img_path}.jpeg')
    #print(image_data)
    
    #image_data = BytesIO(image_data)
    pil_image = Image.open(f'{img_path}.{img_suffix}')
    pil_image = ImageOps.fit(pil_image, (new_width, new_height), Image.ANTIALIAS)
    pil_image_rgb = pil_image.convert("RGB")
    pil_image_rgb.save(filename, format="JPEG", quality=90)
    print("Image downloaded to %s." % filename)
    if display:
        display_image(pil_image)
    return filename

def draw_bounding_box_on_image(image,
                             ymin,
                             xmin,
                             ymax,
                             xmax,
                             color,
                             font,
                             thickness=4,
                             display_str_list=()):
    """Adds a bounding box to an image."""
    draw = ImageDraw.Draw(image)
    im_width, im_height = image.size
    (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                                                ymin * im_height, ymax * im_height)
    draw.line([(left, top), (left, bottom), (right, bottom), (right, top),
                         (left, top)],
                        width=thickness,
                        fill=color)

    # If the total height of the display strings added to the top of the bounding
    # box exceeds the top of the image, stack the strings below the bounding box
    # instead of above.
    display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
    # Each display_str has a top and bottom margin of 0.05x.
    total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

    if top > total_display_str_height:
        text_bottom = top
    else:
        text_bottom = top + total_display_str_height
    # Reverse list and print from bottom to top.
    for display_str in display_str_list[::-1]:
        text_width, text_height = font.getsize(display_str)
        margin = np.ceil(0.05 * text_height)
        draw.rectangle([(left, text_bottom - text_height - 2 * margin),
                                        (left + text_width, text_bottom)],
                                     fill=color)
        draw.text((left + margin, text_bottom - text_height - margin),
                            display_str,
                            fill="black",
                            font=font)
        text_bottom -= text_height - 2 * margin

def draw_boxes(image, boxes, class_names, scores, max_boxes=10, min_score=0.1, return_image=True):
    """Overlay labeled boxes on an image with formatted scores and label names."""
    
    if return_image:
        colors = list(ImageColor.colormap.values())

        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf", 25)
        except IOError:
            print("Font not found, using default font.")
            font = ImageFont.load_default()

    res_dict={'label': [], 'score': []}
    for i in range(min(boxes.shape[0], max_boxes)):
        if scores[i] >= min_score:
            
            res_dict['label'].append(class_names[i].decode('utf-8'))
            #res_dict['box'].append(boxes[i])
            res_dict['score'].append(scores[i])
            
            if return_image:
                ymin, xmin, ymax, xmax = tuple(boxes[i])
                display_str = "{}: {}%".format(class_names[i].decode("ascii"), int(100 * scores[i]))
                color = colors[hash(class_names[i]) % len(colors)]
                image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
                draw_bounding_box_on_image(
                        image_pil,
                        ymin,
                        xmin,
                        ymax,
                        xmax,
                        color,
                        font,
                        display_str_list=[display_str])
                np.copyto(image, np.array(image_pil))
    if return_image:
        return image, res_dict
    else:
        return res_dict

def load_img(path):
    img = tf.io.read_file(path)
    img = tf.image.decode_jpeg(img, channels=3)
    return img


def run_detector(detector, path, return_image=True):
    img = load_img(path)

    converted_img = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
    start_time = time.time()
    result = detector(converted_img)
    end_time = time.time()

    result = {key:value.numpy() for key,value in result.items()}

    print("Found %d objects." % len(result["detection_scores"]))
    print("Inference time: ", end_time-start_time)


    return draw_boxes(img.numpy(), result["detection_boxes"], result["detection_class_entities"], result["detection_scores"],
                       return_image=return_image)
    
def detect_img(img_path, img_suffix='jpeg'):
    image_path = resize_image(img_path, img_suffix='jpeg', new_width=640, new_height=480)
    res = run_detector(detector, image_path)
    end_time = time.time()
    
    return res

# --------------------------------

module_handle = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1" #@param ["https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1", "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"]
detector = hub.load(module_handle).signatures['default']
