import subprocess

# this will need sudo.
command = ['sudo', 'pwrstat', '-status']

# https://stackoverflow.com/questions/8217613/how-to-get-data-from-command-line-from-within-a-python-program
p = subprocess.Popen(command)
text = p.stdout.read()
retcode = p.wait()