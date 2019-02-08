cur_x = 3
rate = 0.01 # Learning rate
precision = 0.00001
previous_step_size = 1
max_iters = 10000
iters = 0
df = lambda x: 2*x - 2.71 #Gradient

while previous_step_size > precision and iters < max_iters:
    prev_x = cur_x  # Store current x value in prev_x
    cur_x = cur_x - rate * df(prev_x)  # Grad descent
    previous_step_size = abs(cur_x - prev_x)  # Change in x
    iters = iters + 1  # iteration count
    print("Iteration", iters, "\nX value is", cur_x)  # Print iterations

print("The local minimum occurs at", cur_x)