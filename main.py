import cv2
from ultralytics import YOLO
import numpy as np
import time

class DribbleCounter:
    def __init__(self):
        # Load the YOLO model for ball detection
        """
        Initializes the DribbleCounter class.

        Attributes:
        - pose_model: YOLO object for pose estimation.
        - model: YOLO object for ball detection.
        - cap: VideoCapture object for reading input video.
        - prev_x_center: Previous x-coordinate of the basketball center.
        - prev_y_center: Previous y-coordinate of the basketball center.
        - prev_delta_y: Previous change in y-coordinate.
        - dribble_count: Counter for the number of dribbles detected.
        - dribble_threshold: Threshold for detecting a dribble based on y-coordinate change.
        - width: Width of the input video frames.
        - height: Height of the input video frames.
        - fourcc: FourCC codec for video writing.
        - combined_out: VideoWriter object for writing annotated frames
        """
        self.pose_model = YOLO("yolov8s-pose.pt")
        self.model = YOLO(
            "/home/shashank/Documents/Python_Workspace/analysis_basket_ball/basketball_dribbling/best17.pt")

        # Open the video file
        self.cap = cv2.VideoCapture("basket_ball.mp4")

        self.prev_x_center = None
        self.prev_y_center = None
        self.prev_delta_y = None

        self.dribble_count = 0

        self.dribble_threshold = 18

        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.combined_out = cv2.VideoWriter(
            "combined_output.mp4", self.fourcc, 24.0, (2 * self.width, self.height))
    
    def process_frame(self, frame):
        """
        Performs pose estimation on the frame with a lower confidence threshold.

        Args:
        - frame: Input video frame.

        Returns:
        - pose_annotated_frame: Annotated frame with pose estimation results.
        """

        pose_results = self.pose_model(frame, verbose=False, conf=0.5)
        pose_annotated_frame = pose_results[0].plot()

        return pose_annotated_frame

    def run(self):
        """
        Processes video frames, detects ball and poses, updates dribble count,
        and writes annotated frames to output video.

        """
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if success:
                results_list = self.model(frame, verbose=False, conf=0.45)
                print("RESULT LIST", results_list)
                pose_annotated_frame = self.process_frame(frame)

                for results in results_list:
                    for bbox in results.boxes.xyxy:
                        x1, y1, x2, y2 = bbox[:4]

                        x_center = (x1 + x2) / 2
                        y_center = (y1 + y2) / 2

                        print(
                            f"Ball coordinates: (x={x_center:.2f}, y={y_center:.2f})")

                        self.update_dribble_count(x_center, y_center)

                        self.prev_x_center = x_center
                        self.prev_y_center = y_center

                    annotated_frame = results.plot()

                    # Draw the dribble count on the frame
                    cv2.putText(annotated_frame, f"Dribbles: {self.dribble_count}", (
                        20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    # Write the annotated frame to the output video

                    combined_window = np.concatenate(
                        (annotated_frame, pose_annotated_frame), axis=1)
                    self.combined_out.write(combined_window)

                    cv2.namedWindow("Combined Inference", cv2.WINDOW_NORMAL)
                    cv2.imshow("Combined Inference", combined_window)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                break

        # Release the video capture and close windows
        self.cap.release()
        self.combined_out.release()
        cv2.destroyAllWindows()

    def update_dribble_count(self, x_center, y_center):
        """
        Updates the dribble count based on the change in the y-coordinate of the basketball.

        Args:
        - x_center: Current x-coordinate of the basketball center.
        - y_center: Current y-coordinate of the basketball center.

        """
        if self.prev_y_center is not None:
            delta_y = y_center - self.prev_y_center

            if (
                self.prev_delta_y is not None
                and self.prev_delta_y > self.dribble_threshold
                and delta_y < -self.dribble_threshold
            ):
                self.dribble_count += 1

            self.prev_delta_y = delta_y


if __name__ == "__main__":
    dribble_counter = DribbleCounter()
    dribble_counter.run()