本项目的目的是爬取玩加赛事上的lol比赛数据并通过python进行分析。</br>
赛事数据存储在Mysql的lol库的games表中。</br>
建表语句为:</br>
create table games(</br>
id int(10) not null primary key auto_increment comment '主键',</br>
mt_time datetime comment '比赛时间',</br>
homeTeam varchar(10) not null comment '主队',</br>
visitingTeam varchar(10) not null comment '客队',</br>
score varchar(10) not null comment '比分',</br>
time1 varchar(15)  not null comment '第一场比赛时间',</br>
time2 varchar(15)  comment '第二场比赛时间',</br>
time3 varchar(15)  comment '第三场比赛时间',</br>
time4 varchar(15)  comment '第四场比赛时间',</br>
time5 varchar(15)  comment '第五场比赛时间'</br>
);
