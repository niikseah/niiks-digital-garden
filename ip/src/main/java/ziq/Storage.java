package ziq;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.regex.Pattern;

/**
 * Handles loading and saving tasks to/from a file.
 * Manages persistent storage of task data.
 */
public class Storage {
    private static final String FILE_DELIMITER = " | ";
    private static final String DONE_STATUS_CODE = "1";
    private static final String NOT_DONE_STATUS_CODE = "0";
    private static final int MINIMUM_PARTS_COUNT = 3;
    private static final int TODO_PARTS_COUNT = 4;
    private static final int DEADLINE_PARTS_COUNT = 5;
    private static final int EVENT_PARTS_COUNT = 6;
    private static final int TYPE_INDEX = 0;
    private static final int STATUS_INDEX = 1;
    private static final int DESCRIPTION_INDEX = 2;
    private static final int TODO_TAG_INDEX = 3;
    private static final int DEADLINE_TIME_INDEX = 3;
    private static final int DEADLINE_TAG_INDEX = 4;
    private static final int EVENT_START_INDEX = 3;
    private static final int EVENT_END_INDEX = 4;
    private static final int EVENT_TAG_INDEX = 5;

    private final String filePath;
    private final Ui ui;

    /**
     * Constructs a Storage instance with the specified file path and UI for messages.
     *
     * @param filePath the path to the file where tasks are stored
     * @param ui the UI for output (e.g. save error messages)
     */
    public Storage(String filePath, Ui ui) {
        this.filePath = filePath;
        this.ui = ui;
    }

    /**
     * Loads tasks from the storage file.
     *
     * @return a list of tasks loaded from the file, or an empty list if file doesn't exist
     * @throws ZiqException if there is an error reading or parsing the file
     */
    public ArrayList<Task> load() throws ZiqException {
        ArrayList<Task> loadedTasks = new ArrayList<>();
        File file = new File(filePath);
        if (!file.exists()) {
            return loadedTasks;
        }

        // Check if file path points to a directory instead of a file
        if (file.isDirectory()) {
            throw new ZiqException("Save file path points to a directory, not a file: " + filePath
                    + ". Please specify a valid file path.");
        }

        try (Scanner s = new Scanner(file)) {
            int lineNumber = 0;
            while (s.hasNext()) {
                lineNumber++;
                String line = s.nextLine();
                if (line.trim().isEmpty()) {
                    continue; // Skip empty lines
                }
                Task task = parseTaskFromLine(line);
                if (task != null) {
                    loadedTasks.add(task);
                } else {
                    // Log warning about invalid line but continue loading
                    ui.printLine("Warning: Skipped invalid line " + lineNumber + " in save file: " + filePath);
                }
            }
        } catch (IOException e) {
            if (e instanceof FileNotFoundException) {
                return loadedTasks;
            }
            String msg = e.getMessage();
            if (msg != null && (msg.toLowerCase().contains("access") || msg.toLowerCase().contains("permission"))) {
                throw new ZiqException("Cannot read save file: access denied. Check file permissions for " + filePath);
            }
            throw new ZiqException("Cannot read save file: " + (msg != null ? msg : "unknown error"));
        } catch (SecurityException e) {
            throw new ZiqException("Cannot read save file: access denied. Check file permissions for " + filePath);
        } catch (ZiqException e) {
            throw e;
        } catch (Exception e) {
            throw new ZiqException("Save file content is invalid or corrupted: " + e.getMessage()
                    + ". Fix or remove the file and try again.");
        }
        return loadedTasks;
    }

    /**
     * Parses a single line from the save file into a Task object.
     *
     * @param line the line to parse
     * @return the parsed Task, or null if the line is invalid
     * @throws ZiqException if there is an error parsing the line
     */
    private Task parseTaskFromLine(String line) throws ZiqException {
        String[] parts = line.split(Pattern.quote(FILE_DELIMITER));
        if (parts.length < MINIMUM_PARTS_COUNT) {
            return null;
        }

        TaskType type;
        try {
            type = TaskType.findTaskType(parts[TYPE_INDEX]);
        } catch (ZiqException e) {
            return null;
        }
        Task task = createTaskFromParts(type, parts);
        if (task != null && parts[STATUS_INDEX].equals(DONE_STATUS_CODE)) {
            task.markAsDone();
        }
        return task;
    }

