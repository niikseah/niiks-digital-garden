package ziq;

import java.io.IOException;
import java.util.Collections;
import java.util.Set;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.geometry.Pos;
import javafx.scene.Node;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.text.Text;
import javafx.scene.text.TextFlow;

/**
 * Represents a dialog box with an accompanying image to represent speaker
 * and a label containing text from the speaker.
 */
public class DialogBox extends HBox {

    private static final Set<String> VALID_COMMANDS = Set.of(
            "bye", "list", "mark", "unmark", "todo", "deadline", "event", "delete", "find", "schedule",
            "clear", "help", "tag", "organise");

    @FXML
    private VBox dialogWrapper;
    @FXML
    private TextFlow dialog;
    @FXML
    private ImageView displayPicture;

    private DialogBox(String text, Image img, boolean isUser) {
        try {
            FXMLLoader fxmlLoader = new FXMLLoader(MainWindow.class.getResource("/view/DialogBox.fxml"));
            fxmlLoader.setController(this);
            fxmlLoader.setRoot(this);
            fxmlLoader.load();
        } catch (IOException e) {
            e.printStackTrace();
        }

        setDialogContent(text, isUser);
        displayPicture.setImage(img);
        makeImageViewCircular(displayPicture);
        dialogWrapper.heightProperty().addListener((o, oldVal, newVal) -> updateAlignment());
    }

    /**
     * Sets HBox and VBox alignment: center when message height <= avatar height, top when taller.
     */
    private void updateAlignment() {
        double wrapperHeight = dialogWrapper.getHeight();
        double avatarHeight = displayPicture.getFitHeight();
        boolean useTop = wrapperHeight > avatarHeight + 1;
        dialogWrapper.setAlignment(useTop ? Pos.TOP_LEFT : Pos.CENTER_LEFT);
        boolean messageFirst = getChildren().get(0) == dialogWrapper;
        setAlignment(useTop
                ? (messageFirst ? Pos.TOP_RIGHT : Pos.TOP_LEFT)
                : (messageFirst ? Pos.CENTER_RIGHT : Pos.CENTER_LEFT));
    }

    /**
     * Sets the dialog text. For user messages, colours the first word maroon if it is not a valid command.
     * For help text (starts with "here are the commands"), formats with colors and spacing.
     */
    private void setDialogContent(String text, boolean isUser) {
        dialog.getChildren().clear();
        if (text == null || text.isEmpty()) {
            return;
        }
        if (isUser) {
            String trimmed = text.trim();
            int space = trimmed.indexOf(' ');
            String firstWord = space < 0 ? trimmed : trimmed.substring(0, space);
            String rest = space < 0 ? "" : trimmed.substring(space);
            boolean validCommand = VALID_COMMANDS.contains(firstWord.toLowerCase());

            if (!validCommand && !firstWord.isEmpty()) {
                Text first = new Text(firstWord);
                first.setFill(Color.MAROON);
                Text restText = new Text(rest);
                restText.setFill(Color.BLACK);
                dialog.getChildren().addAll(first, restText);
            } else {
                // Color task type commands with darker versions of their task type colors
                Text firstWordText = new Text(firstWord);
                String lowerFirstWord = firstWord.toLowerCase();
                if (lowerFirstWord.equals("todo")) {
                    firstWordText.setFill(Color.web("#00B359")); // Darker green for todo
                } else if (lowerFirstWord.equals("deadline")) {
                    firstWordText.setFill(Color.web("#C0392B")); // Darker red for deadline
                } else if (lowerFirstWord.equals("event")) {
                    firstWordText.setFill(Color.web("#F1C40F")); // Darker yellow for event
                } else if (lowerFirstWord.equals("tag")) {
                    firstWordText.setFill(Color.web("#8E44AD")); // Purple for tag
                } else if (lowerFirstWord.equals("organise")) {
                    firstWordText.setFill(Color.web("#E67E22")); // Orange for organise
                } else {
                    firstWordText.setFill(Color.BLACK);
                }

                Text restText = new Text(rest);
                restText.setFill(Color.BLACK);
                dialog.getChildren().addAll(firstWordText, restText);
            }
        } else {
            if (text.startsWith("here are the commands")) {
                formatHelpText(text);
            } else {
                formatTextWithTags(text);
            }
        }
    }

