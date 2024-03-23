import argparse
import subprocess
import magic
import os

def detect_compression_algorithm(file_path):
    # Use magic library to determine file type
    file_type = magic.from_file(file_path)

    # Check for specific file types
    if 'gzip' in file_type:
        return 'gzip'
    elif 'XZ compressed data' in file_type:
        return 'xz'
    elif 'LZ4 compressed data' in file_type:
        return 'lz4'
    elif 'LZO compressed data' in file_type:
        return 'lzop'
    elif 'lzma compressed data' in file_type:
        return 'lzma'
    else:
        return None

def extract_ramdisk(compressed_file):
    compression_algorithm = detect_compression_algorithm(compressed_file)
    if compression_algorithm is None:
        print(f"Unsupported compression algorithm for file: {compressed_file}")
        return

    print(f"Compression algorithm: {compression_algorithm} for file: {compressed_file}")

    # Run decompression command and pipe output to cpio for extraction
    if compression_algorithm == 'gzip':
        decompression_cmd = ['gzip', '-d', '-c', compressed_file]
    elif compression_algorithm == 'xz':
        decompression_cmd = ['xz', '-d', '-c', compressed_file]
    elif compression_algorithm == 'lz4':
        decompression_cmd = ['lz4', '-d', '-c', compressed_file]
    elif compression_algorithm == 'lzop':
        decompression_cmd = ['lzop', '-d', '-c', compressed_file]
    elif compression_algorithm == 'lzma':
        decompression_cmd = ['lzma', '-d', '-c', compressed_file]
    else:
        print(f"Unsupported compression algorithm for file: {compressed_file}")
        return

    cpio_cmd = ['cpio', '-i', '-d', '-m', '--no-absolute-filenames']

    ramdisk_directory = os.path.join(os.getcwd(), 'ramdisk')
    if not os.path.exists(ramdisk_directory):
        os.makedirs(ramdisk_directory)

    with open(os.path.join(ramdisk_directory, 'ramdisk'), 'wb') as ramdisk_file:
        decompression_process = subprocess.Popen(decompression_cmd, stdout=subprocess.PIPE)
        cpio_process = subprocess.Popen(cpio_cmd, stdin=decompression_process.stdout, cwd=ramdisk_directory)
        decompression_process.stdout.close()  # Allow decompression process to receive a SIGPIPE if cpio exits
        cpio_process.communicate()  # Wait for cpio process to finish

def extract_ramdisk_from_directory(directory):
    for root, _, files in os.walk(directory):
        for file_name in files:
            if 'ramdisk' in file_name:
                file_path = os.path.join(root, file_name)
                extract_ramdisk(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract ramdisk from compressed ramdisk (need to contain 'ramdisk' in the filename) to an output directory",
                                     epilog="Ramdisks will be extracted to a folder named 'ramdisk' within the current directory.")
    parser.add_argument("directory", nargs="?", help="Path to the directory containing compressed files (default: current directory)", default=".")
    args = parser.parse_args()

    extract_ramdisk_from_directory(args.directory)
    print(f"Ramdisks extracted from files containing 'ramdisk' in their names in: {os.getcwd()}/ramdisk")
