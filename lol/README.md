本项目的目的是爬取玩加赛事上的lol比赛数据并通过python进行分析。
赛事数据存储在Mysql的lol库的games表中。
建表语句为:
create table games(
id int(10) not null primary key auto_increment comment '主键',
mt_time datetime comment '比赛时间',
homeTeam varchar(10) not null comment '主队',
visitingTeam varchar(10) not null comment '客队',
score varchar(10) not null comment '比分',
time1 varchar(15)  not null comment '第一场比赛时间',
time2 varchar(15)  comment '第二场比赛时间',
time3 varchar(15)  comment '第三场比赛时间',
time4 varchar(15)  comment '第四场比赛时间',
time5 varchar(15)  comment '第五场比赛时间'
);