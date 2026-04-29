package ziq;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.time.LocalDateTime;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class ParserTest {

    private TaskList tasks;
    private Ui ui;
    private Storage storage;
    private ByteArrayOutputStream outputStream;

    @BeforeEach
    public void setUp() {
        tasks = new TaskList();
        ui = new Ui();
        storage = new MockStorage();
        outputStream = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outputStream));
    }

    @AfterEach
    public void tearDown() {
        System.setOut(System.out);
    }

    @Test
    public void executeCommand_bye_returnsTrue() throws ZiqException {
        assertTrue(Parser.executeCommand("bye", tasks, ui, storage));
    }

    @Test
    public void executeCommand_list_printsTasks() throws ZiqException {
        tasks.add(new Todo("task1"), new Todo("task2"));
        Parser.executeCommand("list", tasks, ui, storage);
        String output = outputStream.toString();
        assertTrue(output.contains("here is your to-do list!"));
        assertTrue(output.contains("task1"));
        assertTrue(output.contains("task2"));
    }

    @Test
    public void executeCommand_emptyInput_throwsException() {
        assertThrows(ZiqException.class, () -> Parser.executeCommand("   ", tasks, ui, storage));
    }

    @Test
    public void executeCommand_unknownCommand_throwsException() {
        assertThrows(ZiqException.class, () -> Parser.executeCommand("invalid", tasks, ui, storage));
    }

    @Test
    public void executeCommand_todo_addsTask() throws ZiqException {
        Parser.executeCommand("todo read book", tasks, ui, storage);
        assertEquals(1, tasks.size());
        assertEquals("read book", tasks.get(0).description());
    }

    @Test
    public void executeCommand_todoEmptyDescription_throwsException() {
        assertThrows(ZiqException.class, () -> Parser.executeCommand("todo", tasks, ui, storage));
    }

    @Test
    public void executeCommand_todoOnlySpaces_throwsException() {
        assertThrows(ZiqException.class, () -> Parser.executeCommand("todo   ", tasks, ui, storage));
    }

    @Test
    public void executeCommand_todo_normalizesSpaces() throws ZiqException {
        Parser.executeCommand("todo   read   book", tasks, ui, storage);
        assertEquals("read book", tasks.get(0).description());
    }

    @Test
    public void executeCommand_deadline_addsTask() throws ZiqException {
        Parser.executeCommand("deadline submit /by 22022022 1200", tasks, ui, storage);
        assertEquals(1, tasks.size());
        assertTrue(tasks.get(0) instanceof Deadline);
    }

    @Test
    public void executeCommand_deadlineMissingBy_throwsException() {
        assertThrows(ZiqException.class, () -> Parser.executeCommand("deadline submit", tasks, ui, storage));
    }

    @Test
    public void executeCommand_deadlineDuplicateBy_throwsException() {
        assertThrows(ZiqException.class, () -> Parser.executeCommand(
                "deadline submit /by 22022022 1200 /by 23022022 1200", tasks, ui, storage));
    }

    @Test
    public void executeCommand_deadlineInvalidDate_throwsException() {
        assertThrows(ZiqException.class, () -> Parser.executeCommand(
                "deadline submit /by 32012022 1200", tasks, ui, storage));
    }

    @Test
    public void executeCommand_deadlineEmptyDescription_throwsException() {
        assertThrows(ZiqException.class, () -> Parser.executeCommand(
                "deadline /by 22022022 1200", tasks, ui, storage));
    }

    @Test
    public void executeCommand_event_addsTask() throws ZiqException {
        Parser.executeCommand("event meeting /from 22022022 1200 /to 22022022 1400", tasks, ui, storage);
        assertEquals(1, tasks.size());
        assertTrue(tasks.get(0) instanceof Event);
    }

    @Test
    public void executeCommand_eventStartAfterEnd_throwsException() {
        assertThrows(ZiqException.class, () -> Parser.executeCommand(
                "event meeting /from 22022022 1400 /to 22022022 1200", tasks, ui, storage));
    }

    @Test
    public void executeCommand_eventStartEqualsEnd_throwsException() {
        assertThrows(ZiqException.class, () -> Parser.executeCommand(
                "event meeting /from 22022022 1200 /to 22022022 1200", tasks, ui, storage));
    }

    @Test
    public void executeCommand_eventMissingFrom_throwsException() {
        assertThrows(ZiqException.class, () -> Parser.executeCommand(
                "event meeting /to 22022022 1400", tasks, ui, storage));
    }

    @Test
    public void executeCommand_eventDuplicateFrom_throwsException() {
        assertThrows(ZiqException.class, () -> Parser.executeCommand(
                "event meeting /from 22022022 1200 /from 22022022 1300 /to 22022022 1400", tasks, ui, storage));
    }

    @Test
    public void executeCommand_mark_validIndex() throws ZiqException {
        tasks.add(new Todo("task"));
        Parser.executeCommand("mark 1", tasks, ui, storage);
        assertTrue(tasks.get(0).getStatus().equals("✅"));
    }

    @Test
    public void executeCommand_markMissingNumber_throwsException() {
        tasks.add(new Todo("task"));
        assertThrows(ZiqException.class, () -> Parser.executeCommand("mark", tasks, ui, storage));
    }

    @Test
    public void executeCommand_markInvalidIndex_throwsException() {
        tasks.add(new Todo("task"));
        // mark 0 is rejected before reaching TaskList.get (index < 1 check)
        assertThrows(ZiqException.class, () -> Parser.executeCommand("mark 0", tasks, ui, storage));
        // mark 2 causes IndexOutOfBoundsException in TaskList.get which is caught and rethrown as ZiqException
        assertThrows(ZiqException.class, () -> Parser.executeCommand("mark 2", tasks, ui, storage));
    }

    @Test
    public void executeCommand_markNonNumeric_throwsException() {
        tasks.add(new Todo("task"));
        assertThrows(ZiqException.class, () -> Parser.executeCommand("mark abc", tasks, ui, storage));
    }

    @Test
    public void executeCommand_mark_normalizesSpaces() throws ZiqException {
        tasks.add(new Todo("task"));
        Parser.executeCommand("mark   1", tasks, ui, storage);
        assertTrue(tasks.get(0).getStatus().equals("✅"));
    }

    @Test
    public void executeCommand_unmark_validIndex() throws ZiqException {
        tasks.add(new Todo("task"));
        tasks.get(0).markAsDone();
        Parser.executeCommand("unmark 1", tasks, ui, storage);
        assertTrue(tasks.get(0).getStatus().equals(" "));
    }

    @Test
    public void executeCommand_delete_validIndex() throws ZiqException {
        tasks.add(new Todo("task"));
        Parser.executeCommand("delete 1", tasks, ui, storage);
        assertEquals(0, tasks.size());
    }

    @Test
    public void executeCommand_deleteMissingNumber_throwsException() {
        tasks.add(new Todo("task"));
        assertThrows(ZiqException.class, () -> Parser.executeCommand("delete", tasks, ui, storage));
    }

    @Test
    public void executeCommand_deleteInvalidIndex_throwsException() {
        tasks.add(new Todo("task"));
        assertThrows(ZiqException.class, () -> Parser.executeCommand("delete 0", tasks, ui, storage));
        assertThrows(ZiqException.class, () -> Parser.executeCommand("delete 2", tasks, ui, storage));
    }

    @Test
    public void executeCommand_find_matchingTasks() throws ZiqException {
        tasks.add(new Todo("read book"), new Todo("write book"), new Todo("exercise"));
        Parser.executeCommand("find book", tasks, ui, storage);
        String output = outputStream.toString();
        assertTrue(output.contains("matching tasks"));
        assertTrue(output.contains("read book"));
        assertTrue(output.contains("write book"));
        assertFalse(output.contains("exercise"));
    }

    @Test
    public void executeCommand_findEmptyKeyword_listsAll() throws ZiqException {
        tasks.add(new Todo("task1"), new Todo("task2"));
        Parser.executeCommand("find", tasks, ui, storage);
        String output = outputStream.toString();
        assertTrue(output.contains("here is your to-do list!"));
    }

    @Test
    public void executeCommand_schedule_validDate() throws ZiqException {
        LocalDateTime by = LocalDateTime.of(2022, 2, 22, 12, 0);
        tasks.add(new Deadline("submit", by, true));
        Parser.executeCommand("schedule 22022022", tasks, ui, storage);
        String output = outputStream.toString();
        assertTrue(output.contains("schedule"));
        assertTrue(output.contains("submit"));
    }

    @Test
    public void executeCommand_scheduleInvalidDate_throwsException() {
        assertThrows(ZiqException.class, () -> Parser.executeCommand("schedule 32012022", tasks, ui, storage));
    }

    @Test
    public void executeCommand_scheduleMissingDate_throwsException() {
        assertThrows(ZiqException.class, () -> Parser.executeCommand("schedule", tasks, ui, storage));
    }

    @Test
    public void executeCommand_duplicateTask_throwsException() throws ZiqException {
        Parser.executeCommand("todo read book", tasks, ui, storage);
        assertThrows(ZiqException.class, () -> Parser.executeCommand("todo read book", tasks, ui, storage));
    }

    @Test
    public void executeCommand_duplicateDeadline_throwsException() throws ZiqException {
        Parser.executeCommand("deadline submit /by 22022022 1200", tasks, ui, storage);
        assertThrows(ZiqException.class, () -> Parser.executeCommand(
                "deadline submit /by 22022022 1200", tasks, ui, storage));
    }

    @Test
    public void executeCommand_duplicateEvent_throwsException() throws ZiqException {
        Parser.executeCommand("event meeting /from 22022022 1200 /to 22022022 1400", tasks, ui, storage);
        assertThrows(ZiqException.class, () -> Parser.executeCommand(
                "event meeting /from 22022022 1200 /to 22022022 1400", tasks, ui, storage));
    }

    @Test
    public void executeCommand_clear_removesAllTasks() throws ZiqException {
        tasks.add(new Todo("task1"), new Todo("task2"), new Todo("task3"));
        assertEquals(3, tasks.size());
        Parser.executeCommand("clear", tasks, ui, storage);
        assertEquals(0, tasks.size());
        String output = outputStream.toString();
        assertTrue(output.contains("all tasks cleared"));
    }

    @Test
    public void executeCommand_clear_emptyList() throws ZiqException {
        assertEquals(0, tasks.size());
        Parser.executeCommand("clear", tasks, ui, storage);
        assertEquals(0, tasks.size());
        String output = outputStream.toString();
        assertTrue(output.contains("all tasks cleared"));
        assertTrue(output.contains("0 task(s) removed"));
    }

    @Test
    public void executeCommand_help_displaysCommands() throws ZiqException {
        Parser.executeCommand("help", tasks, ui, storage);
        String output = outputStream.toString();
        assertTrue(output.contains("commands available"));
        assertTrue(output.contains("todo"));
        assertTrue(output.contains("deadline"));
        assertTrue(output.contains("event"));
        assertTrue(output.contains("clear"));
    }

    private static class MockStorage extends Storage {
        public MockStorage() {
            super("test.txt", new Ui());
        }

        @Override
        public void save(java.util.ArrayList<Task> list) throws ZiqException {
            // Mock: do nothing
        }
    }
}

