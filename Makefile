# Makefile for source rpm: ImageMagick
# $Id$
NAME := ImageMagick
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
