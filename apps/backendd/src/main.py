import cv2
from stampede_detector import StampedeDetector
from visualization import VisualizationManager

def main():
    # Initialize video capture with webcam
    cap = cv2.VideoCapture(0)  # Use 0 for default webcam
    
    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    #Allocated the variables to the other codes jinko import kiya hai..aur visualizer of params diye hai height and width ke taaki detect kr skee...
    detector = StampedeDetector()
    visualizer = VisualizationManager(frame_width, frame_height)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Process frame
        result, boxes = detector.process_frame(frame)
        
        # Visualize results
        frame = visualizer.draw_boxes(frame, boxes)
        frame = visualizer.draw_stats(frame, result)
        
        # Display frame
        cv2.imshow('Stampede Detection System', frame)
        
        # Break loop on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    # Save final results to CSV
    detector.results_df.to_csv('stampede_detection_results.csv', index=False)

if __name__ == "__main__":
    main() 