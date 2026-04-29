package ziq;

/**
 * Exception thrown when an error occurs in the Ziq application.
 */
public class ZiqException extends Exception {
    /**
     * Constructs a new ZiqException with the specified error message.
     *
     * @param message the error message
     */
    public ZiqException(String message) {
        super(message);
    }
}

