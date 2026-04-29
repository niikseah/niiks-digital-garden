package ziq;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.LocalDateTime;

import org.junit.jupiter.api.Test;

public class DeadlineTest {

    @Test
    public void deadlineHasCorrectDescription() {
        LocalDateTime by = LocalDateTime.of(2022, 2, 22, 12, 0);
        Deadline d = new Deadline("submit report", by, true);
        assertEquals("submit report", d.description());
    }

    @Test
    public void deadlineHasCorrectByTime() {
        LocalDateTime by = LocalDateTime.of(2022, 2, 22, 12, 0);
        Deadline d = new Deadline("submit report", by, true);
        assertEquals(by, d.by());
    }

    @Test
    public void deadlineToString_showsDoneWhenMarked() {
        LocalDateTime by = LocalDateTime.of(2022, 2, 22, 12, 0);
        Deadline d = new Deadline("submit report", by, true);
        assertTrue(d.toString().contains("[D]"));
        assertTrue(d.toString().contains("[ ]"));
        assertTrue(d.toString().contains("submit report"));
        d.markAsDone();
        assertTrue(d.toString().contains("[✅]"));
    }

    @Test
    public void deadlineToString_includesFormattedDate() {
        LocalDateTime by = LocalDateTime.of(2022, 2, 22, 12, 0);
        Deadline d = new Deadline("submit report", by, true);
        String output = d.toString();
        assertTrue(output.contains("by "));
        assertTrue(output.contains("Feb"));
        assertTrue(output.contains("2022"));
    }

    @Test
    public void deadlineHasSameDetailsAs_sameDescriptionAndTime() {
        LocalDateTime by = LocalDateTime.of(2022, 2, 22, 12, 0);
        Deadline d1 = new Deadline("submit report", by, true);
        Deadline d2 = new Deadline("submit report", by, true);
        assertTrue(d1.hasSameDetailsAs(d2));
    }

    @Test
    public void deadlineHasSameDetailsAs_differentDescription() {
        LocalDateTime by = LocalDateTime.of(2022, 2, 22, 12, 0);
        Deadline d1 = new Deadline("submit report", by, true);
        Deadline d2 = new Deadline("submit assignment", by, true);
        assertFalse(d1.hasSameDetailsAs(d2));
    }

    @Test
    public void deadlineHasSameDetailsAs_differentTime() {
        LocalDateTime by1 = LocalDateTime.of(2022, 2, 22, 12, 0);
        LocalDateTime by2 = LocalDateTime.of(2022, 2, 22, 14, 0);
        Deadline d1 = new Deadline("submit report", by1, true);
        Deadline d2 = new Deadline("submit report", by2, true);
        assertFalse(d1.hasSameDetailsAs(d2));
    }

    @Test
    public void deadlineHasSameDetailsAs_differentTaskType() {
        LocalDateTime by = LocalDateTime.of(2022, 2, 22, 12, 0);
        Deadline d = new Deadline("submit report", by, true);
        Todo t = new Todo("submit report");
        assertFalse(d.hasSameDetailsAs(t));
    }

    @Test
    public void deadlineUnmark_clearsDoneStatus() {
        LocalDateTime by = LocalDateTime.of(2022, 2, 22, 12, 0);
        Deadline d = new Deadline("submit report", by, true);
        d.markAsDone();
        assertTrue(d.getStatus().equals("✅"));
        d.unmark();
        assertTrue(d.getStatus().equals(" "));
    }
}

