package ziq;

import javafx.animation.PauseTransition;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.ScrollPane;
import javafx.scene.control.TextField;
import javafx.scene.image.Image;
import javafx.scene.image.WritableImage;
import javafx.scene.input.ScrollEvent;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import javafx.util.Duration;

/**
 * Controller for the main GUI.
 */
public class MainWindow extends AnchorPane {

    private static final int DEFAULT_IMAGE_SIZE = 100;
    private static final double SCROLL_BAR_HIDE_DELAY_SECONDS = 1.5;
    private static final double SCROLL_PANE_MAX_VALUE = 1.0;

    @FXML
    private ScrollPane scrollPane;
    @FXML
    private VBox dialogContainer;
    @FXML
    private TextField userInput;
    @FXML
    private Button sendButton;

    private Ziq ziq;
    private Stage stage;

    private Image userImage;
    private Image ziqImage;

    private PauseTransition scrollBarHideTransition;

    /**
     * Loads an image from the resources folder.
     *
     * @param resourcePath the path to the image resource
     * @return the loaded Image, or a blank image if loading fails
     */
    private static Image loadImage(String resourcePath) {
        var stream = MainWindow.class.getResourceAsStream(resourcePath);
        if (stream == null) {
            return new WritableImage(DEFAULT_IMAGE_SIZE, DEFAULT_IMAGE_SIZE);
        }
        try (stream) {
            return new Image(stream);
        } catch (Exception e) {
            return new WritableImage(DEFAULT_IMAGE_SIZE, DEFAULT_IMAGE_SIZE);
        }
    }

    /**
     * Initializes the main window, consisting of images and dialog boxes.
     */
    @FXML
    public void initialize() {
        userImage = loadImage("/images/user.jpg");
        ziqImage = loadImage("/images/ziq.jpg");
        dialogContainer.heightProperty().addListener((observable) -> scrollPane.setVvalue(SCROLL_PANE_MAX_VALUE));
        dialogContainer.getChildren().add(DialogBox.getDukeDialog(
                "hi, i'm ziq!\nplease give me a command!\nif you need help, enter 'help'.", ziqImage));
        setupScrollBarRevealOnScroll();
    }

    /**
     * Shows the scroll bar when the user scrolls with the mouse wheel, then hides it after a delay.
     */
    private void setupScrollBarRevealOnScroll() {
        scrollBarHideTransition = new PauseTransition(Duration.seconds(SCROLL_BAR_HIDE_DELAY_SECONDS));
        scrollBarHideTransition.setOnFinished(e -> scrollPane.getStyleClass().remove("scrolling"));
        scrollPane.addEventFilter(ScrollEvent.SCROLL, e -> {
            if (!scrollPane.getStyleClass().contains("scrolling")) {
                scrollPane.getStyleClass().add("scrolling");
            }
            scrollBarHideTransition.playFromStart();
        });
    }

    /**
     * Sets the Ziq instance for this controller.
     *
     * @param z the Ziq instance to use
     */
    public void setZiq(Ziq z) {
        ziq = z;
    }

    /**
     * Sets the stage so the window can be closed when the user says "bye".
     *
     * @param s the stage to control
     */
    public void setStage(Stage s) {
        stage = s;
    }

    /**
     * Handles user input: creates dialog boxes for user input and Ziq's reply,
     * and clears the input field after processing.
     * Closes the window if the user says "bye".
     */
    @FXML
    private void handleUserInput() {
        String input = userInput.getText().trim();
        userInput.clear();
        if (input.isEmpty()) {
            return;
        }
        String response = ziq.getResponse(input);
        dialogContainer.getChildren().addAll(
                DialogBox.getUserDialog(input, userImage),
                DialogBox.getDukeDialog(response, ziqImage)
        );
        if (stage != null && "Bye. Hope to see you again!".equals(response)) {
            stage.close();
        }
    }
}

