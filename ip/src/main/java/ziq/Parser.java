package ziq;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;

/**
 * Parses and executes user commands.
 * Handles all command types: todo, deadline, event, mark, unmark, delete, list, find, schedule, bye.
 */
public class Parser {

    public static final DateTimeFormatter OUTPUT_FORMAT = DateTimeFormatter.ofPattern("MMM dd yyyy, h:mm a");
    private static final DateTimeFormatter INPUT_FORMAT = DateTimeFormatter.ofPattern("ddMMyyyy HHmm");
    private static final DateTimeFormatter DEADLINE_INPUT_FORMAT = DateTimeFormatter.ofPattern("ddMMyyyy HHmm");
    private static final DateTimeFormatter DATE_ONLY_FORMAT = DateTimeFormatter.ofPattern("ddMMyyyy");
    private static final int COMMAND_TODO_PREFIX_LENGTH = 5;
    private static final int COMMAND_DEADLINE_PREFIX_LENGTH = 9;
    private static final int COMMAND_EVENT_PREFIX_LENGTH = 6;
    private static final int COMMAND_DELETE_PREFIX_LENGTH = 7;
    private static final int COMMAND_FIND_PREFIX_LENGTH = 5;
    private static final int COMMAND_SCHEDULE_PREFIX_LENGTH = 9;
    private static final int COMMAND_TAG_PREFIX_LENGTH = 4;
    private static final int COMMAND_ORGANISE_PREFIX_LENGTH = 9;
    private static final int DISPLAY_INDEX_OFFSET = 1;

    /**
     * Parses and executes a user command.
     *
     * @param input the user's input command
     * @param tasks the task list to modify
     * @param ui the UI handler for output
     * @param storage the storage handler for saving tasks
     * @return true if the command is "bye" (exit), false otherwise
     * @throws ZiqException if the command is invalid or cannot be executed
     */
    public static boolean executeCommand(String input, TaskList tasks, Ui ui, Storage storage) throws ZiqException {
        assert input != null : "input must not be null";
        assert tasks != null : "tasks must not be empty";
        assert ui != null : "ui must not be empty";
        assert storage != null : "storage must not be empty";
        String trimmedInput = input.trim();
        if (trimmedInput.isEmpty()) {
            throw new ZiqException("command me now. enter 'help' for a list of commands.");
        }
        // Normalize whitespace: replace multiple spaces/tabs with single space
        String normalized = trimmedInput.replaceAll("\\s+", " ");

        if (normalized.equalsIgnoreCase("bye")) {
            return true;
        }

        if (normalized.equalsIgnoreCase("list")) {
            printTaskList(tasks, ui);
        } else if (normalized.equalsIgnoreCase("clear")) {
            handleClear(tasks, ui, storage);
        } else if (normalized.equalsIgnoreCase("mark") || normalized.startsWith("mark ")) {
            handleMark(normalized, tasks, ui, storage, true);
        } else if (normalized.equalsIgnoreCase("unmark") || normalized.startsWith("unmark ")) {
            handleMark(normalized, tasks, ui, storage, false);
        } else if (normalized.equalsIgnoreCase("todo") || normalized.startsWith("todo ")) {
            handleTodo(normalized, tasks, ui, storage);
        } else if (normalized.equalsIgnoreCase("deadline") || normalized.startsWith("deadline ")) {
            handleDeadline(normalized, tasks, ui, storage);
        } else if (normalized.equalsIgnoreCase("event") || normalized.startsWith("event ")) {
            handleEvent(normalized, tasks, ui, storage);
        } else if (normalized.equalsIgnoreCase("delete") || normalized.startsWith("delete ")) {
            handleDelete(normalized, tasks, ui, storage);
        } else if (normalized.equalsIgnoreCase("find") || normalized.startsWith("find ")) {
            handleFind(normalized, tasks, ui);
        } else if (normalized.equalsIgnoreCase("schedule") || normalized.startsWith("schedule ")) {
            handleSchedule(normalized, tasks, ui);
        } else if (normalized.equalsIgnoreCase("tag") || normalized.startsWith("tag ")) {
            handleTag(normalized, tasks, ui, storage);
        } else if (normalized.equalsIgnoreCase("organise") || normalized.startsWith("organise ")) {
            handleOrganise(normalized, tasks, ui);
        } else if (normalized.toLowerCase().startsWith("help")) {
            getHelp(ui);
        } else {
            throw new ZiqException("Unknown command. Enter 'help' for a list of commands.");
        }

        return false;
    }

