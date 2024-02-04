use tokio::net::TcpListener;
use tokio_tungstenite::accept_async;
use futures_util::stream::StreamExt;
use tokio_tungstenite::tungstenite::protocol::Message;
use futures_util::sink::SinkExt;

use opencv::{
    prelude::*,
    objdetect,
    highgui,
    imgproc,
    core,
    types,
    videoio,
    imgcodecs::IMREAD_COLOR,
    Result,
};

#[tokio::main]
async fn main() -> Result<()> {
    let addr = "127.0.0.1:8765";
    let listener = TcpListener::bind(addr).await.expect("Failed to bind");

    println!("WebSocket server is running on ws://{}", addr);

    while let Ok((stream, _)) = listener.accept().await {
        tokio::spawn(handle_connection(stream));
    }

    Ok(())
}

async fn handle_connection(stream: tokio::net::TcpStream) {
    if let Ok(ws_stream) = accept_async(stream).await {
        println!("WebSocket connection established to Unity");

        // Initialize the camera and face detector
        let mut camera = videoio::VideoCapture::new(0, videoio::CAP_ANY)
            .expect("Failed to initialize camera");
        let xml = "D:/3DavatarAssistant/Backend/Server Side/haarcascade_frontalface_default.xml";
        let mut face_detector = objdetect::CascadeClassifier::new(xml)
            .expect("Failed to load face detector");

        receive_and_process_frames(ws_stream, &mut camera, &mut face_detector).await;
    } else {
        println!("Error during WebSocket handshake");
    }
}

async fn receive_and_process_frames(
    mut ws_stream: tokio_tungstenite::WebSocketStream<tokio::net::TcpStream>,
    camera: &mut videoio::VideoCapture,
    face_detector: &mut objdetect::CascadeClassifier,
) {
    // Store the previous number of faces
    let mut previous_num_faces = None;

    loop {
        let mut img = Mat::default();

        // Read a frame from the camera
        camera.read(&mut img).expect("Failed to read frame from camera");

        // Convert the frame to grayscale
        let mut gray = Mat::default();
        imgproc::cvt_color(&img, &mut gray, imgproc::COLOR_BGR2GRAY, 0)
            .expect("Failed to convert to grayscale");

        // Detect faces
        let mut faces = types::VectorOfRect::new();
        face_detector.detect_multi_scale(
            &gray,
            &mut faces,
            1.1,
            14,
            objdetect::CASCADE_SCALE_IMAGE,
            core::Size::new(10, 10),
            core::Size::new(0, 0),
        )
        .expect("Failed to detect faces");

        let current_num_faces = faces.len();
        if Some(current_num_faces) != previous_num_faces {
            // Send data only when there is a change in the number of faces
            if let Err(e) = ws_stream.send(Message::Text(format!("{}", current_num_faces))).await {
                eprintln!("Error sending message to client: {}", e);
            }

            // Update the previous number of faces
            previous_num_faces = Some(current_num_faces);
        }

        // Draw rectangles around detected faces
        if faces.len() > 0 {
            for face in faces.iter() {
                imgproc::rectangle(
                    &mut img,
                    face,
                    core::Scalar::new(0f64, 255f64, 0f64, 0f64),
                    2,
                    imgproc::LINE_8,
                    0,
                )
                .expect("Failed to draw rectangle");
            }
        }

        // Display the frame with rectangles around faces
        highgui::imshow("gray", &img).expect("Failed to display image");
        highgui::wait_key(1).expect("Failed to wait for key");
    }
}
