from PIL import Image
from datetime import datetime

# unique sequence is what our encoding ends in, so it can be recognised by the decoder
# it cannot be any sequence,
unique_sequence = "0000011100000111"


## @brief function used to see if message can be hidden in the image
#  @param img - the image 
#  @return - maximum number of bits that the message can have
def get_max_number_of_alterable_channels(img):
    return img.width * img.height * 3


## @brief function used to transform the message into a stream of bits
#  @param message - the message
#  @return - binarized message
def serialize_message(message):
    global unique_sequence
    temporary_byte = 0
    payload = str("")

    for byte in message:
        # [2:] because bin introduces '0b' as the first 2 bits of th converted string
        # example: 0b01010110 -> [2:] results in 01010110
        temporary_byte = bin(ord(byte))[2:]
        temporary_byte = '%08d' % int(temporary_byte)
        payload += temporary_byte

    payload += unique_sequence

    return payload


## @brief function used to transform an int into bits
#  @param integer - the integer that we want to binarize
#  @return - binarized integer
def serialize_8bit_int(integer):
    return '%08d' % int(str(bin(integer)[2:]))


## @brief function used to encode the message into an image
#  @param message - given message to hide in image
#  @param img - the image in which we want to hide the message
def encode(message, img, save_path, nr_bits: int):
    # 3.3.2 in documentation
    payload = serialize_message(message)

    # 3.3.3 in documentation
    if len(payload) > int(get_max_number_of_alterable_channels(img) * nr_bits):
        raise Exception("Message can't fit in image.")
    else:
        message_index = 0

        start_time = datetime.now()

        for i in range(img.height):
            for j in range(img.width):
                pixel = img.getpixel((j, i))

                r = serialize_8bit_int(pixel[0])
                g = serialize_8bit_int(pixel[1])
                b = serialize_8bit_int(pixel[2])

                # 3.3.4 in documentation
                if message_index < len(payload):
                    new_r = int(r[:(8 - nr_bits)] + payload[message_index:message_index + nr_bits], 2)
                    message_index += nr_bits
                if message_index < len(payload):
                    new_g = int(g[:(8 - nr_bits)] + payload[message_index:message_index + nr_bits], 2)
                    message_index += nr_bits
                if message_index < len(payload):
                    new_b = int(b[:(8 - nr_bits)] + payload[message_index:message_index + nr_bits], 2)
                    message_index += nr_bits

                img.putpixel((j, i), (new_r, new_g, new_b))

                if message_index == len(payload):
                    break
            if message_index == len(payload):
                break

        end_time = datetime.now()
        print('Duration: {}'.format(end_time - start_time))

        # we save in .png because PIL jpg compression messes the pixels we've modified
        img.save(save_path + "/not_a_suspicious_image.png", format='PNG')


## @brief function used to decode the message from an image
#  @param img - the image from which we want to decode the message
#  @return the decoded message in a string from 
def decode(img, nr_bits: int):
    decoded_payload = ""
    decoded_message = ""
    temp_char = ""

    for i in range(img.height):
        for j in range(img.width):
            pixel = img.getpixel((j, i))

            r = serialize_8bit_int(pixel[0])
            g = serialize_8bit_int(pixel[1])
            b = serialize_8bit_int(pixel[2])

            decoded_payload += r[(8 - nr_bits):]
            if decoded_payload[-len(unique_sequence):] == unique_sequence and len(decoded_payload) % 8 == 0:
                break
            decoded_payload += g[(8 - nr_bits):]
            if decoded_payload[-len(unique_sequence):] == unique_sequence and len(decoded_payload) % 8 == 0:
                break
            decoded_payload += b[(8 - nr_bits):]
            if decoded_payload[-len(unique_sequence):] == unique_sequence and len(decoded_payload) % 8 == 0:
                break

        if decoded_payload[-len(unique_sequence):] == unique_sequence and len(decoded_payload) % 8 == 0:
            decoded_payload = decoded_payload[:-len(unique_sequence)]
            break

    for bit in decoded_payload:
        temp_char += bit
        if len(temp_char) % 8 == 0:
            decoded_message += chr(int(temp_char, 2))
            temp_char = ""

    return decoded_message
