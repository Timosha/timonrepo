# Makefile for source rpm: postgresql-jdbc
# $Id$
NAME := postgresql-jdbc
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
