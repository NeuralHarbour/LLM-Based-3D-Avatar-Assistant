use figlet_rs::FIGfont;
use indicatif::ProgressBar;
use rodio::Sink;
use std::fs::File;
use std::process::Command;
use std::thread;
use std::time::Duration;
use ctrlc;

fn main() {

    let standard_font = FIGfont::standard().unwrap();
    let figure = standard_font.convert("NEURAL HARBOUR AI");
    assert!(figure.is_some());

    let small_font = FIGfont::from_file("resources/ANSI.flf").unwrap();
    let figure = small_font.convert("NEURAL HARBOUR");
    assert!(figure.is_some());
    println!("{}", figure.unwrap());

    let spinner = ProgressBar::new_spinner();
    spinner.set_message("Loading...");
    spinner.enable_steady_tick(100);

    play_startup_music();

    thread::sleep(Duration::from_secs_f64(0.6));

    spinner.finish_with_message("Done loading!");

    let _ = Command::new("python")
        .arg("D:/3DavatarAssistant/Backend/Server Side/server.py")
        .current_dir("D:/3DavatarAssistant/Backend/Server Side")
        .spawn()
        .expect("Failed To start server");

    let _stt_process = Command::new("python")
        .arg("D:/3DavatarAssistant/Backend/Server Side/STT.py")
        .spawn()
        .expect("Failed to start Speech to text Service");

    let _face_recognizer = Command::new("cargo")
        .arg("run")
        .arg("--manifest-path")
        .arg("D:/3DavatarAssistant/Backend/Server Side/Recognizers/Face/rust-opencv/Cargo.toml")
        .current_dir("D:/3DavatarAssistant/Backend/Server Side/Recognizers/Face/rust-opencv")
        .spawn()
        .expect("Failed to start Face Recognizer");

    let _jp_stt = Command::new("D:/3DavatarAssistant/Backend/JP_STT Binaries/run.exe")
        .current_dir("D:/3DavatarAssistant/Backend/JP_STT Binaries")
        .spawn()
        .expect("Failed to run JP_STT");

    let running = std::sync::Arc::new(std::sync::atomic::AtomicBool::new(true));
    let r = running.clone();
    ctrlc::set_handler(move || {
        r.store(false, std::sync::atomic::Ordering::SeqCst);
    }).expect("Error setting Ctrl-C handler");

    // Main loop
    while running.load(std::sync::atomic::Ordering::SeqCst) {
        // Your main program logic here...
    }

    // Cleanup code after Ctrl-C
    println!("Ctrl-C pressed. Exiting...");
    play_interrupt_music();
    // Additional cleanup code if needed...
}

fn play_startup_music() {
    let file = File::open("resources/LOADER.mp3").expect("Failed to open music file");
    let (_stream, stream_handle) = rodio::OutputStream::try_default().unwrap();
    let sink = Sink::try_new(&stream_handle).unwrap();
    let source = rodio::Decoder::new(file).unwrap();
    sink.append(source);
    thread::sleep(Duration::from_secs(5));
}
fn play_interrupt_music() {
    let file = File::open("resources/interrupt.mp3").expect("Failed to open music file");
    let (_stream, stream_handle) = rodio::OutputStream::try_default().unwrap();
    let sink = Sink::try_new(&stream_handle).unwrap();
    let source = rodio::Decoder::new(file).unwrap();
    sink.append(source);
    thread::sleep(Duration::from_secs(3));
}
