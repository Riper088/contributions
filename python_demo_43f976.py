# Fractal Art with Recursion and Turtle Graphics

# Learning Objective:
# This tutorial will teach you how to generate intricate fractal art
# using the power of recursion and the Python Turtle graphics module.
# We will focus on understanding how a recursive function can create
# complex patterns by repeatedly calling itself with smaller inputs.

# What is Recursion?
# Recursion is a programming technique where a function calls itself
# within its own definition. Think of it like a set of Russian nesting dolls;
# each doll contains a smaller version of itself.
# In fractal generation, this means a shape is drawn by repeating the
# same drawing process on smaller and smaller parts of the shape itself.

# What is Fractal Art?
# Fractal art is a form of algorithmic art created by calculating
# fractal objects and representing the calculation results as still
# images, animations, or other media. Fractals are characterized by
# self-similarity, meaning that parts of the fractal look like the whole,
# but at smaller scales.

# The Turtle Module:
# The Turtle module provides a simple way to draw graphics. It's like
# having a virtual pen on a canvas that you can move around.
# We'll use turtle commands like forward(), left(), right(), pendown(),
# and penup() to draw our fractal.

import turtle

def draw_fractal(t, order, size):
    """
    Recursively draws a fractal pattern.

    Args:
        t: The turtle object to draw with.
        order: The current recursion depth (determines complexity).
        size: The length of the current line segment to draw.
    """
    # Base Case: When the recursion depth is 0, we stop drawing.
    # This is crucial to prevent infinite recursion.
    if order == 0:
        t.forward(size)  # Draw a simple line segment at the smallest scale.
        return  # Exit the function

    # Recursive Step: If order is greater than 0, we break down the
    # current drawing into smaller parts.

    # 1. Divide the current segment into three equal parts.
    new_size = size / 3

    # 2. Recursively call draw_fractal for the first third.
    # This draws the first "branch" or segment of the fractal.
    draw_fractal(t, order - 1, new_size)

    # 3. Turn left to prepare for the next segment.
    # The angle determines the shape of the fractal. For a Koch curve, it's 60 degrees.
    t.left(60)

    # 4. Recursively call draw_fractal for the second third.
    # This draws the middle "spike" or outward segment.
    draw_fractal(t, order - 1, new_size)

    # 5. Turn right to realign for the next segment.
    t.right(120)  # Turn 120 degrees (60 degrees left + 60 degrees right)

    # 6. Recursively call draw_fractal for the third third.
    # This draws the final "branch" or segment, mirroring the first.
    draw_fractal(t, order - 1, new_size)

    # 7. Turn left again to prepare for returning to the starting point
    # of the larger segment or to draw subsequent parts if this were a more complex fractal.
    t.left(60)

    # 8. Move forward by the remaining length of the original segment.
    # This ensures that after drawing the three smaller segments and turns,
    # the turtle is positioned at the end of the original `size` segment.
    draw_fractal(t, order - 1, new_size)


# --- Example Usage ---

if __name__ == "__main__":
    # Set up the screen
    screen = turtle.Screen()
    screen.setup(width=800, height=600)  # Set the window size
    screen.bgcolor("white")           # Set the background color
    screen.title("Recursive Fractal Art - Koch Curve") # Set the window title

    # Create a turtle object
    fractal_turtle = turtle.Turtle()
    fractal_turtle.speed(0)          # Set the speed to fastest (0)
    fractal_turtle.penup()           # Lift the pen to move without drawing
    fractal_turtle.goto(-200, 0)     # Move to a starting position
    fractal_turtle.pendown()         # Put the pen down to start drawing
    fractal_turtle.pencolor("blue")  # Set the drawing color

    # Define fractal parameters
    fractal_order = 4  # The depth of recursion. Higher numbers mean more detail.
    initial_size = 400 # The initial length of the line segment.

    # Call the recursive function to draw the fractal
    draw_fractal(fractal_turtle, fractal_order, initial_size)

    # Keep the window open until it's manually closed
    screen.mainloop()

# How to experiment:
# 1. Change `fractal_order`: Try values from 0 to 5. See how complexity increases.
# 2. Change `initial_size`: Observe how the overall scale of the fractal changes.
# 3. Change `t.left()` and `t.right()` angles: This will create entirely different fractal shapes!
# 4. Change `t.pencolor()` and `screen.bgcolor()`: Experiment with colors.
# 5. Modify the order of `draw_fractal` calls or the number of recursive calls: This is how you can design new fractal patterns!