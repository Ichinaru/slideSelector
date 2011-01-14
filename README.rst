slideSelector
#############

Introduction
============

The slideSelector project provide a way to extract regions from ndpi files (Hamamatsu NanoZoomer Digital Pathology images).
The regions are defined using the NDP.view image viewer.
The slideSelector project offers an easy way to analyse specific histological regions.

Installation
============

Stay tuned...

Usage
=====

Due to the very erratic development of the project, two versions might be found.
The first one, rather complete in terms of features but rather difficult to extend uses an obsolete wrapper for the NDPRead library that has some memory leaks.
The second one, that is rather simple and featureless is build with a modular design and uses the new ctypes wrapper.

For the first version, the entry point of the software is the file slideSelector.py
For the second version, well it's entry...

As you understand, the second version will gain in features very soon