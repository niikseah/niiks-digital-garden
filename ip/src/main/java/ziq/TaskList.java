package ziq;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Manages a collection of tasks.
 * Provides methods to add, remove, and retrieve tasks.
 */
public class TaskList {
    private final ArrayList<Task> tasks;

    /**
     * Constructs a TaskList with the given list of tasks.
     *
     * @param tasks the initial list of tasks
     */
    public TaskList(ArrayList<Task> tasks) {
        assert tasks != null : "tasks list must not be null";
        this.tasks = tasks;
    }

    /**
     * Constructs an empty TaskList.
     */
    public TaskList() {
        this.tasks = new ArrayList<>();
    }

    /**
     * Adds one or more tasks to the list.
     *
     * @param t the task(s) to add (varargs)
     */
    public void add(Task... t) {
        for (Task task : t) {
            assert task != null : "task to add must not be null";
            tasks.add(task);
        }
    }

    /**
     * Returns true if the list already contains a task with the same details as the given task.
     *
     * @param task the task to check for duplicate
     * @return true if a duplicate exists
     */
    public boolean containsDuplicateOf(Task task) {
        for (Task existing : tasks) {
            if (existing.hasSameDetailsAs(task)) {
                return true;
            }
        }
        return false;
    }

    /**
     * Clears all tasks from the list.
     */
    public void clear() {
        tasks.clear();
    }

    /**
     * Returns the list of all tasks.
     *
     * @return the list of tasks
     */
    public ArrayList<Task> getTaskList() {
        return this.tasks;
    }

    /**
     * Deletes and returns the task at the specified index.
     *
     * @param index the index of the task to delete (0-based)
     * @return the deleted task
     * @throws ZiqException if the index is invalid
     */
    public Task delete(int index) throws ZiqException {
        if (index < 0 || index >= tasks.size()) {
            throw new ZiqException("task number does not exist. enter 'list' to see valid task numbers");
        }
        assert index >= 0 && index < tasks.size() : "index must be valid at this point";
        return tasks.remove(index);
    }

    /**
     * Returns the task at the specified index.
     *
     * @param index the index of the task to retrieve (0-based)
     * @return the task at the specified index
     * @throws IndexOutOfBoundsException if the index is out of range
     */
    public Task get(int index) {
        if (index < 0 || index >= tasks.size()) {
            throw new IndexOutOfBoundsException("index must be in range [0, size)");
        }
        return tasks.get(index);
    }

    /**
     * Returns the number of tasks in the list.
     *
     * @return the number of tasks
     */
    public int size() {
        return tasks.size();
    }

    /**
     * Returns true if the list contains no tasks.
     *
     * @return true if the list is empty
     */
    public boolean isEmpty() {
        return tasks.isEmpty();
    }

    /**
     * Returns tasks that fall on the given date (deadlines due that day, events that span that day),
     * sorted by time.
     *
     * @param date the date to view the schedule for
     * @return list of tasks on that date, sorted by time
     */
    public ArrayList<Task> getTasksOnDate(LocalDate date) {
        List<Task> onDate = tasks.stream()
                .filter(task -> isTaskOnDate(task, date))
                .sorted(Comparator.comparing(t -> getScheduleTime(t)))
                .collect(Collectors.toList());
        return new ArrayList<>(onDate);
    }

    /**
     * Checks if a task falls on the given date.
     * For deadlines: checks if due date matches.
     * For events: checks if the date falls within the event's time range.
     * For todos: returns false (no date).
     *
     * @param task the task to check
     * @param date the date to check against
     * @return true if the task is on the given date
     */
    private static boolean isTaskOnDate(Task task, LocalDate date) {
        if (task instanceof Deadline) {
            return ((Deadline) task).by().toLocalDate().equals(date);
        }
        if (task instanceof Event) {
            Event e = (Event) task;
            return !date.isBefore(e.from().toLocalDate()) && !date.isAfter(e.to().toLocalDate());
        }
        return false;
    }

    /**
     * Gets the time to use for sorting tasks in the schedule.
     * For deadlines: returns the due date/time.
     * For events: returns the start time.
     * For todos: returns LocalDateTime.MIN (sorted first).
     *
     * @param task the task to get the schedule time for
     * @return the LocalDateTime to use for sorting
     */
    private static LocalDateTime getScheduleTime(Task task) {
        if (task instanceof Deadline) {
            return ((Deadline) task).by();
        }
        if (task instanceof Event) {
            return ((Event) task).from();
        }
        return LocalDateTime.MIN;
    }
}

