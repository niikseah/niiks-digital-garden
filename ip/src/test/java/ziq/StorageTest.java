package ziq;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.util.ArrayList;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

public class StorageTest {

    @TempDir
    Path tempDir;

    private Storage storage;
    private File testFile;
    private Ui ui;

    @BeforeEach
    public void setUp() {
        testFile = tempDir.resolve("test.txt").toFile();
        ui = new Ui();
        storage = new Storage(testFile.getPath(), ui);
    }

    @AfterEach
    public void tearDown() {
        if (testFile.exists()) {
            testFile.delete();
        }
    }

    @Test
    public void load_nonExistentFile_returnsEmptyList() throws ZiqException {
        ArrayList<Task> tasks = storage.load();
        assertEquals(0, tasks.size());
    }

    @Test
    public void load_emptyFile_returnsEmptyList() throws IOException, ZiqException {
        testFile.createNewFile();
        ArrayList<Task> tasks = storage.load();
        assertEquals(0, tasks.size());
    }

    @Test
    public void load_todoTask_loadsCorrectly() throws IOException, ZiqException {
        try (FileWriter writer = new FileWriter(testFile)) {
            writer.write("T | 0 | read book\n");
        }
        ArrayList<Task> tasks = storage.load();
        assertEquals(1, tasks.size());
        assertTrue(tasks.get(0) instanceof Todo);
        assertEquals("read book", tasks.get(0).description());
    }

    @Test
    public void load_todoTaskDone_loadsCorrectly() throws IOException, ZiqException {
        try (FileWriter writer = new FileWriter(testFile)) {
            writer.write("T | 1 | read book\n");
        }
        ArrayList<Task> tasks = storage.load();
        assertEquals(1, tasks.size());
        assertTrue(tasks.get(0).getStatus().equals("✅"));
    }

    @Test
    public void load_deadlineTask_loadsCorrectly() throws IOException, ZiqException {
        try (FileWriter writer = new FileWriter(testFile)) {
            writer.write("D | 0 | submit report | 2022-02-22T12:00\n");
        }
        ArrayList<Task> tasks = storage.load();
        assertEquals(1, tasks.size());
        assertTrue(tasks.get(0) instanceof Deadline);
        Deadline d = (Deadline) tasks.get(0);
        assertEquals("submit report", d.description());
        assertEquals(LocalDateTime.of(2022, 2, 22, 12, 0), d.by());
    }

    @Test
    public void load_eventTask_loadsCorrectly() throws IOException, ZiqException {
        try (FileWriter writer = new FileWriter(testFile)) {
            writer.write("E | 0 | meeting | 2022-02-22T12:00 | 2022-02-22T14:00\n");
        }
        ArrayList<Task> tasks = storage.load();
        assertEquals(1, tasks.size());
        assertTrue(tasks.get(0) instanceof Event);
        Event e = (Event) tasks.get(0);
        assertEquals("meeting", e.description());
        assertEquals(LocalDateTime.of(2022, 2, 22, 12, 0), e.from());
        assertEquals(LocalDateTime.of(2022, 2, 22, 14, 0), e.to());
    }

    @Test
    public void load_multipleTasks_loadsAll() throws IOException, ZiqException {
        try (FileWriter writer = new FileWriter(testFile)) {
            writer.write("T | 0 | task1\n");
            writer.write("T | 0 | task2\n");
            writer.write("T | 0 | task3\n");
        }
        ArrayList<Task> tasks = storage.load();
        assertEquals(3, tasks.size());
    }

    @Test
    public void load_invalidTaskType_skipsLine() throws IOException, ZiqException {
        try (FileWriter writer = new FileWriter(testFile)) {
            writer.write("X | 0 | invalid\n");
            writer.write("T | 0 | valid\n");
        }
        ArrayList<Task> tasks = storage.load();
        assertEquals(1, tasks.size());
        assertEquals("valid", tasks.get(0).description());
    }

    @Test
    public void load_incompleteLine_skipsLine() throws IOException, ZiqException {
        try (FileWriter writer = new FileWriter(testFile)) {
            writer.write("T | 0\n");
            writer.write("T | 0 | complete\n");
        }
        ArrayList<Task> tasks = storage.load();
        assertEquals(1, tasks.size());
    }

    @Test
    public void load_invalidDate_throwsException() throws IOException {
        try (FileWriter writer = new FileWriter(testFile)) {
            writer.write("D | 0 | task | invalid-date\n");
        }
        assertThrows(ZiqException.class, () -> storage.load());
    }

    @Test
    public void save_todoTask_writesCorrectly() throws ZiqException, IOException {
        ArrayList<Task> tasks = new ArrayList<>();
        tasks.add(new Todo("read book"));
        storage.save(tasks);
        assertTrue(testFile.exists());
        String content = Files.readString(testFile.toPath());
        assertTrue(content.contains("T | 0 | read book"));
    }

    @Test
    public void save_todoTaskDone_writesCorrectly() throws ZiqException, IOException {
        ArrayList<Task> tasks = new ArrayList<>();
        Todo todo = new Todo("read book");
        todo.markAsDone();
        tasks.add(todo);
        storage.save(tasks);
        String content = Files.readString(testFile.toPath());
        assertTrue(content.contains("T | 1 | read book"));
    }

    @Test
    public void save_deadlineTask_writesCorrectly() throws ZiqException, IOException {
        ArrayList<Task> tasks = new ArrayList<>();
        LocalDateTime by = LocalDateTime.of(2022, 2, 22, 12, 0);
        tasks.add(new Deadline("submit", by, true));
        storage.save(tasks);
        String content = Files.readString(testFile.toPath());
        assertTrue(content.contains("D | 0 | submit"));
        assertTrue(content.contains("2022-02-22T12:00"));
    }

    @Test
    public void save_eventTask_writesCorrectly() throws ZiqException, IOException {
        ArrayList<Task> tasks = new ArrayList<>();
        LocalDateTime from = LocalDateTime.of(2022, 2, 22, 12, 0);
        LocalDateTime to = LocalDateTime.of(2022, 2, 22, 14, 0);
        tasks.add(new Event("meeting", from, to));
        storage.save(tasks);
        String content = Files.readString(testFile.toPath());
        assertTrue(content.contains("E | 0 | meeting"));
        assertTrue(content.contains("2022-02-22T12:00"));
        assertTrue(content.contains("2022-02-22T14:00"));
    }

    @Test
    public void save_multipleTasks_writesAll() throws ZiqException, IOException {
        ArrayList<Task> tasks = new ArrayList<>();
        tasks.add(new Todo("task1"));
        tasks.add(new Todo("task2"));
        tasks.add(new Todo("task3"));
        storage.save(tasks);
        String content = Files.readString(testFile.toPath());
        assertTrue(content.contains("task1"));
        assertTrue(content.contains("task2"));
        assertTrue(content.contains("task3"));
    }

    @Test
    public void save_emptyList_createsFile() throws ZiqException {
        ArrayList<Task> tasks = new ArrayList<>();
        storage.save(tasks);
        assertTrue(testFile.exists());
    }

    @Test
    public void save_overwritesExistingFile() throws ZiqException, IOException {
        ArrayList<Task> tasks1 = new ArrayList<>();
        tasks1.add(new Todo("old"));
        storage.save(tasks1);
        ArrayList<Task> tasks2 = new ArrayList<>();
        tasks2.add(new Todo("new"));
        storage.save(tasks2);
        String content = Files.readString(testFile.toPath());
        assertTrue(content.contains("new"));
        assertTrue(!content.contains("old"));
    }
}

