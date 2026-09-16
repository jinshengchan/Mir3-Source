# -*- coding: utf-8 -*-
#目前可以listener fun_name
# "OnProcess","OnDie","OnDayChange","OnWeekChange","OnMonthChange"


_all_data={}

def add_listener(fun_name,fun):
	_all_data[fun_name] = fun



def trig_player(Sender,fun_name,args):
	if(fun_name in _all_data.keys()):
		fun = _all_data[fun_name]
		return fun(args)
	else:	
		return
		
		