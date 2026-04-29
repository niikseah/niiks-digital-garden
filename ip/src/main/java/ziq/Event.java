package ziq;

import java.time.LocalDateTime;

/**
 * Represents an Event task with a start and end date/time.
 */
public class Event extends Task {
    protected LocalDateTime from;
    protected LocalDateTime to;

    /**
     * Constructs a new Event task with the given description, start and end date/time.
     *
     * @param description the description of the event
     * @param from the start date/time of the event
     * @param to the end date/time of the event
     */
    public Event(String description, LocalDateTime from, LocalDateTime to) {
        super(description);
        this.from = from;
        this.to = to;
    }

    /**
     * Returns the start date/time of this event.
     *
     * @return the start date/time
     */
    public LocalDateTime from() {
        return this.from;
    }

    /**
     * Returns the end date/time of this event.
     *
     * @return the end date/time
     */
    public LocalDateTime to() {
        return this.to;
    }

    /**
     * Returns true if this event has the same description, start time, and end time as the other task.
     *
     * @param other the other task to compare
     * @return true if both are events with the same description, start time, and end time
     */
    @Override
    public boolean hasSameDetailsAs(Task other) {
        if (!(other instanceof Event)) {
            return false;
        }
        Event e = (Event) other;
        return description.equals(e.description) && from.equals(e.from) && to.equals(e.to);
    }

    /**
     * Returns a string representation of this event task.
     *
     * @return a string in the format "[E][status] description (from: date/time to: date/time) [#tag]"
     */
    @Override
    public String toString() {
        return "[E]" + super.toString()
                + " (from: " + from.format(Parser.OUTPUT_FORMAT)
                + " to: " + to.format(Parser.OUTPUT_FORMAT) + ")";
    }
}

