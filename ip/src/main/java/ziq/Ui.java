package ziq;

import java.util.Scanner;

/**
 * Handles user interface interactions.
 * Manages input/output operations for the application.
 * When a response buffer is set (e.g. for GUI), output is captured there instead of System.out.
 */
public class Ui {
    private final Scanner sc;
    private StringBuilder responseBuffer;

    /**
     * Constructs a new Ui instance with a Scanner for reading user input.
     */
    public Ui() {
        this.sc = new Scanner(System.in);
    }

    /**
     * Sets the buffer to capture output (for GUI). When null, output goes to System.out.
     *
     * @param buffer the buffer to append output to, or null for console output
     */
    public void setResponseBuffer(StringBuilder buffer) {
        this.responseBuffer = buffer;
    }

    /**
     * Prints one or more lines to the current output (buffer if set, otherwise System.out).
     *
     * @param lines the lines to print (varargs)
     */
    public void printLine(String... lines) {
        for (String line : lines) {
            if (responseBuffer != null) {
                responseBuffer.append(line).append("\n");
            } else {
                System.out.println(line);
            }
        }
    }

    /**
     * Displays the welcome message to the user.
     */
    public void welcomeUser() {
        printLine("Hello, I'm Ziq!");
        printLine("What can I do for you?");
        printLine("");
    }

    /**
     * Reads a command from the user.
     *
     * @return the user's input command
     */
    public String readCommand() {
        return sc.nextLine();
    }

    /**
     * Displays an error message to the user.
     *
     * @param message the error message to display
     */
    public void diagnoseError(String message) {
        printLine("oop. " + message);
    }

    /**
     * Displays an error message when loading tasks fails.
     */
    public void showLoadingError() {
        printLine("oop. error loading,,, starting afresh!");
    }
}

