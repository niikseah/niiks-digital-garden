package ziq;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

public class TaskTest {

    @Test
    public void taskHasCorrectDescription() {
        Task t = new Todo("read book");
        assertEquals("read book", t.description());
    }

    @Test
    public void taskStartsAsNotDone() {
        Task t = new Todo("read book");
        assertEquals(" ", t.getStatus());
        assertFalse(t.toString().contains("[✅]"));
    }

    @Test
    public void taskMarkAsDone_changesStatus() {
        Task t = new Todo("read book");
        t.markAsDone();
        assertEquals("✅", t.getStatus());
        assertTrue(t.toString().contains("[✅]"));
    }

    @Test
    public void taskUnmark_clearsDoneStatus() {
        Task t = new Todo("read book");
        t.markAsDone();
        t.unmark();
        assertEquals(" ", t.getStatus());
    }

    @Test
    public void taskHasSameDetailsAs_sameDescription() {
        Task t1 = new Todo("read book");
        Task t2 = new Todo("read book");
        assertTrue(t1.hasSameDetailsAs(t2));
    }

    @Test
    public void taskHasSameDetailsAs_differentDescription() {
        Task t1 = new Todo("read book");
        Task t2 = new Todo("write book");
        assertFalse(t1.hasSameDetailsAs(t2));
    }

    @Test
    public void taskHasSameDetailsAs_nullReturnsFalse() {
        Task t = new Todo("read book");
        assertFalse(t.hasSameDetailsAs(null));
    }

    @Test
    public void taskToString_includesStatusAndDescription() {
        Task t = new Todo("read book");
        String output = t.toString();
        assertTrue(output.contains("[ ]"));
        assertTrue(output.contains("read book"));
    }
}

