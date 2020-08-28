import hashlib
import base64
import argparse
import xml.etree.ElementTree as ElementTree


def sha256(filepath):
    with open(filepath, "rb") as file:
        digest = hashlib.sha256()
        while chunk := file.read(8192):
            digest.update(chunk)
    return digest.hexdigest()


parser_description = "Checks if submission report dependant documents exists and matches the supplied digest"
parser = argparse.ArgumentParser(description=parser_description)
parser.add_argument("-r", "--report", help="submission report file location (ends with .xml)")
parser.add_argument("-c", "--content", help="content folder location (contains all the files for this offer)")
args = parser.parse_args()

namespaces = {'sr': 'https://eten.publicprocurement.be/sr'}
tree = ElementTree.parse(args.report)
documents = tree.findall('sr:tender/sr:documents/sr:document', namespaces=namespaces)
for document in documents:
    filename = document.findtext('sr:details/sr:filename', namespaces=namespaces)
    expected_digest = base64.b64decode(document.findtext('sr:details/sr:digest/sr:dgValue', namespaces=namespaces)).hex()
    try:
        actual_digest = sha256(args.content + "/" + filename)
    except FileNotFoundError as error:
        actual_digest = "[FILE NOT FOUND]"
    print(f'[{expected_digest == actual_digest}] {filename} : {expected_digest} vs {actual_digest}')
print("check completed")




