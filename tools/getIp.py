import commands
import re
sta,ret = commands.getstatusoutput('ifconfig')
regx = 'inet\s(10.\w+.\w+.\w+)?'
result = re.findall(regx, ret)[1]
print(result)