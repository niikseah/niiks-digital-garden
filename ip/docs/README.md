# ziq user guide



ziq is a user-friendly task management chatbot that helps you keep track of your todos, deadlines, and events. 

## Quick Start

1. Launch the application
2. Type a command in the input field
3. Press Enter or click Send
4. ziq will update you on the system status

## Features

### Adding Tasks


| **todo** — Add a todo task                       |
| ------------------------------------------------ |
| Add a simple todo task without any date or time. |
| **Format:** `todo`                               |
| **Example:** `todo read book`                    |



| **deadline** — Add a deadline task                                                                         |
| ---------------------------------------------------------------------------------------------------------- |
| Add a deadline task with a due date. Time is optional - if not specified, it defaults to midnight (00:00). |
| **Format:** `deadline /by DDMMYYYY [HHmm]`                                                                 |
| **Examples:** `deadline submit report /by 22022022 1200` · `deadline finish assignment /by 15032022`       |



| **event** — Add an event task                                      |
| ------------------------------------------------------------------ |
| Add an event task with a start and end time.                       |
| **Format:** `event /from DDMMYYYY HHmm /to DDMMYYYY HHmm`          |
| **Example:** `event meeting /from 22022022 1200 /to 22022022 1400` |


### Viewing Tasks


| **list** — List all tasks    |
| ---------------------------- |
| View all tasks in your list. |
| **Format:** `list`           |


### Managing Tasks


| **mark** — Mark a task as done |
| ------------------------------ |
| Mark a task as completed.      |
| **Format:** `mark`             |
| **Example:** `mark 1`          |



| **unmark** — Mark a task as not done |
| ------------------------------------ |
| Mark a completed task as not done.   |
| **Format:** `unmark`                 |
| **Example:** `unmark 1`              |



| **delete** — Remove a task    |
| ----------------------------- |
| Remove a task from your list. |
| **Format:** `delete`          |
| **Example:** `delete 2`       |



| **clear** — Remove all tasks             |
| ---------------------------------------- |
| Remove all tasks from your list at once. |
| **Format:** `clear`                      |


### Finding Tasks


| **find** — Search tasks by keyword                               |
| ---------------------------------------------------------------- |
| Find tasks that contain a specific keyword in their description. |
| **Format:** `find`                                               |
| **Example:** `find book`                                         |


### Tagging Tasks


| **tag** — Add a tag to a task                                             |
| ------------------------------------------------------------------------- |
| Add a tag to any task (todo, deadline, or event) for better organization. |
| **Format:** `tag`                                                         |
| **Example:** `tag 1 work`                                                 |


### Organizing Tasks


| **organise tag** — Group tasks by tag                                                                                                   |
| --------------------------------------------------------------------------------------------------------------------------------------- |
| Group and display tasks organized by their tags. Tasks with the same tag are grouped together, and untagged tasks are shown separately. |
| **Format:** `organise tag`                                                                                                              |
| **Example:** `organise tag`                                                                                                             |



| **organise deadline** — Order tasks by deadline                                                                                     |
| ----------------------------------------------------------------------------------------------------------------------------------- |
| Display tasks organized by deadline, with deadlines sorted by due date, followed by events sorted by start date, and finally todos. |
| **Format:** `organise deadline`                                                                                                     |
| **Example:** `organise deadline`                                                                                                    |


### Viewing Schedule


| **schedule** — View tasks on a date                                               |
| --------------------------------------------------------------------------------- |
| View all tasks (deadlines and events) scheduled for a particular date.            |
| **Format:** `schedule DDMMYYYY` (or `DD` for day only, `DDMM` for day/month only) |
| **Example:** `schedule 22022022` or `schedule 22` or `schedule 2202`              |


### Getting Help


| **help** — Show available commands        |
| ----------------------------------------- |
| Display a list of all available commands. |
| **Format:** `help`                        |


### Exiting the Application


| **bye** — Exit the application |
| ------------------------------ |
| Close the application.         |
| **Format:** `bye`              |


## Command Summary


| Command  | Format                                        | Description                       |
| -------- | --------------------------------------------- | --------------------------------- |
| todo     | `todo`                                        | Add a todo task                   |
| deadline | `deadline /by DDMMYYYY [HHmm]`                | Add a deadline task               |
| event    | `event /from DDMMYYYY HHmm /to DDMMYYYY HHmm` | Add an event task                 |
| list     | `list`                                        | List all tasks                    |
| mark     | `mark`                                        | Mark a task as done               |
| unmark   | `unmark`                                      | Mark a task as not done           |
| delete   | `delete`                                      | Delete a task                     |
| find     | `find`                                        | Find tasks by keyword             |
| schedule | `schedule DDMMYYYY` (or DD, DDMM)             | View tasks on a date              |
| tag      | `tag`                                         | Add a tag to a task               |
| organise | `organise tag` or `organise deadline`         | Organize tasks by tag or deadline |
| clear    | `clear`                                       | Remove all tasks                  |
| help     | `help`                                        | Show help message                 |
| bye      | `bye`                                         | Exit the application              |


## Notes

- Task indices start from 1 (not 0)
- Dates use `DDMMYYYY` format with no slashes (e.g., `22022022` for February 22, 2022)
- For the `schedule` command, you can use partial dates:
  - `DD` - uses current month and year (e.g., `22` for the 22nd of the current month)
  - `DDMM` - uses current year (e.g., `2202` for February 22 of the current year)
  - `DDMMYYYY` - full date (e.g., `22022022`)
- Time format is `HHmm` (24-hour format, e.g., `1200` for 12:00 PM)
- If no time is specified for a `deadline`, only the date is displayed 
- Tasks are automatically saved to `data/ziq.txt`
- Duplicate tasks (same description and details) are not allowed
- Tags are color-coded for easy identification
- Command keywords in your input are color-coded: `todo`=green, `deadline`=red, `event`=yellow, `tag`=purple, `organise`=orange

