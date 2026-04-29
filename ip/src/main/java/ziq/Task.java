package ziq;

/**
 * Represents a task with a description and completion status.
 * Base class for different types of tasks (Todo, Deadline, Event).
 */
public class Task {
    protected String description;
    protected boolean isDone;
    protected String tag;

    /**
     * Constructs a new Task with the given description.
     *
     * @param description the description of the task
     */
    public Task(String description) {
        this.description = description;
        this.isDone = false;
        this.tag = null;
    }

    /**
     * Returns the description of this task.
     *
     * @return the task description
     */
    public String description() {
        return this.description;
    }

    /**
     * Returns the completion status as a string ("✅" for done, " " for not done).
     *
     * @return "✅" if task is done, " " otherwise
     */
    public String getStatus() {
        return (isDone ? "✅" : " ");
    }

    /**
     * Marks this task as completed.
     */
    public void markAsDone() {
        this.isDone = true;
    }

    /**
     * Marks this task as not completed.
     */
    public void unmark() {
        this.isDone = false;
    }

    /**
     * Returns the tag of this task, or null if no tag is set.
     *
     * @return the tag, or null if not set
     */
    public String getTag() {
        return tag;
    }

    /**
     * Sets the tag for this task.
     *
     * @param tag the tag to set
     */
    public void setTag(String tag) {
        this.tag = tag;
    }

    /**
     * Returns true if this task has the same logical details as the other (description and type-specific fields).
     * Used to detect duplicate tasks.
     *
     * @param other the other task to compare
     * @return true if details are the same
     */
    public boolean hasSameDetailsAs(Task other) {
        if (other == null) {
            return false;
        }
        // Different types cannot have same details
        if (this.getClass() != other.getClass()) {
            return false;
        }
        return description.equals(other.description);
    }

    /**
     * Returns a string representation of this task.
     *
     * @return a string in the format "[status] description [tag]"
     */
    @Override
    public String toString() {
        String tagStr = (tag != null && !tag.isEmpty()) ? " [" + tag + "]" : "";
        return "[" + getStatus() + "] " + description + tagStr;
    }
}

