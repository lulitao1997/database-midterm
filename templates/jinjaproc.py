from jinja2 import FileSystemLoader
from jinja2.environment import Environment
import os, sys

cwd = os.getcwd()
filename = sys.argv[1]

env = Environment()
env.loader = FileSystemLoader('.')
tmpl = env.get_template(filename)
ans = tmpl.render()
outfile = open('output.html','w')

outfile.write(ans)
outfile.close()
