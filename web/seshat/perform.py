import subprocess

# subprocess.call("/home/lyon106/seshat/seshat", "-c /home/lyon106/seshat/Config/CONFIG -i /home/lyon106/seshat/SampleMathExps/exp.scgink")
subprocess.call("./seshat %s %s" % (str("-c Config/CONFIG"), str("-i SampleMathExps/exp.scgink")), shell=True)