package ziq;

/**
 * Enumeration of task types with their corresponding codes.
 */
public enum TaskType {
    TODO("T"), DEADLINE("D"), EVENT("E");

    private final String code;

    /**
     * Constructs a TaskType with the given code.
     *
     * @param code the code representing this task type
     */
    TaskType(String code) {
        this.code = code;
    }

    /**
     * Returns the code for this task type.
     *
     * @return the code string
     */
    public String getCode() {
        return code;
    }

    /**
     * Returns the TaskType corresponding to the given code.
     *
     * @param code the code to look up
     * @return the corresponding TaskType
     * @throws ZiqException if the code does not match any task type
     */
    public static TaskType findTaskType(String code) throws ZiqException {
        for (TaskType t : TaskType.values()) {
            if (t.getCode().equals(code)) {
                return t;
            }
        }
        throw new ZiqException("what kind of task is this?");
    }
}

