"""Run bash scripts"""
import sys
import subprocess

# name of script passed to file
scriptname = sys.argv[1]
scriptname = "scripts/" + scriptname + ".sh"

subprocess.call(scriptname, shell=True)
