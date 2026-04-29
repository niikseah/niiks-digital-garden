package ziq;

import javafx.application.Application;

/**
 * A launcher class to workaround classpath issues.
 */
public class Launcher {
    /**
     * Entry point for launching the JavaFX application.
     *
     * @param args command line arguments (not used)
     */
    public static void main(String[] args) {
        Application.launch(Main.class, args);
    }
}

