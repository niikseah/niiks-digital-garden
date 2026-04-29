package ziq;

import java.time.LocalDateTime;

import org.junit.jupiter.api.Test;

public class DebugTest {
    @Test
    public void eventHasCorrectFromAndTo() {
        LocalDateTime from = LocalDateTime.of(2022, 2, 22, 12, 0);
        LocalDateTime to = null;
        Event e = new Event("meeting", from, to);
    }
}

