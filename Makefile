# Makefile for source rpm: postgresql
# $Id$
NAME := postgresql
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
