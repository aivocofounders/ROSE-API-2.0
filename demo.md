# Aivoco WebSocket Integration - Developer Documentation

## Overview
This document describes the WebSocket (WSS) implementation for the AI Voice Call application that enables real-time bidirectional audio communication between a web client and an AI voice agent through the Aivoco platform.

## Architecture

### WebSocket Connection
- **Endpoint**: `wss://call.aivoco.on.cloud.vispark.in/ws/{apiKey}/{agentId}`
- **Protocol**: Secure WebSocket (WSS) over TLS
- **Authentication**: URL-based using API key and agent ID parameters

### Audio Processing Pipeline
1. **Input**: Microphone → MediaRecorder → WebRTC Audio Stream
2. **Encoding**: Raw audio → Base64 encoded chunks
3. **Transport**: WebSocket messages 
4. **Output**: Base64 payload → μ-law PCM → Web Audio API playback

## WebSocket Message Protocol

### Connection Initialization
The client sends two initialization messages upon connection:

1. **Empty Handshake Message**
   ```javascript
   websocket.send('');
   ```

2. **Start Message**
   ```json
   {
     "event": "start",
     "sequenceNumber": "1",
     "start": {
       "accountSid": "AC{randomString}",
       "streamSid": "MZ{randomString}",
       "callSid": "CA{randomString}",
       "tracks": ["inbound"],
       "customParameters": {},
       "mediaFormat": {
         "encoding": "audio/x-mulaw",
         "sampleRate": 8000,
         "channels": 1
       }
     },
     "streamSid": "MZ{randomString}"
   }
   ```

### Audio Data Messages

#### Outbound Audio (Client → Server)
```json
{
  "event": "media",
  "media": {
    "track": "inbound",
    "chunk": sequenceNumber,
    "timestamp": "currentTimestamp",
    "payload": "base64EncodedAudioData"
  },
  "sequenceNumber": sequenceNumber
}
```

#### Inbound Audio (Server → Client)
```json
{
  "event": "media",
  "media": {
    "chunk": chunkNumber,
    "timestamp": timestamp,
    "payload": "base64EncodedMulawAudio"
  }
}
```

## Audio Processing Details

### Input Audio Configuration
- **Sample Rate**: 16kHz (for recording), 8kHz (for transmission)
- **Channels**: Mono (1 channel)
- **Format**: WebM with Opus codec (preferred), fallback to MP4
- **Features**: Echo cancellation, noise suppression, auto gain control enabled

### Audio Encoding Process
1. **Capture**: MediaRecorder captures audio in 100ms chunks
2. **Conversion**: ArrayBuffer → Base64 string encoding
3. **Sequencing**: Each chunk assigned incremental sequence number
4. **Transmission**: JSON message with media payload

### Audio Decoding Process
1. **Reception**: Base64 payload from WebSocket message
2. **Decoding**: Base64 → Binary data (μ-law format)
3. **Conversion**: μ-law → 16-bit PCM using lookup table
4. **Playback**: Web Audio API buffer source with volume control

### μ-law to PCM Conversion
The application includes a complete μ-law to PCM conversion table for audio decoding:
- **Input**: 8-bit μ-law encoded samples
- **Output**: 16-bit signed PCM samples
- **Range**: -32124 to +32124 (signed 16-bit)

## Connection Management

### Connection States
- **Disconnected**: Initial state, ready to connect
- **Connecting**: Establishing WebSocket connection and audio setup
- **Connected**: Active call with bidirectional audio

### Error Handling
- **Microphone Access**: Graceful fallback if permission denied
- **WebSocket Errors**: Connection timeout (10s), credential validation
- **Audio Playback**: Silent failure to prevent error spam
- **Connection Loss**: Automatic cleanup and state reset

### Cleanup Process
1. Stop MediaRecorder and audio recording
2. Close all audio stream tracks
3. Close AudioContext
4. Close WebSocket connection
5. Reset sequence numbers and stream IDs

## Implementation Features

### Real-time Audio Streaming
- **Chunk Size**: 100ms audio segments
- **Latency**: Optimized for real-time conversation
- **Buffering**: Minimal buffering for low-latency playback

### Audio Quality Controls
- **Volume Control**: 0-100% adjustable playback volume
- **Audio Indicators**: Visual feedback for listening/speaking states
- **Format Support**: Multiple codec fallbacks for browser compatibility

### Logging and Debugging
- **Comprehensive Logging**: All WebSocket messages and audio data
- **Message Details**: Payload size, chunk numbers, timestamps
- **Audio Metrics**: Raw buffer sizes, encoding information
- **Connection Events**: State changes, errors, and cleanup actions

### Security Considerations
- **Secure Transport**: WSS (WebSocket Secure) encryption
- **Credential Validation**: Server-side API key and agent ID verification
- **Audio Permissions**: Explicit microphone access request
- **Data Handling**: No persistent storage of audio data

## Browser Compatibility

### Required APIs
- **WebSocket**: For real-time communication
- **MediaDevices.getUserMedia**: For microphone access
- **MediaRecorder**: For audio capture
- **Web Audio API**: For audio playback and processing
- **Base64 Encoding**: For audio data transport

### Supported Formats
- **Primary**: audio/webm;codecs=opus
- **Fallback**: audio/webm, audio/mp4
- **Playback**: μ-law PCM via Web Audio API

## Usage Example

### Basic Integration
```javascript
const aiVoiceCall = new AIVoiceCall();
// User provides API key and agent ID through UI
// Click call button to initiate connection
```

### Custom Implementation
```javascript
// Initialize with credentials
const wsUrl = `wss://call.aivoco.on.cloud.vispark.in/ws/${apiKey}/${agentId}`;
const websocket = new WebSocket(wsUrl);

// Handle connection and send initialization messages
websocket.onopen = () => {
  websocket.send(''); // Handshake
  websocket.send(JSON.stringify(startMessage));
};

// Process incoming audio
websocket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.event === 'media') {
    playMulawAudio(data.media.payload);
  }
};
```

## Performance Considerations

### Optimization Strategies
- **Chunk Size**: 100ms provides good balance of latency vs. overhead
- **Sequence Management**: Incremental numbering for packet ordering
- **Memory Management**: Automatic cleanup of audio resources
- **Error Recovery**: Graceful handling of connection issues

### Resource Usage
- **CPU**: Moderate for real-time audio processing
- **Memory**: Minimal buffering, immediate processing
- **Bandwidth**: ~64kbps for 8kHz μ-law audio stream
- **Battery**: Optimized for mobile device usage

## Troubleshooting

### Common Issues
1. **Microphone Permission**: Ensure HTTPS context for getUserMedia
2. **WebSocket Connection**: Verify API credentials and network connectivity
3. **Audio Playback**: Check browser audio codec support
4. **Cross-Origin**: Ensure proper CORS configuration if hosting separately

### Debug Information
- Monitor browser console for detailed logging
- Check WebSocket network tab for message flow
- Verify audio permissions in browser settings
- Test with different audio input devices

This implementation provides a robust, real-time voice communication system suitable for AI voice assistant applications with comprehensive error handling and browser compatibility.
