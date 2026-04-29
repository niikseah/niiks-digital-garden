package ziq;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

public class ZiqExceptionTest {

    @Test
    public void ziqException_withMessage() {
        String message = "Test error message";
        ZiqException e = new ZiqException(message);
        assertEquals(message, e.getMessage());
        assertNotNull(e);
    }

    @Test
    public void ziqException_emptyMessage() {
        ZiqException e = new ZiqException("");
        assertEquals("", e.getMessage());
    }

    @Test
    public void ziqException_isException() {
        ZiqException e = new ZiqException("error");
        assertTrue(e instanceof Exception);
    }
}

