package ziq;

import java.io.IOException;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.layout.AnchorPane;
import javafx.stage.Stage;

/**
 * GUI for Ziq using FXML.
 */
public class Main extends Application {

    private static final double MIN_WINDOW_HEIGHT = 600.0;
    private static final double MIN_WINDOW_WIDTH = 400.0;

    private Ziq ziq = new Ziq();

    /**
     * Starts the JavaFX application and sets up the GUI.
     *
     * @param stage the primary stage for the application
     */
    @Override
    public void start(Stage stage) {
        try {
            FXMLLoader fxmlLoader = new FXMLLoader(Main.class.getResource("/view/MainWindow.fxml"));
            AnchorPane ap = fxmlLoader.load();
            Scene scene = new Scene(ap);
            scene.getStylesheets().add(Main.class.getResource("/view/styles.css").toExternalForm());
            stage.setScene(scene);
            MainWindow controller = fxmlLoader.getController();
            controller.setZiq(ziq);
            controller.setStage(stage);
            stage.setTitle("ziq 🦍");
            stage.setResizable(true);
            stage.setMinHeight(MIN_WINDOW_HEIGHT);
            stage.setMinWidth(MIN_WINDOW_WIDTH);
            stage.show();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