    /**
     * Handles mark and unmark commands.
     *
     * @param input the user's input command
     * @param tasks the task list to modify
     * @param ui the UI handler for output
     * @param storage the storage handler for saving tasks
     * @param isMark true to mark as done, false to unmark
     * @throws ZiqException if the task index is invalid
     */
    private static void handleMark(String input, TaskList tasks, Ui ui, Storage storage, boolean isMark)
            throws ZiqException {
        String cmd = isMark ? "mark" : "unmark";
        String[] parts = input.split(" ", 2);
        if (parts.length < 2 || parts[1].trim().isEmpty()) {
            throw new ZiqException("task number is missing."
                    + " enter 'list' to see task numbers.");
        }
        try {
            int taskNumber = Integer.parseInt(parts[1].trim());
            int index = taskNumber - DISPLAY_INDEX_OFFSET;
            if (index < 0 || taskNumber < 1) {
                throw new ZiqException("task number must be at least 1."
                        + " enter 'list' to see task numbers.");
            }
            Task task = tasks.get(index);
            boolean previousStatus = task.getStatus().equals("✅");
            boolean alreadyInDesiredState = (isMark && previousStatus) || (!isMark && !previousStatus);

            if (alreadyInDesiredState) {
                if (isMark) {
                    ui.printLine("this task has been marked!");
                } else {
                    ui.printLine("this task has been unmarked!");
                }
                ui.printLine("  " + task);
                return;
            }

            if (isMark) {
                task.markAsDone();
            } else {
                task.unmark();
            }
            try {
                storage.save(tasks.getTaskList());
                if (isMark) {
                    ui.printLine("task marked as done:");
                } else {
                    ui.printLine("task marked as not done:");
                }
                ui.printLine("  " + task);
            } catch (ZiqException e) {
                // Rollback: restore previous status if save failed
                if (previousStatus) {
                    task.markAsDone();
                } else {
                    task.unmark();
                }
                throw new ZiqException("Task status was changed but could not be saved: " + e.getMessage());
            }
        } catch (IndexOutOfBoundsException e) {
            throw new ZiqException("invalid task number."
                    + "enter 'list' to see task numbers.");
        } catch (NumberFormatException e) {
            throw new ZiqException("task number must be a number."
                    + " enter 'list' to see task numbers.");
        }
    }

    /**
     * Handles the todo command to add a new todo task.
     *
     * @param input the user's input command
     * @param tasks the task list to modify
     * @param ui the UI handler for output
     * @param storage the storage handler for saving tasks
     * @throws ZiqException if the description is empty
     */
    private static void handleTodo(String input, TaskList tasks, Ui ui, Storage storage) throws ZiqException {
        if (input.length() <= COMMAND_TODO_PREFIX_LENGTH) {
            throw new ZiqException("description of task cannot be empty.");
        }
        String description = input.substring(COMMAND_TODO_PREFIX_LENGTH).trim();
        if (description.isEmpty()) {
            throw new ZiqException("description of task cannot be empty.");
        }
        Task t = new Todo(description);
        addTaskAndSave(t, tasks, storage, ui);
    }

