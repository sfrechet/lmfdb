# -*- coding: utf-8 -*-
# This Blueprint is about Crystals
# Author: Anne Schilling 

import flask
from lmfdb import base
from flask import render_template, request, abort, url_for, make_response, redirect
import os
import re
from lmfdb.crystals import crystals_page, logger
import sage.all
from sage.all import ZZ, latex, Partition, CrystalOfTableaux

def get_bread(breads=[]):
    bc = [("Crystals", url_for(".index"))]
    for b in breads:
        bc.append(b)
    return bc

@crystals_page.route("/show", methods = ["GET"])
def show():
    weight = request.args.get('weight', None)
    cartan_type = str(request.args.get('cartan_type', None))
    rank = int(request.args.get('rank', None))
    #logger.info("weight = %s" % weight)
    p = Partition(map(int,weight.split(",")))
    crystal = CrystalOfTableaux([cartan_type,rank], shape=p)

    from sage.misc.latex import png
    png(crystal, "/Users/anne/lmfdb/lmfdb/static/crystal.png", debug=True, pdflatex=True)
    return render_template("crystals.html", cartan_type= cartan_type, weight = p, rank = rank, 
                           crystal = crystal,
                           bread = get_bread())

@crystals_page.route("/littelmann")
def show_littelmann():
    return render_template("littelmann-paths.html", title = "Littelmann Paths")

@crystals_page.route("/calc-littelmann")
def calc_littelmann():
    v = request.args.get('value', 0)
    return str( 2 * int(v) )

@crystals_page.route("/littelmann-image")
def littelmann_image():
    from sage.all_cmdline import CrystalOfLSPaths, vector, line

    def line_of_path(path):
        if path is None:
            result = []
        else:
            L = path.parent().weight.parent()
            v = vector(L.zero())
            result = [v]
            for d in path.value:
               v = v + vector(d)
               result.append(v)
        result = list(result)
        result = line(result)
        result.set_axes_range(-10,10,-10,10)
        return result

    from lmfdb.utils import image_callback
    C = CrystalOfLSPaths(['A',2],[6,3])
    x = C[int(request.args.get("value"))]
    y = x.f_string([1, 1])
    return image_callback(line_of_path(y))

@crystals_page.route("/")
def index():
    bread = get_bread()
    return render_template("crystals-index.html", title="Crystals", bread=bread)

