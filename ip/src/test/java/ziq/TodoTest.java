package ziq;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

public class TodoTest {

    @Test
    public void todoHasCorrectDescription() {
        Todo t = new Todo("read book");
        assertEquals("read book", t.description());
    }

    @Test
    public void todoToString_showsDoneWhenMarked() {
        Todo t = new Todo("read book");
        assertEquals("[T][ ] read book", t.toString());
        t.markAsDone();
        assertEquals("[T][✅] read book", t.toString());
    }

    @Test
    public void todoStartsAsNotDone() {
        Todo t = new Todo("read book");
        assertEquals(" ", t.getStatus());
        assertFalse(t.toString().contains("[✅]"));
    }

    @Test
    public void todoUnmark_clearsDoneStatus() {
        Todo t = new Todo("read book");
        t.markAsDone();
        assertTrue(t.getStatus().equals("✅"));
        t.unmark();
        assertTrue(t.getStatus().equals(" "));
    }

    @Test
    public void todoHasSameDetailsAs_sameDescription() {
        Todo t1 = new Todo("read book");
        Todo t2 = new Todo("read book");
        assertTrue(t1.hasSameDetailsAs(t2));
    }

    @Test
    public void todoHasSameDetailsAs_differentDescription() {
        Todo t1 = new Todo("read book");
        Todo t2 = new Todo("write book");
        assertFalse(t1.hasSameDetailsAs(t2));
    }

    @Test
    public void todoHasSameDetailsAs_differentTaskType() {
        Todo t = new Todo("read book");
        java.time.LocalDateTime by = java.time.LocalDateTime.of(2022, 2, 22, 12, 0);
        Deadline d = new Deadline("read book", by, true);
        assertFalse(t.hasSameDetailsAs(d));
    }

    @Test
    public void todoToString_includesTypeCode() {
        Todo t = new Todo("read book");
        assertTrue(t.toString().contains("[T]"));
    }
}

