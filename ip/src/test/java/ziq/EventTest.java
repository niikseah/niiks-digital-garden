package ziq;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.LocalDateTime;

import org.junit.jupiter.api.Test;

public class EventTest {

    @Test
    public void eventHasCorrectDescription() {
        LocalDateTime from = LocalDateTime.of(2022, 2, 22, 12, 0);
        LocalDateTime to = LocalDateTime.of(2022, 2, 22, 14, 0);
        Event e = new Event("meeting", from, to);
        assertEquals("meeting", e.description());
    }

    @Test
    public void eventHasCorrectFromAndTo() {
        LocalDateTime from = LocalDateTime.of(2022, 2, 22, 12, 0);
        LocalDateTime to = LocalDateTime.of(2022, 2, 22, 14, 0);
        Event e = new Event("meeting", from, to);
        assertEquals(from, e.from());
        assertEquals(to, e.to());
    }

    @Test
    public void eventToString_showsDoneWhenMarked() {
        LocalDateTime from = LocalDateTime.of(2022, 2, 22, 12, 0);
        LocalDateTime to = LocalDateTime.of(2022, 2, 22, 14, 0);
        Event e = new Event("meeting", from, to);
        assertTrue(e.toString().contains("[E]"));
        assertTrue(e.toString().contains("[ ]"));
        assertTrue(e.toString().contains("meeting"));
        e.markAsDone();
        assertTrue(e.toString().contains("[✅]"));
    }

    @Test
    public void eventToString_includesFormattedDates() {
        LocalDateTime from = LocalDateTime.of(2022, 2, 22, 12, 0);
        LocalDateTime to = LocalDateTime.of(2022, 2, 22, 14, 0);
        Event e = new Event("meeting", from, to);
        String output = e.toString();
        assertTrue(output.contains("from:"));
        assertTrue(output.contains("to:"));
        assertTrue(output.contains("Feb"));
    }

    @Test
    public void eventHasSameDetailsAs_sameDescriptionAndTimes() {
        LocalDateTime from = LocalDateTime.of(2022, 2, 22, 12, 0);
        LocalDateTime to = LocalDateTime.of(2022, 2, 22, 14, 0);
        Event e1 = new Event("meeting", from, to);
        Event e2 = new Event("meeting", from, to);
        assertTrue(e1.hasSameDetailsAs(e2));
    }

    @Test
    public void eventHasSameDetailsAs_differentDescription() {
        LocalDateTime from = LocalDateTime.of(2022, 2, 22, 12, 0);
        LocalDateTime to = LocalDateTime.of(2022, 2, 22, 14, 0);
        Event e1 = new Event("meeting", from, to);
        Event e2 = new Event("conference", from, to);
        assertFalse(e1.hasSameDetailsAs(e2));
    }

    @Test
    public void eventHasSameDetailsAs_differentFromTime() {
        LocalDateTime from1 = LocalDateTime.of(2022, 2, 22, 12, 0);
        LocalDateTime from2 = LocalDateTime.of(2022, 2, 22, 13, 0);
        LocalDateTime to = LocalDateTime.of(2022, 2, 22, 14, 0);
        Event e1 = new Event("meeting", from1, to);
        Event e2 = new Event("meeting", from2, to);
        assertFalse(e1.hasSameDetailsAs(e2));
    }

    @Test
    public void eventHasSameDetailsAs_differentToTime() {
        LocalDateTime from = LocalDateTime.of(2022, 2, 22, 12, 0);
        LocalDateTime to1 = LocalDateTime.of(2022, 2, 22, 14, 0);
        LocalDateTime to2 = LocalDateTime.of(2022, 2, 22, 15, 0);
        Event e1 = new Event("meeting", from, to1);
        Event e2 = new Event("meeting", from, to2);
        assertFalse(e1.hasSameDetailsAs(e2));
    }

    @Test
    public void eventHasSameDetailsAs_differentTaskType() {
        LocalDateTime from = LocalDateTime.of(2022, 2, 22, 12, 0);
        LocalDateTime to = LocalDateTime.of(2022, 2, 22, 14, 0);
        Event e = new Event("meeting", from, to);
        Todo t = new Todo("meeting");
        assertFalse(e.hasSameDetailsAs(t));
    }

    @Test
    public void eventUnmark_clearsDoneStatus() {
        LocalDateTime from = LocalDateTime.of(2022, 2, 22, 12, 0);
        LocalDateTime to = LocalDateTime.of(2022, 2, 22, 14, 0);
        Event e = new Event("meeting", from, to);
        e.markAsDone();
        assertTrue(e.getStatus().equals("✅"));
        e.unmark();
        assertTrue(e.getStatus().equals(" "));
    }
}