    /**
     * Handles the deadline command to add a new deadline task.
     *
     * @param input the user's input command
     * @param tasks the task list to modify
     * @param ui the UI handler for output
     * @param storage the storage handler for saving tasks
     * @throws ZiqException if the format is invalid or the date cannot be parsed
     */
    private static void handleDeadline(String input, TaskList tasks, Ui ui, Storage storage) throws ZiqException {
        if (!input.contains(" /by ")) {
            throw new ZiqException("deadline must have '/by' with date. e.g."
                    + "deadline <description> /by DDMMYYYY [HHmm] (e.g. deadline submit report /by 22022022 1200)");
        }
        String commandBody = input.substring(COMMAND_DEADLINE_PREFIX_LENGTH).trim();
        String[] parts = commandBody.split(" /by ", -1);
        if (parts.length != 2) {
            throw new ZiqException("deadline can only one '/by'. e.g."
                    + "deadline <description> /by DDMMYYYY [HHmm] (e.g. deadline submit report /by 22022022 1200)");
        }
        String description = parts[0].trim();
        String dateTimeStr = parts[1].trim();
        if (description.isEmpty()) {
            throw new ZiqException("description of deadline cannot be empty. e.g."
                    + "deadline <description> /by DDMMYYYY [HHmm]");
        }
        if (dateTimeStr.isEmpty()) {
            throw new ZiqException("deadline date cannot be empty. e.g."
                    + "deadline <description> /by DDMMYYYY [HHmm] (e.g. /by 22022022 1200)");
        }
        try {
            LocalDateTime deadlineTime;
            boolean hasTime;
            String[] dateTimeParts = dateTimeStr.split(" ", 2);
            if (dateTimeParts.length == 2 && !dateTimeParts[1].trim().isEmpty()) {
                // Has time component
                deadlineTime = LocalDateTime.parse(dateTimeStr, DEADLINE_INPUT_FORMAT);
                hasTime = true;
            } else {
                // Date only - set time to start of day (00:00)
                LocalDate date = LocalDate.parse(dateTimeParts[0].trim(), DATE_ONLY_FORMAT);
                deadlineTime = date.atTime(0, 0);
                hasTime = false;
            }
            Task task = new Deadline(description, deadlineTime, hasTime);
            addTaskAndSave(task, tasks, storage, ui);
        } catch (DateTimeParseException e) {
            throw new ZiqException("invalid date for deadline. use DDMMYYYY [HHmm]. "
                    + "(e.g. 22022022 1200 or 22022022). dates like Feb 30 are not allowed.");
        }
    }

    /**
     * Handles the event command to add a new event task.
     *
     * @param input the user's input command
     * @param tasks the task list to modify
     * @param ui the UI handler for output
     * @param storage the storage handler for saving tasks
     * @throws ZiqException if the format is invalid or the dates cannot be parsed
     */
    private static void handleEvent(String input, TaskList tasks, Ui ui, Storage storage) throws ZiqException {
        if (!input.contains(" /from ") || !input.contains(" /to ")) {
            throw new ZiqException("event must include '/from' and '/to' with date and time. e.g."
                    + "event <description> /from DDMMYYYY HHmm /to DDMMYYYY HHmm "
                    + "(e.g. event meeting /from 22022022 1200 /to 22022022 1400)");
        }
        String commandBody = input.substring(COMMAND_EVENT_PREFIX_LENGTH).trim();
        String[] parts = commandBody.split(" /from | /to ", -1);
        if (parts.length != 3) {
            throw new ZiqException("event can only one '/from' and one '/to'. e.g."
                    + "event <description> /from DDMMYYYY HHmm /to DDMMYYYY HHmm");
        }
        String description = parts[0].trim();
        String fromStr = parts[1].trim();
        String toStr = parts[2].trim();
        if (description.isEmpty()) {
            throw new ZiqException("description of event cannot be empty. e.g."
                    + "event <description> /from DDMMYYYY HHmm /to DDMMYYYY HHmm");
        }
        if (fromStr.isEmpty() || toStr.isEmpty()) {
            throw new ZiqException("event must have both /from and /to dates. e.g."
                    + "event <description> /from DDMMYYYY HHmm /to DDMMYYYY HHmm");
        }
        try {
            LocalDateTime startTime = LocalDateTime.parse(fromStr, INPUT_FORMAT);
            LocalDateTime endTime = LocalDateTime.parse(toStr, INPUT_FORMAT);
            if (!startTime.isBefore(endTime)) {
                throw new ZiqException("event end time must be after start time.");
            }
            Task task = new Event(description, startTime, endTime);
            addTaskAndSave(task, tasks, storage, ui);
        } catch (DateTimeParseException e) {
            throw new ZiqException("invalid date for event. use DDMMYYYY HHmm. "
                    + "dates like Feb 30 are not allowed.");
        }
    }