    /**
     * Creates a Task object from parsed parts based on task type.
     *
     * @param type the type of task
     * @param parts the parsed parts from the save file line
     * @return the created Task, or null if type is invalid
     * @throws ZiqException if there is an error creating the task
     */
    private Task createTaskFromParts(TaskType type, String[] parts) throws ZiqException {
        try {
            switch (type) {
            case TODO:
                if (parts.length < TODO_PARTS_COUNT - 1) {
                    return null;
                }
                Todo todo = new Todo(parts[DESCRIPTION_INDEX]);
                // Tag is optional (for backward compatibility with old save files)
                if (parts.length >= TODO_PARTS_COUNT && !parts[TODO_TAG_INDEX].isEmpty()) {
                    todo.setTag(parts[TODO_TAG_INDEX]);
                }
                return todo;
            case DEADLINE:
                if (parts.length < DEADLINE_PARTS_COUNT - 1) {
                    return null;
                }
                LocalDateTime deadlineTime = LocalDateTime.parse(parts[DEADLINE_TIME_INDEX]);
                // If time is exactly midnight (00:00:00), assume no time was originally specified
                boolean hasTime = !(deadlineTime.getHour() == 0 && deadlineTime.getMinute() == 0
                        && deadlineTime.getSecond() == 0);
                Deadline deadline = new Deadline(parts[DESCRIPTION_INDEX], deadlineTime, hasTime);
                // Tag is optional (for backward compatibility with old save files)
                if (parts.length >= DEADLINE_PARTS_COUNT && !parts[DEADLINE_TAG_INDEX].isEmpty()) {
                    deadline.setTag(parts[DEADLINE_TAG_INDEX]);
                }
                return deadline;
            case EVENT:
                if (parts.length < EVENT_PARTS_COUNT - 1) {
                    return null;
                }
                LocalDateTime startTime = LocalDateTime.parse(parts[EVENT_START_INDEX]);
                LocalDateTime endTime = LocalDateTime.parse(parts[EVENT_END_INDEX]);
                Event event = new Event(parts[DESCRIPTION_INDEX], startTime, endTime);
                // Tag is optional (for backward compatibility with old save files)
                if (parts.length >= EVENT_PARTS_COUNT && !parts[EVENT_TAG_INDEX].isEmpty()) {
                    event.setTag(parts[EVENT_TAG_INDEX]);
                }
                return event;
            default:
                return null;
            }
        } catch (DateTimeParseException e) {
            throw new ZiqException("Save file contains an invalid date. Fix or remove the file: " + filePath);
        }
    }

    /**
     * Saves the list of tasks to the storage file.
     *
     * @param list the list of tasks to save
     * @throws ZiqException if there is an error saving the file
     */
    public void save(ArrayList<Task> list) throws ZiqException {
        assert list != null : "task list to save must not be null";
        try {
            File file = new File(filePath);

            // Check if file path points to an existing directory
            if (file.exists() && file.isDirectory()) {
                throw new ZiqException("Cannot save: file path points to a directory: " + filePath
                        + ". Please specify a valid file path.");
            }

            File parent = file.getParentFile();
            if (parent != null && !parent.exists() && !parent.mkdirs()) {
                throw new ZiqException("Could not create data folder. Check write permissions: " + parent.getPath());
            }
            writeTasksToFile(file, list);
        } catch (IOException e) {
            String msg = e.getMessage();
            if (msg != null && (msg.toLowerCase().contains("access") || msg.toLowerCase().contains("permission"))) {
                throw new ZiqException("Could not save tasks: access denied. Check file permissions for " + filePath);
            }
            throw new ZiqException("Could not save tasks to file: " + (msg != null ? msg : "unknown error"));
        } catch (SecurityException e) {
            throw new ZiqException("Could not save tasks: access denied. Check file permissions for " + filePath);
        }
    }

    /**
     * Writes all tasks to the file in the save format.
     *
     * @param file the file to write to
     * @param taskList the list of tasks to save
     * @throws IOException if there is an error writing to the file
     */
    private void writeTasksToFile(File file, ArrayList<Task> taskList) throws IOException {
        try (FileWriter fileWriter = new FileWriter(file)) {
            for (Task task : taskList) {
                String line = formatTaskForSave(task);
                fileWriter.write(line + System.lineSeparator());
            }
        }
    }

    /**
     * Formats a task into a string for saving to file.
     *
     * @param task the task to format
     * @return the formatted string representation
     */
    private String formatTaskForSave(Task task) {
        TaskType type = determineTaskType(task);
        String statusCode = task.getStatus().equals("✅") ? DONE_STATUS_CODE : NOT_DONE_STATUS_CODE;
        StringBuilder line = new StringBuilder();
        line.append(type.getCode()).append(FILE_DELIMITER);
        line.append(statusCode).append(FILE_DELIMITER);
        line.append(task.description());

        String tag = task.getTag();
        String tagStr = (tag != null && !tag.isEmpty()) ? tag : "";

        if (task instanceof Deadline) {
            Deadline deadline = (Deadline) task;
            line.append(FILE_DELIMITER).append(deadline.by());
            line.append(FILE_DELIMITER).append(tagStr);
        } else if (task instanceof Event) {
            Event event = (Event) task;
            line.append(FILE_DELIMITER).append(event.from());
            line.append(FILE_DELIMITER).append(event.to());
            line.append(FILE_DELIMITER).append(tagStr);
        } else {
            // Todo
            line.append(FILE_DELIMITER).append(tagStr);
        }
        return line.toString();
    }

    /**
     * Determines the TaskType of a given task.
     *
     * @param task the task to check
     * @return the corresponding TaskType
     */
    private TaskType determineTaskType(Task task) {
        if (task instanceof Todo) {
            return TaskType.TODO;
        } else if (task instanceof Deadline) {
            return TaskType.DEADLINE;
        } else {
            return TaskType.EVENT;
        }
    }
}