    /**
     * Formats regular text, detecting task types and tags, coloring them appropriately.
     * Task types [E], [D], [T] are colored differently, and tags are colored with readable colors.
     *
     * @param text the text to format
     */
    private void formatTextWithTags(String text) {
        int lastIndex = 0;
        int textLength = text.length();

        while (lastIndex < textLength) {
            // Look for task type indicators first: [E], [D], [T]
            int taskTypeStart = text.indexOf("[", lastIndex);
            if (taskTypeStart >= 0 && taskTypeStart + 2 < textLength) {
                char nextChar = text.charAt(taskTypeStart + 1);
                if ((nextChar == 'E' || nextChar == 'D' || nextChar == 'T' || nextChar == '✅' || nextChar == ' ')
                        && text.charAt(taskTypeStart + 2) == ']') {
                    // Found a task type or status indicator
                    // Add text before task type
                    if (taskTypeStart > lastIndex) {
                        Text before = new Text(text.substring(lastIndex, taskTypeStart));
                        before.setFill(Color.WHITE);
                        dialog.getChildren().add(before);
                    }

                    // Color the task type indicator
                    Text taskType = new Text(text.substring(taskTypeStart, taskTypeStart + 3));
                    if (nextChar == 'E') {
                        taskType.setFill(Color.web("#FFEB3B")); // Bright yellow for Events
                    } else if (nextChar == 'D') {
                        taskType.setFill(Color.web("#E74C3C")); // Red for Deadlines
                    } else if (nextChar == 'T') {
                        taskType.setFill(Color.web("#00FF7F")); // Bright green for Todos
                    } else {
                        // Status indicator (✅ or space)
                        taskType.setFill(Color.WHITE);
                    }
                    dialog.getChildren().add(taskType);
                    lastIndex = taskTypeStart + 3;
                    continue;
                }
            }

            // Look for tags: [tag] (not task type indicators)
            int tagStart = text.indexOf(" [", lastIndex);
            if (tagStart < 0) {
                // No more tags, add remaining text
                if (lastIndex < textLength) {
                    Text remaining = new Text(text.substring(lastIndex));
                    remaining.setFill(Color.WHITE);
                    dialog.getChildren().add(remaining);
                }
                break;
            }

            // Add text before tag
            if (tagStart > lastIndex) {
                Text beforeTag = new Text(text.substring(lastIndex, tagStart));
                beforeTag.setFill(Color.WHITE);
                dialog.getChildren().add(beforeTag);
            }

            // Find tag end
            int tagEnd = text.indexOf("]", tagStart + 2);
            if (tagEnd < 0) {
                // No closing bracket, add rest as normal text
                Text remaining = new Text(text.substring(tagStart));
                remaining.setFill(Color.WHITE);
                dialog.getChildren().add(remaining);
                break;
            }

            // Extract tag (without brackets)
            String tag = text.substring(tagStart + 2, tagEnd);
            Text tagText = new Text(" [" + tag + "]");
            tagText.setFill(getTagColor(tag));
            dialog.getChildren().add(tagText);

            lastIndex = tagEnd + 1;
        }
    }

    /**
     * Generates a consistent, readable color for a tag based on its name.
     * Same tag name will always produce the same color.
     * Colors are chosen from a palette of vibrant, readable colors.
     *
     * @param tagName the tag name
     * @return a Color for the tag
     */
    private Color getTagColor(String tagName) {
        // Predefined palette of readable, vibrant colors
        Color[] colorPalette = {
            Color.web("#FFD93D"), // Yellow
            Color.web("#6BCB77"), // Green
            Color.web("#4D96FF"), // Blue
            Color.web("#FF6B6B"), // Red
            Color.web("#A8E6CF"), // Light green
            Color.web("#FFD3A5"), // Peach
            Color.web("#C7CEEA"), // Lavender
            Color.web("#FFB6C1"), // Light pink
            Color.web("#87CEEB"), // Sky blue
            Color.web("#F0E68C"), // Khaki
            Color.web("#DDA0DD"), // Plum
            Color.web("#98D8C8"), // Mint
            Color.web("#FFA07A"), // Light salmon
            Color.web("#B0E0E6"), // Powder blue
            Color.web("#FFE4B5") // Moccasin
        };

        // Use hash to select a color from palette
        int hash = Math.abs(tagName.hashCode());
        return colorPalette[hash % colorPalette.length];
    }