    /**
     * Handles the delete command to remove a task.
     *
     * @param input the user's input command
     * @param tasks the task list to modify
     * @param ui the UI handler for output
     * @param storage the storage handler for saving tasks
     * @throws ZiqException if the task index is invalid
     */
    private static void handleDelete(String input, TaskList tasks, Ui ui, Storage storage) throws ZiqException {
        String taskNumberString = input.length() > COMMAND_DELETE_PREFIX_LENGTH
                ? input.substring(COMMAND_DELETE_PREFIX_LENGTH).trim()
                : "";
        if (taskNumberString.isEmpty()) {
            throw new ZiqException("task number is missing."
                    + " enter 'list' to see task numbers.");
        }
        try {
            int taskNumber = Integer.parseInt(taskNumberString);
            int index = taskNumber - DISPLAY_INDEX_OFFSET;
            if (index < 0 || taskNumber < 1) {
                throw new ZiqException("task number must be at least 1."
                        + " enter 'list' to see task numbers.");
            }
            Task removedTask = tasks.delete(index);
            try {
                storage.save(tasks.getTaskList());
                ui.printLine("task removed:");
                ui.printLine("  " + removedTask);
                ui.printLine("now you have " + tasks.size() + " task(s) in the list.");
            } catch (ZiqException e) {
                // Rollback: re-add the task if save failed
                tasks.add(removedTask);
                throw new ZiqException("task was deleted but could not be saved: " + e.getMessage());
            }
        } catch (NumberFormatException e) {
            throw new ZiqException("task number must be a number. "
                    + "enter 'list' to see task numbers.");
        } catch (IndexOutOfBoundsException e) {
            throw new ZiqException("invalid task number. "
                    + "enter 'list' to see task numbers.");
        }
    }

    /**
     * Handles the find command to list tasks whose description contains the given keyword.
     *
     * @param input the user's input command (e.g. "find book")
     * @param tasks the task list to search
     */
    private static void handleFind(String input, TaskList tasks, Ui ui) {
        if (input.length() <= COMMAND_FIND_PREFIX_LENGTH) {
            printTaskList(tasks, ui);
            return;
        }
        String keyword = input.substring(COMMAND_FIND_PREFIX_LENGTH).trim().toLowerCase();
        printMatchingTasks(tasks, keyword, ui);
    }

    /**
     * Handles the schedule command to view tasks on a specific date.
     * Supports partial dates: missing year/month/day defaults to current year/month/day.
     *
     * @param input the user's input (e.g. "schedule 08022026" or "schedule 22" or "schedule 2202")
     * @param tasks the task list to search
     * @param ui the UI handler for output
     * @throws ZiqException if the date format is invalid
     */
    private static void handleSchedule(String input, TaskList tasks, Ui ui) throws ZiqException {
        if (input.length() <= COMMAND_SCHEDULE_PREFIX_LENGTH) {
            throw new ZiqException("Schedule needs a date. Correct format: schedule DDMMYYYY "
                    + "(e.g. schedule 22022022 or schedule 22)");
        }
        String dateStr = input.substring(COMMAND_SCHEDULE_PREFIX_LENGTH).trim();
        if (dateStr.isEmpty()) {
            throw new ZiqException("Schedule date cannot be empty. Correct format: schedule DDMMYYYY "
                    + "(e.g. schedule 22022022 or schedule 22)");
        }
        try {
            LocalDate date = parsePartialDate(dateStr);
            ArrayList<Task> onDate = tasks.getTasksOnDate(date);
            ui.printLine("schedule for " + date.format(DateTimeFormatter.ofPattern("MMM dd yyyy")) + ":");
            if (onDate.isEmpty()) {
                ui.printLine("  (no tasks on this date)");
            } else {
                for (int i = 0; i < onDate.size(); i++) {
                    ui.printLine((i + DISPLAY_INDEX_OFFSET) + ". " + onDate.get(i));
                }
            }
        } catch (DateTimeParseException | NumberFormatException e) {
            throw new ZiqException("Invalid date for schedule. Use DD, DDMM, or DDMMYYYY "
                    + "(e.g. schedule 22, schedule 2202, or schedule 22022022). "
                    + "Dates like Feb 30 are not allowed.");
        }
    }

