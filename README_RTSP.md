# MMM-Face-Recognition-SMAI with RTSP Support

This modified version of the MMM-Face-Recognition-SMAI module now supports multiple video sources including RTSP streams, USB cameras, and the original PiCamera.

## New Features

- **RTSP Stream Support**: Connect to IP cameras via RTSP protocol
- **USB Camera Support**: Use standard USB webcams
- **PiCamera Support**: Maintains original Raspberry Pi camera functionality
- **Flexible Configuration**: Command-line arguments for easy source selection
- **Error Handling**: Robust error handling for connection issues

## Dependencies

Install the required dependencies:

```bash
pip install opencv-python face_recognition picamera numpy
```

## Usage

### 1. PiCamera (Original functionality)
```bash
python MMM-Face-Recognition-SMAI.py --source picamera
```

### 2. RTSP Stream
```bash
python MMM-Face-Recognition-SMAI.py --source rtsp --rtsp-url "rtsp://username:password@ip_address:port/stream_path"
```

Example RTSP URLs:
- `rtsp://192.168.1.100:554/stream1`
- `rtsp://admin:password@192.168.1.100:554/live/main`
- `rtsp://user:pass@camera_ip:554/h264Preview_01_main`

### 3. USB Camera
```bash
python MMM-Face-Recognition-SMAI.py --source usb --usb-index 0
```

## Command Line Arguments

- `--source`: Video source type (`picamera`, `rtsp`, `usb`)
- `--rtsp-url`: RTSP stream URL (required for rtsp source)
- `--usb-index`: USB camera index (default: 0)

## Configuration

The script maintains the same face recognition logic and file structure as the original:
- Face images should be placed in `/home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/public/`
- Recognition results are written to `sample.txt`
- Same 15-second timeout for user detection

## Error Handling

The script includes robust error handling for:
- Connection failures to RTSP streams
- USB camera initialization issues
- Frame capture errors
- Graceful shutdown on Ctrl+C

## Troubleshooting

### RTSP Issues
- Verify the RTSP URL is correct
- Check network connectivity to the camera
- Ensure camera supports RTSP protocol
- Try different RTSP URL formats

### USB Camera Issues
- Check if camera is connected and recognized
- Try different USB camera indices (0, 1, 2, etc.)
- Verify camera permissions

### Performance
- RTSP streams may have higher latency than local cameras
- Consider network bandwidth for RTSP streams
- Adjust frame resolution if needed (currently set to 320x240)
