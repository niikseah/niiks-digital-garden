package ziq;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

public class TaskTypeTest {

    @Test
    public void todoGetCode_returnsT() {
        assertEquals("T", TaskType.TODO.getCode());
    }

    @Test
    public void deadlineGetCode_returnsD() {
        assertEquals("D", TaskType.DEADLINE.getCode());
    }

    @Test
    public void eventGetCode_returnsE() {
        assertEquals("E", TaskType.EVENT.getCode());
    }

    @Test
    public void findTaskType_validCodeT() throws ZiqException {
        assertEquals(TaskType.TODO, TaskType.findTaskType("T"));
    }

    @Test
    public void findTaskType_validCodeD() throws ZiqException {
        assertEquals(TaskType.DEADLINE, TaskType.findTaskType("D"));
    }

    @Test
    public void findTaskType_validCodeE() throws ZiqException {
        assertEquals(TaskType.EVENT, TaskType.findTaskType("E"));
    }

    @Test
    public void findTaskType_invalidCode_throwsException() {
        assertThrows(ZiqException.class, () -> TaskType.findTaskType("X"));
    }

    @Test
    public void findTaskType_emptyString_throwsException() {
        assertThrows(ZiqException.class, () -> TaskType.findTaskType(""));
    }

    @Test
    public void findTaskType_null_throwsException() {
        assertThrows(ZiqException.class, () -> TaskType.findTaskType(null));
    }
}