    /**
     * Handles the tag command to add a tag to a task.
     *
     * @param input the user's input command (e.g. "tag 1 meeting")
     * @param tasks the task list to modify
     * @param ui the UI handler for output
     * @param storage the storage handler for saving tasks
     * @throws ZiqException if the task index is invalid
     */
    private static void handleTag(String input, TaskList tasks, Ui ui, Storage storage) throws ZiqException {
        String[] parts = input.split(" ", 3);
        if (parts.length < 3 || parts[2].trim().isEmpty()) {
            throw new ZiqException("tag command needs task number and tag. e.g."
                    + "(e.g. tag 1 meeting)");
        }
        try {
            int taskNumber = Integer.parseInt(parts[1].trim());
            int index = taskNumber - DISPLAY_INDEX_OFFSET;
            if (index < 0 || taskNumber < 1) {
                throw new ZiqException("task number must be at least 1. e.g."
                        + " enter 'list' to see task numbers.");
            }
            Task task = tasks.get(index);
            String tag = parts[2].trim();
            task.setTag(tag);
            try {
                storage.save(tasks.getTaskList());
                ui.printLine("tag added to task:");
                ui.printLine("  " + task);
            } catch (ZiqException e) {
                // Rollback: remove tag if save failed
                task.setTag(null);
                throw new ZiqException("tag was added but could not be saved: " + e.getMessage());
            }
        } catch (IndexOutOfBoundsException e) {
            throw new ZiqException("invalid task number. e.g."
                    + " enter 'list' to see task numbers.");
        } catch (NumberFormatException e) {
            throw new ZiqException("task number must be a number. e.g."
                    + " enter 'list' to see task numbers.");
        }
    }

    /**
     * Parses a partial date string, filling in missing parts with current date values.
     * Supports formats: DD (day only), DDMM (day+month), DDMMYYYY (full date).
     *
     * @param dateStr the date string to parse (no slashes)
     * @return a LocalDate with missing parts filled from current date
     * @throws DateTimeParseException if the date format is invalid
     * @throws NumberFormatException if the date parts are not valid numbers
     */
    private static LocalDate parsePartialDate(String dateStr) throws DateTimeParseException, NumberFormatException {
        LocalDate now = LocalDate.now();
        String digits = dateStr.replaceAll("\\s", "");
        int len = digits.length();

        if (len == 2) {
            // DD only - use current month and year
            int day = Integer.parseInt(digits.substring(0, 2));
            return LocalDate.of(now.getYear(), now.getMonth(), day);
        } else if (len == 4) {
            // DDMM - use current year
            int day = Integer.parseInt(digits.substring(0, 2));
            int month = Integer.parseInt(digits.substring(2, 4));
            return LocalDate.of(now.getYear(), month, day);
        } else if (len == 8) {
            // DDMMYYYY
            return LocalDate.parse(digits, DATE_ONLY_FORMAT);
        } else {
            throw new DateTimeParseException("Invalid date format", dateStr, 0);
        }
    }

    /**
     * Handles the organise command to organize tasks by tag or deadline.
     *
     * @param input the user's input command (e.g. "organise tag" or "organise deadline")
     * @param tasks the task list to organize
     * @param ui the UI handler for output
     * @throws ZiqException if the organize type is invalid
     */
    private static void handleOrganise(String input, TaskList tasks, Ui ui) throws ZiqException {
        if (input.length() <= COMMAND_ORGANISE_PREFIX_LENGTH) {
            throw new ZiqException("organise needs to know if it's by tag or deadline.");
        }
        String type = input.substring(COMMAND_ORGANISE_PREFIX_LENGTH).trim().toLowerCase();
        if (type.isEmpty()) {
            throw new ZiqException("organise must have a filter of either tag or deadline");
        }
        if (type.equals("tag")) {
            printTasksOrganisedByTag(tasks, ui);
        } else if (type.equals("deadline")) {
            printTasksOrganisedByDeadline(tasks, ui);
        } else {
            throw new ZiqException("invalid organise type. enter 'organise tag' or 'organise deadline'");
        }
    }

