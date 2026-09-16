_data={}
_all_data={}

def add_listener(mon_index,fun_name,fun):
	if (mon_index not in _data.keys()):  
		_data[mon_index] = {}
	d = _data[mon_index];
	d[fun_name] = fun;

def add_all_listener(fun_name,fun):
	_all_data[fun_name] = fun



def trig_mon(mon,fun_name,args):
	if(mon.MonsterInfo.Index in _data.keys()):
		d = _data[mon.MonsterInfo.Index];
		if(fun_name in d.keys()):
			fun = d[fun_name]
			return fun(args)
		else:
			return
	elif(fun_name in _all_data.keys()):
		fun = _all_data[fun_name]
		return fun(args)
	else:	
		return