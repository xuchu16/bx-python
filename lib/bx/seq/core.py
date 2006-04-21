"""
Support for "biological sequence" files
---------------------------------------

:Author: Bob Harris (rsharris@bx.psu.edu)
:Version: $Revision: $

See seq.py for more information
"""

import struct
import fasta, nib, qdna

def seq_file (file, format=None, revcomp=False, name="", gap=None):
    if   (format == None):    format = infer_format(file)
    if   (format == "fasta"): return fasta.FastaFile (file, revcomp=revcomp, name=name, gap=gap)
    elif (format == "nib"):   return nib.NibFile     (file, revcomp=revcomp, name=name, gap=gap)
    elif (format == "qdna"):  return qdna.QdnaFile   (file, revcomp=revcomp, name=name, gap=gap)
    else:
        if (format == None): format = ""
        else:                format = " " + format
        raise "Unknown sequence format%s in %s" % (format,file.name)


def seq_reader (file, format=None, revcomp=False, name="", gap=None):
    if   (format == None):    format = infer_format(file)
    if   (format == "fasta"): return fasta.FastaReader (file, revcomp=revcomp, name=name, gap=gap)
    elif (format == "nib"):   return nib.NibReader     (file, revcomp=revcomp, name=name, gap=gap)
    elif (format == "qdna"):  return qdna.QdnaReader   (file, revcomp=revcomp, name=name, gap=gap)
    else: raise "Unknown sequence format %s" % format


def infer_format (file):
    format = None
    magic = struct.unpack(">L", file.read(4))[0]
    if (magic == nib.NIB_MAGIC_NUMBER) or (magic == nib.NIB_MAGIC_NUMBER_SWAP):
        format = "nib"
    elif (magic == qdna.qdnaMagic) or (magic == qdna.qdnaMagicSwap):
        format = "qdna"
    else:
        file.seek(0)
        if (file.read(1) == ">"):
            format = "fasta"
    file.seek(0)
    return format