    /**
     * Prints tasks organized by tag, grouping tasks with the same tag together.
     *
     * @param tasks the task list to organize
     * @param ui the UI handler for output
     */
    private static void printTasksOrganisedByTag(TaskList tasks, Ui ui) {
        if (tasks.isEmpty()) {
            ui.printLine("you don't have anything on your list right now!");
            return;
        }
        ArrayList<Task> taskList = tasks.getTaskList();
        // Group tasks by tag
        Map<String, ArrayList<Task>> tagGroups = new HashMap<>();
        ArrayList<Task> untaggedTasks = new ArrayList<>();

        for (Task task : taskList) {
            String tag = task.getTag();
            if (tag == null || tag.isEmpty()) {
                untaggedTasks.add(task);
            } else {
                tagGroups.computeIfAbsent(tag, k -> new ArrayList<>()).add(task);
            }
        }

        ui.printLine("tasks organized by tag:");
        int displayNumber = DISPLAY_INDEX_OFFSET;

        // Print tagged tasks grouped by tag
        for (Map.Entry<String, ArrayList<Task>> entry : tagGroups.entrySet()) {
            String tag = entry.getKey();
            ArrayList<Task> taggedTasks = entry.getValue();
            ui.printLine("");
            ui.printLine("[" + tag + "]:");
            for (Task task : taggedTasks) {
                ui.printLine(displayNumber + ". " + task);
                displayNumber++;
            }
        }

        // Print untagged tasks
        if (!untaggedTasks.isEmpty()) {
            ui.printLine("");
            ui.printLine("[untagged]:");
            for (Task task : untaggedTasks) {
                ui.printLine(displayNumber + ". " + task);
                displayNumber++;
            }
        }
    }

    /**
     * Prints tasks organized by deadline, sorting deadlines first, then events, then todos.
     *
     * @param tasks the task list to organize
     * @param ui the UI handler for output
     */
    private static void printTasksOrganisedByDeadline(TaskList tasks, Ui ui) {
        if (tasks.isEmpty()) {
            ui.printLine("you don't have anything on your list right now!");
            return;
        }
        ArrayList<Task> taskList = tasks.getTaskList();
        // Separate tasks by type
        ArrayList<Deadline> deadlines = new ArrayList<>();
        ArrayList<Event> events = new ArrayList<>();
        ArrayList<Task> todos = new ArrayList<>();

        for (Task task : taskList) {
            if (task instanceof Deadline) {
                deadlines.add((Deadline) task);
            } else if (task instanceof Event) {
                events.add((Event) task);
            } else {
                todos.add(task);
            }
        }

        // Sort deadlines by due date
        deadlines.sort(Comparator.comparing(Deadline::by));

        // Sort events by start date
        events.sort(Comparator.comparing(Event::from));

        ui.printLine("tasks organized by deadline:");
        int displayNumber = DISPLAY_INDEX_OFFSET;

        // Print deadlines
        if (!deadlines.isEmpty()) {
            ui.printLine("");
            ui.printLine("deadlines:");
            for (Deadline deadline : deadlines) {
                ui.printLine(displayNumber + ". " + deadline);
                displayNumber++;
            }
        }

        // Print events
        if (!events.isEmpty()) {
            ui.printLine("");
            ui.printLine("events:");
            for (Event event : events) {
                ui.printLine(displayNumber + ". " + event);
                displayNumber++;
            }
        }

        // Print todos
        if (!todos.isEmpty()) {
            ui.printLine("");
            ui.printLine("todos:");
            for (Task task : todos) {
                ui.printLine(displayNumber + ". " + task);
                displayNumber++;
            }
        }
    }

    /**
     * Prints all tasks in the task list.
     *
     * @param tasks the task list to print
     * @param ui the UI handler for output
     */
    private static void printTaskList(TaskList tasks, Ui ui) {
        if (tasks.isEmpty()) {
            ui.printLine("you don't have anything on your list right now!");
            return;
        }
        ui.printLine("here is your to-do list!");
        for (int i = 0; i < tasks.size(); i++) {
            int displayNumber = i + DISPLAY_INDEX_OFFSET;
            ui.printLine(displayNumber + ". " + tasks.get(i));
        }
    }

