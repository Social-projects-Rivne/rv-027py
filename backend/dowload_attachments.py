import os
import urllib2
import zipfile
from config import Config

url = 'https://drive.google.com/uc?export=download&id=1_nOsXlKJRIoRqasCEbypQpUkENAYbS_V'
zip_file_name = 'attachments.zip'
zip_file_path = os.path.realpath(zip_file_name)
directory_to_extract = Config.MEDIA_FOLDER
print zip_file_path


def download_attachments(url, zip_file_name):
    zip_file = urllib2.urlopen(url)
    with open(zip_file_name, 'wb') as output:
        output.write(zip_file.read())
    print 'File successfully downloaded'


def unzip_file(zip_file_path, directory_to_extract_to):
    zip_ref = zipfile.ZipFile(zip_file_path, 'r')
    zip_ref.extractall(directory_to_extract_to)
    zip_ref.close()
    os.remove(zip_file_path)
    print 'Files was extracted'


if __name__ == '__main__':
    download_attachments(url, zip_file_name)
    unzip_file(zip_file_path, directory_to_extract)
