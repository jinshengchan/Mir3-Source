# -*- coding: utf-8 -*-
_all_data={}

def add_listener(fun_name,fun):
	_all_data[fun_name] = fun



def trig_server(fun_name,args):
	if(fun_name in _all_data.keys()):
		fun = _all_data[fun_name]
		return fun(args)
	else:	
		return


def AutoRecycleWeapons(args=None):
	from Ser.定时活动 import AutoRecycleWeapons as callback
	return callback(args)