    /**
     * Prints tasks whose description contains the given keyword.
     *
     * @param tasks the task list to search
     * @param keyword the keyword to search for (case-insensitive)
     * @param ui the UI handler for output
     */
    private static void printMatchingTasks(TaskList tasks, String keyword, Ui ui) {
        int matchCount = 0;
        for (int i = 0; i < tasks.size(); i++) {
            Task task = tasks.get(i);
            if (task.description().toLowerCase().contains(keyword)) {
                matchCount++;
            }
        }
        if (matchCount == 0) {
            ui.printLine("no matches found!");
            return;
        }
        ui.printLine("here are the matching tasks in your list:");
        int displayCount = 0;
        for (int i = 0; i < tasks.size(); i++) {
            Task task = tasks.get(i);
            if (task.description().toLowerCase().contains(keyword)) {
                displayCount++;
                ui.printLine(displayCount + ". " + task);
            }
        }
    }

    /**
     * Adds a task to the list, saves to storage, and prints confirmation.
     * Rejects duplicate tasks (same description and type-specific details).
     * If save fails, the task is removed from the list to maintain consistency.
     *
     * @param task the task to add
     * @param tasks the task list to modify
     * @param storage the storage handler for saving
     * @param ui the UI handler for output
     * @throws ZiqException if a task with the same details already exists or if save fails
     */
    private static void addTaskAndSave(Task task, TaskList tasks, Storage storage, Ui ui) throws ZiqException {
        if (tasks.containsDuplicateOf(task)) {
            throw new ZiqException("a task with the same details already exists in the list. "
                    + "use a different description or date.");
        }
        tasks.add(task);
        try {
            storage.save(tasks.getTaskList());
            ui.printLine("task added:");
            ui.printLine("  " + task);
            ui.printLine("now you have " + tasks.size() + " task(s) in the list.");
        } catch (ZiqException e) {
            // Rollback: remove the task if save failed
            tasks.getTaskList().remove(task);
            throw new ZiqException("task was added but could not be saved: " + e.getMessage());
        }
    }

    /**
     * Handles the clear command to remove all tasks from the list.
     *
     * @param tasks the task list to clear
     * @param ui the UI handler for output
     * @param storage the storage handler for saving tasks
     * @throws ZiqException if there is an error saving after clearing
     */
    private static void handleClear(TaskList tasks, Ui ui, Storage storage) throws ZiqException {
        int count = tasks.size();
        ArrayList<Task> backup = new ArrayList<>(tasks.getTaskList());
        tasks.clear();
        try {
            storage.save(tasks.getTaskList());
            ui.printLine("all tasks cleared! (" + count + " task(s) removed)");
        } catch (ZiqException e) {
            // Rollback: restore tasks if save failed
            tasks.getTaskList().addAll(backup);
            throw new ZiqException("tasks were cleared but could not be saved: " + e.getMessage());
        }
    }

    /**
     * Displays a list of available commands to the user.
     *
     * @param ui the UI handler for output
     */
    private static void getHelp(Ui ui) {
        ui.printLine("here are the commands available:");
        ui.printLine("");
        ui.printLine("todo <description> - add a todo task");
        ui.printLine("");
        ui.printLine("deadline <description> /by DDMMYYYY [HHmm] - add a deadline task, time is optional");
        ui.printLine("");
        ui.printLine("event <description> /from DDMMYYYY HHmm /to DDMMYYYY HHmm - add an event task");
        ui.printLine("");
        ui.printLine("mark <index> - mark a task as done");
        ui.printLine("");
        ui.printLine("unmark <index> - mark a task as not done");
        ui.printLine("");
        ui.printLine("delete <index> - delete a task");
        ui.printLine("");
        ui.printLine("find <keyword> - find tasks by keyword");
        ui.printLine("");
        ui.printLine("schedule DDMMYYYY - view tasks on a specific date (or DD, DDMM for partial)");
        ui.printLine("");
        ui.printLine("tag <index> <tag> - add a tag to a task");
        ui.printLine("");
        ui.printLine("organise tag - organize tasks by tag");
        ui.printLine("");
        ui.printLine("organise deadline - organize tasks by deadline");
        ui.printLine("");
        ui.printLine("clear - remove all tasks");
        ui.printLine("");
        ui.printLine("help - display this list of commands");
        ui.printLine("");
        ui.printLine("bye - terminate Ziq");
    }
}


