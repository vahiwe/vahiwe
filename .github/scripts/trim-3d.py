"""Trim the 3D contribution calendar.

Removes the language donut (it only sees public repos, so it shows almost
everything as "other") and the star/fork counts (they disagree with the
stats card). Keeps the calendar, the activity radar and the contribution total.
"""
import sys
import xml.etree.ElementTree as ET

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
path = sys.argv[1]
tree = ET.parse(path)
root = tree.getroot()


def texts(el):
    return [t.text.strip() for t in el.iter() if t.text and t.text.strip()]


for child in list(root):
    if child.tag == f"{{{NS}}}g" and "other" in texts(child):
        root.remove(child)  # language donut
    elif child.tag == f"{{{NS}}}g" and "contributions" in texts(child):
        keep = True
        for el in list(child):
            label = (el.text or "").strip()
            if label == "contributions":
                keep = False  # everything after the total, up to the date range
                continue
            if not keep and not ("/" in label and "-" in label):
                child.remove(el)

tree.write(path, encoding="unicode", xml_declaration=False)
