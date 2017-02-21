#coding:utf-8

"""命令行火车票查看器

Usage:
    ticket [-gkzdt] <from> <to> <date>

Options:
    -h,-help: 显示帮助菜单
    -g: 高铁
    -k: 普快
    -z: 直达
    -d: 动车
    -t: 特快
Example:
   ticket -g 北京 上海 2017-1-20
"""
from docopt import docopt
from station import stations
import requests
from prettytable import PrettyTable

class TrainInfo:
	header = '车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split()
	def __init__(self, available_trains, option):
		""" 查询到的火车班次集合
		:param available_trains: 一个列表，包含了可获得的火车班次信息，每个班次信息是一个dict
		:param option: 查询的选项，如：高铁，动车，etc...
		"""
		self.available_trains = available_trains
		self.option = option
	def get_duration(self, raw_train):
		duration = raw_train.get('lishi').replace(':',"小时")+'分'
		if duration.startswith('00'):
			return duration[4:]
		if duration.startswith('0'):
			return duration[1:]
		return duration

	def trains(self):
		for raw_train in self.available_trains:
			raw_train = raw_train['queryLeftNewDTO']
			train_no = raw_train['station_train_code']
			initial = train_no[0].lower()
			if not self.option or initial in self.option:
				train = [
				   train_no,
				   '\n'.join([raw_train['from_station_name'], raw_train['to_station_name']]),
				   '\n'.join([raw_train['start_time'],raw_train['arrive_time']]),
				   self.get_duration(raw_train),
				   raw_train['zy_num'],
                   raw_train['ze_num'],
                   raw_train['rw_num'],
                   raw_train['yw_num'],
                   raw_train['yz_num'],
                   raw_train['wz_num'],
				]
				yield train

	def pretty_print(self):
		pt = PrettyTable()
		pt._set_field_names(self.header)
		# print(self.trains())
		for item in self.trains():
			pt.add_row(item)
		print(pt)

def cli():
	"""command-line interface"""
	arguments=docopt(__doc__)
	from_station = stations.get(arguments['<from>'])
	to_station = stations.get(arguments['<to>'])
	date = arguments['<date>']
	# 构建url
	# url=("https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date={}&leftTicket"
	# 	"DTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT").format(date, from_station, to_station)
	url="https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT".format(date, from_station, to_station)
	# 提交url
	r = requests.get(url, verify=False)
	options = ''.join([
		key for key, value in arguments.items() if value is True
	])
	available_trains = r.json()['data']
	TrainInfo(available_trains,options).pretty_print()

if __name__ == '__main__':
	cli()

