"""Extracts CatTaxi_v9_port.c3p into a folder, turning the zip's backslash names into folders (validator layout)."""
import os, shutil, sys, zipfile
src = sys.argv[1] if len(sys.argv) > 1 else "CatTaxi_v9_port.c3p"
dst = sys.argv[2] if len(sys.argv) > 2 else "check9"
shutil.rmtree(dst, ignore_errors=True)
with zipfile.ZipFile(src) as z:
    for info in z.infolist():
        name = info.filename.replace("\\", "/")
        out = os.path.join(dst, name)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with z.open(info) as fi, open(out, "wb") as fo:
            fo.write(fi.read())
print("extracted", len(z.infolist()), "entries to", dst)
