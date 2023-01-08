import argparse
import os
import sys


def start_stegano(in_file: str, out_file: str, hide: bool, message: bytes = None):
    from libStegano import SteganoReader
    from libStegano import SteganoWriter

    if hide:
        stegano_writer = SteganoWriter(in_file, out_file)
        stegano_writer.place_secret_message(message)
    else:
        stegano_reader = SteganoReader(in_file, out_file)
        stegano_reader.extract_secret_message()
        sys.stdout.write(stegano_reader.get_extracted_message() + '\n')


def main():
    parser = argparse.ArgumentParser()
    stegano_group = parser.add_mutually_exclusive_group(required=True)
    stegano_group.add_argument('-w', metavar='MESSAGE', type=str, help='Provide a message to hide')
    stegano_group.add_argument('-r', action='store_true', help='Read a hidden message from image')
    parser.add_argument('in_img', metavar='ORIGIN', type=str, help='Original image')
    parser.add_argument('out_img', metavar='STEGANO', type=str, help='Stegano image')
    args = parser.parse_args()

    if not os.path.exists(args.in_img):
        raise FileExistsError('File does not exist')
    if args.w:
        start_stegano(args.in_img, args.out_img, bool(args.w), args.w.encode('utf-8'))
    else:
        start_stegano(args.in_img, args.out_img, bool(args.w))


if __name__ == "__main__":
    main()
