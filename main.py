from PIL import Image
import os


def display_image(image: Image.Image):
    image.show()


def encrypt_image(image_path: str, key_path: str) -> Image.Image:
    image = Image.open(image_path)
    key = open(key_path, 'r').read().encode()
    image = image.convert(mode='1', colors=2)
    blocks = divide_images_into_blocks(image)

    # now encrypt every block with a key
    encrypted_blocks = encrypt_blocks(blocks, key)
    encrypted_image = join_block(encrypted_blocks)
    return encrypted_image


def xor_bytes(bytes1, bytes2):
    result = bytearray()
    for b1, b2 in zip(bytes1, bytes2):
        result.append(b1 ^ b2)
    return result


def divide_images_into_blocks(image: Image) -> list[Image.Image]:
    blocks = []
    for y in range(0, image.height, 8):
        for x in range(0, image.width, 8):
            block = image.crop((x, y, x+8, y+8))
            blocks.append(block)
    return blocks


def join_block(blocks: list[Image.Image]) -> Image.Image:
    encrypted_image = Image.new(mode='1', size=(256, 256))
    i_block = 0
    for y in range(0, encrypted_image.height, 8):
        for x in range(0, encrypted_image.width, 8):
            encrypted_image.paste(blocks[i_block], (x, y))
            i_block += 1
    return encrypted_image


def encrypt_blocks(blocks: list[Image.Image], key: bytes) -> list[Image.Image]:
    blocks_bytes = [block.tobytes() for block in blocks]
    encrypted_blocks = []
    for block_bytes in blocks_bytes:
        encrypted_blocks.append(Image.frombytes(mode="1", data=bytes(
            xor_bytes(block_bytes, key)), size=(8, 8)))
    return encrypted_blocks

    # Provide the path to your BMP image
bmp_file_path = f"{os.getcwd()}/plain.bmp"
key_file_path = f"{os.getcwd()}/key.txt"
display_image(encrypt_image(bmp_file_path, key_file_path))
