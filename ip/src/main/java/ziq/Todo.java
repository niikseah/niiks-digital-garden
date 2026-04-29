package ziq;

/**
 * Represents a todo task without any date/time.
 */
public class Todo extends Task {
    /**
     * Constructs a new Todo task with the given description.
     *
     * @param description the description of the todo task
     */
    public Todo(String description) {
        super(description);
    }

    /**
     * Returns a string representation of this todo task.
     *
     * @return a string in the format "[T][status] description [#tag]"
     */
    @Override
    public String toString() {
        return "[T]" + super.toString();
    }
}