    /**
     * Formats help text with colors: commands in cyan, parameters in yellow, descriptions in white.
     * Adds spacing between commands.
     */
    private void formatHelpText(String text) {
        String[] lines = text.split("\n");
        boolean isFirstLine = true;
        for (int i = 0; i < lines.length; i++) {
            String line = lines[i].trim();
            if (line.isEmpty()) {
                // Add spacing for empty lines
                Text spacing = new Text("\n");
                dialog.getChildren().add(spacing);
                continue;
            }

            // Header line
            if (line.startsWith("here are the commands")) {
                Text header = new Text(line + "\n");
                header.setFill(Color.WHITE);
                dialog.getChildren().add(header);
                isFirstLine = false;
                continue;
            }

            // Command lines - format: "command <param> - description"
            int dashIndex = line.indexOf(" - ");
            if (dashIndex > 0) {
                String beforeDash = line.substring(0, dashIndex).trim();
                String afterDash = line.substring(dashIndex + 3).trim();

                // Parse command and parameters
                String[] parts = beforeDash.split(" ", 2);
                String command = parts[0];
                String params = parts.length > 1 ? " " + parts[1] : "";

                // Command in cyan
                Text cmdText = new Text(command);
                cmdText.setFill(Color.CYAN);
                dialog.getChildren().add(cmdText);

                // Parameters in yellow
                if (!params.isEmpty()) {
                    Text paramText = new Text(params);
                    paramText.setFill(Color.web("#FFD700")); // Gold/yellow
                    dialog.getChildren().add(paramText);
                }

                // Separator and description in white
                Text descText = new Text(" - " + afterDash);
                descText.setFill(Color.WHITE);
                dialog.getChildren().add(descText);
            } else {
                // Plain text line
                Text plainText = new Text(line);
                plainText.setFill(Color.WHITE);
                dialog.getChildren().add(plainText);
            }

            // Add newline after each line (except last)
            if (i < lines.length - 1) {
                Text newline = new Text("\n");
                dialog.getChildren().add(newline);
            }
            isFirstLine = false;
        }
    }

    /**
     * Clips the ImageView to a circle and scales the image to fill the circle (crop to circle).
     */
    private void makeImageViewCircular(ImageView imageView) {
        double size = 90;
        Image img = imageView.getImage();
        double fitW = size;
        double fitH = size;
        if (img != null && img.getWidth() > 0 && img.getHeight() > 0) {
            double w = img.getWidth();
            double h = img.getHeight();
            if (w >= h) {
                fitW = size * w / h;
                fitH = size;
            } else {
                fitW = size;
                fitH = size * h / w;
            }
            imageView.setFitWidth(fitW);
            imageView.setFitHeight(fitH);
        }
        double radius = Math.min(fitW, fitH) / 2;
        double centerX = fitW / 2;
        double centerY = fitH / 2;
        Circle clip = new Circle(centerX, centerY, radius);
        imageView.setClip(clip);
    }

    /**
     * Flips the dialog box for Ziq.
     */
    private void flip() {
        ObservableList<Node> tmp = FXCollections.observableArrayList(this.getChildren());
        Collections.reverse(tmp);
        getChildren().setAll(tmp);
        setAlignment(Pos.TOP_LEFT);
    }

    /**
     * Applies Ziq's style (white text; blue bubble).
     */
    private void setZiqStyle() {
        dialogWrapper.setStyle("");
        getStyleClass().add("ziq-dialog");
    }

    /**
     * Creates a dialog box for user messages.
     *
     * @param text the user's message text
     * @param img the user's avatar image
     * @return a DialogBox configured for user messages
     */
    public static DialogBox getUserDialog(String text, Image img) {
        return new DialogBox(text, img, true);
    }

    /**
     * Creates a dialog box for Ziq's messages.
     *
     * @param text Ziq's response text
     * @param img Ziq's avatar image
     * @return a DialogBox configured for Ziq's messages (flipped and styled)
     */
    public static DialogBox getDukeDialog(String text, Image img) {
        DialogBox db = new DialogBox(text, img, false);
        db.flip();
        db.setZiqStyle();
        return db;
    }
}

