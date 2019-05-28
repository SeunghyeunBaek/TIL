import numpy

def compute_error_for_given_points(b,m,points):
	totalError = 0 
	for i in range(0,len(points)):
		x = points[i,0]
		y = points[i,1]
		totalError += (y-(m*x+b))**2
	return totalError/float(len(points))

def step_gradient(currents_b, current_m, points, learning_rate):
	#gradient descent
	b_gradient = 0
	m_gradient = 0
	n = float(len(points))
	for i in range(len(points)):
		x = points[i,0]
		y = points[i,1]
		b_gradient += -(2/n)*(y-((current_m*x)+current_b))
		m_gradient += -(2/n)*x*(y-((current_m*x)+current_b))
	# update b,m
	new_b = current_b - (learning_rate*b_gradient)
	new_m = current_m - (learning_rate*m_gradient)
	return(new_b,new_m)

def gradient_descent_runner(points, starting_b, starting_m, learning_rate):
	b = starting_m
	m = starting_m

	for i in range(num_iteration):
		b,m = step_gradient(b,m,array(points))

def run(num_iteration,learning_rate):
	# get Data
	points =
	#hyperparameters
	#y- mx+b(slope formula)
	initial_b = 0
	initial_m = 0
	[b,m] = gradient_descent_runner(points, initial_m,initial_b,num_iteration)
	print(f'best b : {b}')
	print(f'best m : {m}')

if __name__='__main__':
	run(1000,0.01)