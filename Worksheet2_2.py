def f(x): # Function f(x) = 3x^2.
    return 3 * x**2

def f_derivative(x):
    """
    Derivative f'(x) = 6x.
    
    Explanation:
    - The original function is f(x) = 3x^2.
    - To find the derivative, we use the power rule of differentiation:
      If f(x) = ax^n, then f'(x) = a * n * x^(n-1).
    - Applying the rule to f(x) = 3x^2:
      - a = 3, n = 2
      - f'(x) = 3 * 2 * x^(2-1) = 6x
    """
    return 6 * x

def gradient_descent(initial_x, alpha, theta, max_iterations=1000):
    """
    Perform gradient descent to minimize f(x) = 3x^2.
    
    - initial_x: Starting point for x.
    - alpha: Learning rate (step size).
    - theta: Convergence threshold (when to stop).
    - max_iterations: Maximum number of iterations to prevent infinite loops.
    """
    x = initial_x
    for step in range(max_iterations): # Calculate the gradient (slope) at the current point
        gradient = f_derivative(x)
        
        # Check if the gradient is small enough to stop
        if abs(gradient) < theta:
            print(f"\nConverged at step {step}:")
            print(f"  Final x = {x:.5f}")
            print(f"  Final f(x) = {f(x):.5f}")
            return x
        
        # Update x by moving in the direction that reduces f(x)
        x = x - alpha * gradient
        
        # Print the step information
        print(f"\nStep {step}:")
        print(f"  x = {x:.5f}")
        print(f"  f(x) = {f(x):.5f}")
        print(f"  Gradient = {gradient:.5f}")

    print("Did not converge within the maximum number of iterations.")
    return x

# Parameters
initial_x = 10  # Starting point for x
alpha = 0.1     # Learning rate
theta = 0.001   # Convergence threshold

# Run the gradient descent
print("Running Gradient Descent for f(x) = 3x^2")
final_x = gradient_descent(initial_x, alpha, theta)
