package ziq;

import java.nio.file.Paths;

/**
 * Main class for the Ziq task management application.
 * Handles initialization and execution of the application.
 */
public class Ziq {

    private static final String FILE_PATH = Paths.get(".", "data", "ziq.txt").toString();

    private Storage storage;
    private TaskList tasks;
    private Ui ui;

    /**
     * Constructs a new Ziq instance with the default file path for storage.
     */
    public Ziq() {
        this(FILE_PATH);
    }

    /**
     * Constructs a new Ziq instance with the specified file path for storage.
     *
     * @param filePath the path to the file where tasks are stored
     */
    public Ziq(String filePath) {
        assert filePath != null && !filePath.isEmpty() : "file path must not be null or empty";
        ui = new Ui();
        storage = new Storage(filePath, ui);
        try {
            tasks = new TaskList(storage.load());
        } catch (ZiqException e) {
            ui.showLoadingError();
            tasks = new TaskList();
        }
    }

    /**
     * Generates a response for the user's chat message by executing the command
     * and capturing the output for display in the GUI.
     *
     * @param input the user's message (command)
     * @return the response string to show, or the bye message if command is "bye"
     */
    public String getResponse(String input) {
        assert input != null : "input must not be null";
        String trimmed = input.trim();
        if (trimmed.isEmpty()) {
            return "";
        }
        StringBuilder out = new StringBuilder();
        ui.setResponseBuffer(out);
        try {
            boolean isExit = Parser.executeCommand(trimmed, tasks, ui, storage);
            if (isExit) {
                return "Bye. Hope to see you again!";
            }
            return out.toString().trim();
        } catch (ZiqException e) {
            ui.diagnoseError(e.getMessage());
            return out.toString().trim();
        } finally {
            ui.setResponseBuffer(null);
        }
    }

    /**
     * Runs the main application loop, processing user commands until exit.
     */
    public void run() {
        ui.welcomeUser();
        boolean isDone = false;

        while (!isDone) {
            try {
                String commandLine = ui.readCommand();
                isDone = Parser.executeCommand(commandLine, tasks, ui, storage);
            } catch (ZiqException e) {
                ui.diagnoseError(e.getMessage());
            }
        }
        System.out.println("buh-bye!");
    }

    /**
     * Entry point for the Ziq application.
     *
     * @param args command line arguments (not used)
     */
    public static void main(String[] args) {
        new Ziq(FILE_PATH).run();
    }
}

