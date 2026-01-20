// *** Learning Objective: Master Recursion by Procedurally Generating Colorful Fractal Patterns ***
//
// This tutorial will introduce you to the powerful concept of recursion,
// a programming technique where a function calls itself to solve a problem.
// We'll combine this with basic Java graphics to create beautiful,
// intricate fractal patterns. Fractals are self-similar shapes that
// repeat at different scales, showcasing the elegance of recursive design.
//
// By the end of this tutorial, you will understand:
// 1. What recursion is and how it works.
// 2. How to define a base case to stop recursion.
// 3. How to implement recursive algorithms.
// 4. How to use Java's `Graphics` class to draw shapes.
// 5. How to apply recursion to generate visual patterns.

import javax.swing.*;
import java.awt.*;
import java.util.Random;

// Main class to set up the JFrame and panel for drawing.
public class FractalGenerator extends JFrame {

    // Constructor for the main window.
    public FractalGenerator() {
        setTitle("Recursive Fractal Art"); // Set the window title.
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // Define what happens when the window is closed.
        setSize(800, 600); // Set the initial size of the window.

        // Create an instance of our custom drawing panel.
        FractalPanel panel = new FractalPanel();
        add(panel); // Add the drawing panel to the frame.
        setVisible(true); // Make the window visible.
    }

    // The main method where the application starts.
    public static void main(String[] args) {
        // Run the GUI creation on the Event Dispatch Thread (EDT) for thread safety.
        SwingUtilities.invokeLater(FractalGenerator::new);
    }
}

// Custom JPanel class responsible for drawing the fractal.
class FractalPanel extends JPanel {

    // A constant to control the initial size of the fractal.
    private static final int INITIAL_SIZE = 200;
    // A constant to control the maximum recursion depth.
    private static final int MAX_DEPTH = 8;

    // This method is called automatically by Swing to paint the component.
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g); // Call the superclass's paintComponent to ensure proper painting.
        Graphics2D g2d = (Graphics2D) g; // Cast to Graphics2D for more advanced drawing capabilities.

        // Set rendering hints for smoother drawing.
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        // Define the starting point for our fractal.
        // We center it horizontally and vertically.
        int startX = getWidth() / 2;
        int startY = getHeight() / 2;

        // Call our recursive drawing function.
        // We start with the initial size and maximum depth.
        drawFractal(g2d, startX, startY, INITIAL_SIZE, MAX_DEPTH);
    }

    // *** The Recursive Drawing Function ***
    // This is the core of our fractal generation.
    private void drawFractal(Graphics2D g, int x, int y, int size, int depth) {

        // *** Base Case: The Stopping Condition ***
        // If the current depth reaches 0, we stop recursing.
        // This prevents infinite recursion and defines the smallest detail of the fractal.
        if (depth <= 0) {
            return; // Exit the function without further calls.
        }

        // *** Recursive Step: Drawing and Calling Itself ***

        // 1. Draw something at the current level.
        // We draw a rectangle, its color determined by the recursion depth.
        // A simple way to get color variation is to use the depth.
        // We can map depth to shades of a color or to different colors entirely.
        // Here, we'll use a simple mapping to a color component.
        // The modulo operator (%) ensures the value stays within a range.
        int colorComponent = (MAX_DEPTH - depth) * 30 % 255;
        g.setColor(new Color(colorComponent, 255 - colorComponent, 150)); // Create a vibrant color.
        g.fillRect(x - size / 2, y - size / 2, size, size); // Draw a filled rectangle.

        // 2. Make recursive calls to draw smaller versions.
        // For a simple fractal like this, we might divide the space
        // and draw sub-fractals in each part.
        // We reduce the 'size' for the next level and decrement the 'depth'.

        // Calculate coordinates for the four corners of the current rectangle.
        int x1 = x - size / 4; // Top-left x
        int y1 = y - size / 4; // Top-left y
        int x2 = x + size / 4; // Top-right x
        int y2 = y - size / 4; // Top-right y
        int x3 = x - size / 4; // Bottom-left x
        int y3 = y + size / 4; // Bottom-left y
        int x4 = x + size / 4; // Bottom-right x
        int y4 = y + size / 4; // Bottom-right y

        // Recursively call drawFractal for each of the four corners,
        // creating a Sierpinski-like pattern.
        // We pass a smaller size (size / 2) and a reduced depth.
        drawFractal(g, x1, y1, size / 2, depth - 1);
        drawFractal(g, x2, y2, size / 2, depth - 1);
        drawFractal(g, x3, y3, size / 2, depth - 1);
        drawFractal(g, x4, y4, size / 2, depth - 1);
    }
}

// *** Example Usage ***
// To run this code:
// 1. Save the entire code as 'FractalGenerator.java'.
// 2. Compile it using a Java Development Kit (JDK):
//    javac FractalGenerator.java
// 3. Run the compiled code:
//    java FractalGenerator
//
// You will see a window appear with a colorful fractal pattern.
// Experiment by changing INITIAL_SIZE and MAX_DEPTH in the FractalPanel class
// to see how these parameters affect the generated fractal.
// For instance, increasing MAX_DEPTH will create more intricate details.
// Decreasing INITIAL_SIZE will make the starting fractal smaller.
// You can also modify the color calculation within drawFractal to create
// different color schemes.