package ziq;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Represents a Deadline task with a due date/time.
 */
public class Deadline extends Task {

    protected LocalDateTime by;
    private boolean hasTime;

    /**
     * Constructs a new Deadline task with the given description and due date/time.
     *
     * @param description the description of the deadline task
     * @param by the due date/time for the deadline
     * @param hasTime true if a time component was specified, false if only date was provided
     */
    public Deadline(String description, LocalDateTime by, boolean hasTime) {
        super(description);
        this.by = by;
        this.hasTime = hasTime;
    }

    /**
     * Returns the due date/time of this deadline.
     *
     * @return the due date/time
     */
    public LocalDateTime by() {
        return this.by;
    }

    /**
     * Returns true if this deadline has the same description and due date/time as the other task.
     *
     * @param other the other task to compare
     * @return true if both are deadlines with the same description and due date/time
     */
    @Override
    public boolean hasSameDetailsAs(Task other) {
        if (!(other instanceof Deadline)) {
            return false;
        }
        Deadline d = (Deadline) other;
        return description.equals(d.description) && by.equals(d.by);
    }

    /**
     * Returns a string representation of this deadline task.
     * If time was not specified, only shows the date.
     *
     * @return a string in the format "[D][status] description (by date/time) [#tag]"
     */
    @Override
    public String toString() {
        String dateTimeStr;
        if (hasTime) {
            dateTimeStr = by.format(Parser.OUTPUT_FORMAT);
        } else {
            dateTimeStr = by.format(DateTimeFormatter.ofPattern("MMM dd yyyy"));
        }
        return "[D]" + super.toString() + " (by " + dateTimeStr + ")";
    }
}

