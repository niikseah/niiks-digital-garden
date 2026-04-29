package ziq;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class TaskListTest {

    private TaskList taskList;

    @BeforeEach
    public void setUp() {
        taskList = new TaskList();
    }

    @Test
    public void editabilityTest() throws ZiqException {
        taskList.add(new Todo("first"));
        taskList.add(new Todo("second"));
        Task removed = taskList.delete(0);
        assertEquals("first", removed.description());
        assertEquals(1, taskList.size());
    }

    @Test
    public void deleteInvalidIndex() {
        taskList.add(new Todo("only one"));
        assertThrows(ZiqException.class, () -> taskList.delete(5));
    }

    @Test
    public void deleteNegativeIndex_throwsException() {
        taskList.add(new Todo("task"));
        assertThrows(ZiqException.class, () -> taskList.delete(-1));
    }

    @Test
    public void deleteFromEmptyList_throwsException() {
        assertThrows(ZiqException.class, () -> taskList.delete(0));
    }

    @Test
    public void addSingleTask() {
        taskList.add(new Todo("task"));
        assertEquals(1, taskList.size());
        assertEquals("task", taskList.get(0).description());
    }

    @Test
    public void addMultipleTasks() {
        taskList.add(new Todo("task1"), new Todo("task2"), new Todo("task3"));
        assertEquals(3, taskList.size());
        assertEquals("task1", taskList.get(0).description());
        assertEquals("task2", taskList.get(1).description());
        assertEquals("task3", taskList.get(2).description());
    }

    @Test
    public void getTask_validIndex() {
        taskList.add(new Todo("task"));
        Task task = taskList.get(0);
        assertEquals("task", task.description());
    }

    @Test
    public void size_emptyList() {
        assertEquals(0, taskList.size());
    }

    @Test
    public void size_afterAdding() {
        taskList.add(new Todo("task1"));
        assertEquals(1, taskList.size());
        taskList.add(new Todo("task2"));
        assertEquals(2, taskList.size());
    }

    @Test
    public void getTaskList_returnsCorrectList() {
        taskList.add(new Todo("task1"), new Todo("task2"));
        ArrayList<Task> list = taskList.getTaskList();
        assertEquals(2, list.size());
        assertEquals("task1", list.get(0).description());
    }

    @Test
    public void containsDuplicateOf_sameTodo() {
        taskList.add(new Todo("read book"));
        Todo duplicate = new Todo("read book");
        assertTrue(taskList.containsDuplicateOf(duplicate));
    }

    @Test
    public void containsDuplicateOf_differentTodo() {
        taskList.add(new Todo("read book"));
        Todo different = new Todo("write book");
        assertFalse(taskList.containsDuplicateOf(different));
    }

    @Test
    public void containsDuplicateOf_sameDeadline() {
        LocalDateTime by = LocalDateTime.of(2022, 2, 22, 12, 0);
        taskList.add(new Deadline("submit", by, true));
        Deadline duplicate = new Deadline("submit", by, true);
        assertTrue(taskList.containsDuplicateOf(duplicate));
    }

    @Test
    public void containsDuplicateOf_differentDeadlineTime() {
        LocalDateTime by1 = LocalDateTime.of(2022, 2, 22, 12, 0);
        LocalDateTime by2 = LocalDateTime.of(2022, 2, 22, 14, 0);
        taskList.add(new Deadline("submit", by1, true));
        Deadline different = new Deadline("submit", by2, true);
        assertFalse(taskList.containsDuplicateOf(different));
    }

    @Test
    public void containsDuplicateOf_sameEvent() {
        LocalDateTime from = LocalDateTime.of(2022, 2, 22, 12, 0);
        LocalDateTime to = LocalDateTime.of(2022, 2, 22, 14, 0);
        taskList.add(new Event("meeting", from, to));
        Event duplicate = new Event("meeting", from, to);
        assertTrue(taskList.containsDuplicateOf(duplicate));
    }

    @Test
    public void containsDuplicateOf_differentEventTime() {
        LocalDateTime from1 = LocalDateTime.of(2022, 2, 22, 12, 0);
        LocalDateTime from2 = LocalDateTime.of(2022, 2, 22, 13, 0);
        LocalDateTime to = LocalDateTime.of(2022, 2, 22, 14, 0);
        taskList.add(new Event("meeting", from1, to));
        Event different = new Event("meeting", from2, to);
        assertFalse(taskList.containsDuplicateOf(different));
    }

    @Test
    public void getTasksOnDate_deadlineOnDate() {
        LocalDateTime by = LocalDateTime.of(2022, 2, 22, 12, 0);
        taskList.add(new Deadline("submit", by, true));
        LocalDate date = LocalDate.of(2022, 2, 22);
        ArrayList<Task> onDate = taskList.getTasksOnDate(date);
        assertEquals(1, onDate.size());
        assertEquals("submit", onDate.get(0).description());
    }

    @Test
    public void getTasksOnDate_deadlineNotOnDate() {
        LocalDateTime by = LocalDateTime.of(2022, 2, 22, 12, 0);
        taskList.add(new Deadline("submit", by, true));
        LocalDate date = LocalDate.of(2022, 2, 23);
        ArrayList<Task> onDate = taskList.getTasksOnDate(date);
        assertEquals(0, onDate.size());
    }

    @Test
    public void getTasksOnDate_eventOnDate() {
        LocalDateTime from = LocalDateTime.of(2022, 2, 22, 12, 0);
        LocalDateTime to = LocalDateTime.of(2022, 2, 22, 14, 0);
        taskList.add(new Event("meeting", from, to));
        LocalDate date = LocalDate.of(2022, 2, 22);
        ArrayList<Task> onDate = taskList.getTasksOnDate(date);
        assertEquals(1, onDate.size());
    }

    @Test
    public void getTasksOnDate_eventSpansDate() {
        LocalDateTime from = LocalDateTime.of(2022, 2, 20, 12, 0);
        LocalDateTime to = LocalDateTime.of(2022, 2, 24, 14, 0);
        taskList.add(new Event("conference", from, to));
        LocalDate date = LocalDate.of(2022, 2, 22);
        ArrayList<Task> onDate = taskList.getTasksOnDate(date);
        assertEquals(1, onDate.size());
    }

    @Test
    public void getTasksOnDate_eventBeforeDate() {
        LocalDateTime from = LocalDateTime.of(2022, 2, 20, 12, 0);
        LocalDateTime to = LocalDateTime.of(2022, 2, 21, 14, 0);
        taskList.add(new Event("meeting", from, to));
        LocalDate date = LocalDate.of(2022, 2, 22);
        ArrayList<Task> onDate = taskList.getTasksOnDate(date);
        assertEquals(0, onDate.size());
    }

    @Test
    public void getTasksOnDate_todoNotIncluded() {
        taskList.add(new Todo("read book"));
        LocalDate date = LocalDate.of(2022, 2, 22);
        ArrayList<Task> onDate = taskList.getTasksOnDate(date);
        assertEquals(0, onDate.size());
    }

    @Test
    public void getTasksOnDate_multipleTasksSorted() {
        LocalDateTime by1 = LocalDateTime.of(2022, 2, 22, 14, 0);
        LocalDateTime by2 = LocalDateTime.of(2022, 2, 22, 10, 0);
        LocalDateTime from = LocalDateTime.of(2022, 2, 22, 12, 0);
        LocalDateTime to = LocalDateTime.of(2022, 2, 22, 13, 0);
        taskList.add(new Deadline("late", by1, true));
        taskList.add(new Deadline("early", by2, true));
        taskList.add(new Event("middle", from, to));
        LocalDate date = LocalDate.of(2022, 2, 22);
        ArrayList<Task> onDate = taskList.getTasksOnDate(date);
        assertEquals(3, onDate.size());
        assertEquals("early", onDate.get(0).description());
        assertEquals("middle", onDate.get(1).description());
        assertEquals("late", onDate.get(2).description());
    }

    @Test
    public void constructorWithList() {
        ArrayList<Task> initialTasks = new ArrayList<>();
        initialTasks.add(new Todo("task1"));
        initialTasks.add(new Todo("task2"));
        TaskList list = new TaskList(initialTasks);
        assertEquals(2, list.size());
    }
}

