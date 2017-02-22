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
import json
import logging

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
	#获取票价
	def get_price(self, raw_train):
		train_no = raw_train['train_no']
		from_station_no = raw_train['from_station_no']
		to_station_no = raw_train['to_station_no']
		seat_types = raw_train['seat_types']
		train_date = raw_train['start_train_date'][0:4]+'-'+raw_train['start_train_date'][4:6]+'-'+raw_train['start_train_date'][6:8]
		#拼装查询票价的url
		url = "https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no={}&from_station_no={}&to_station_no={}&seat_types={}&train_date={}".format(train_no, from_station_no, to_station_no, seat_types, train_date)
		r = requests.get(url, verify = False)
		# logging.debug(r.json())
		return r.json()['data'] if r.json()!=-1 else {}

	def trains(self):
		for raw_train in self.available_trains:
			raw_train = raw_train['queryLeftNewDTO']
			train_code = raw_train['station_train_code']
			initial = train_code[0].lower()
			logging.debug(raw_train)
			logging.debug(train_code)
			if not self.option or initial in self.option:
				price = self.get_price(raw_train)
				train = [
				   train_code,
				   '\n'.join([raw_train['from_station_name'], raw_train['to_station_name']]),
				   '\n'.join([raw_train['start_time'],raw_train['arrive_time']]),
				   self.get_duration(raw_train),
				   '\n'.join([raw_train['zy_num'],price['A9'] if 'A9' in price.keys() else '']),
                   '\n'.join([raw_train['ze_num'],price['O'] if 'O' in price.keys() else '']),
                   '\n'.join([raw_train['rw_num'],price['A4'] if 'A4' in price.keys() else '']),
                   '\n'.join([raw_train['yw_num'],price['A3'] if 'A3' in price.keys() else '']),
                   '\n'.join([raw_train['yz_num'],price['A1'] if 'A1' in price.keys() else '']),
                   '\n'.join([raw_train['wz_num'],price['WZ'] if 'WZ' in price.keys() else '']),
				]
				yield train

	def pretty_print(self):
		pt = PrettyTable()
		pt._set_field_names(self.header)
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
	url="https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT".format(date, from_station, to_station)
	# 提交url
	r = requests.get(url, verify=False)
	options = ''.join([
		key for key, value in arguments.items() if value is True
	])
	available_trains = r.json()['data']
	logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')
	TrainInfo(available_trains,options).pretty_print()

if __name__ == '__main__':
	cli()

