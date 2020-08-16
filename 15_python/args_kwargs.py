# 200816
'''
- *args: 변수가 tuple 형태로 입력
- **kwargs: 변수가 dictionary 형태로 입력
- 필수 입력은 지정하고, 선택 입력값을 kwargs로 받음
- References
	- https://toughbear.tistory.com/entry/python-args%EC%99%80-kwargs-%EC%9D%98%EB%AF%B8%EC%99%80-%EC%82%AC%EC%9A%A9
'''

def args_func(*args):
	print(args)

def kwargs_func(**kwargs):
	print(kwargs)

def calculate(input_, **kwargs):

	res = 0
	if 'square' in kwargs:
		print('Option: square')
		res = input_**2 if kwargs['square'] == True else input_
	elif 'init' in kwargs:
		print('Option: init')
		res = 0 if kwargs['init'] == True else input_
	else:
		print('Option: nothing')
		res = input_
	return res

if __name__ == '__main__':
	#args_func(1, 2)
	#kwargs_func(a=1, b=2)
	print(calculate(4, init=True))