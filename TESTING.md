# API Testing Guide

This guide shows how to test each backend using curl, Postman, or programming languages.

## Quick Health Checks

Test if backends are running:

```bash
# Python
curl http://localhost:8000/health

# Go
curl http://localhost:8001/health

# Rust
curl http://localhost:8002/health
```

Expected response:
```json
{
  "status": "healthy",
  "services": { ... }
}
```

## Testing Note Synthesis

### Python Backend

**Basic Note Synthesis:**
```bash
curl -X POST http://localhost:8000/synthesize \
  -H "Content-Type: application/json" \
  -d '{
    "note": "C4",
    "velocity": 0.8,
    "duration": 1.0
  }'
```

**With Custom Parameters:**
```bash
curl -X POST http://localhost:8000/synthesize \
  -H "Content-Type: application/json" \
  -d '{
    "note": "A4",
    "velocity": 0.9,
    "duration": 2.0
  }'
```

Expected response:
```json
{
  "status": "success",
  "file_id": "audio_0",
  "note": "C4",
  "size": 88244
}
```

### Go Backend

**Basic Synthesis:**
```bash
curl -X POST http://localhost:8001/synthesize \
  -H "Content-Type: application/json" \
  -d '{
    "note": "E4",
    "velocity": 0.7,
    "duration": 1.5
  }'
```

Expected response:
```json
{
  "status": "success",
  "note": "E4",
  "message": "Note processing started in pipeline"
}
```

### Rust Backend

**Basic Synthesis:**
```bash
curl -X POST http://localhost:8002/synthesize \
  -H "Content-Type: application/json" \
  -d '{
    "note": "G4",
    "velocity": 0.85,
    "duration": 1.2
  }'
```

Expected response:
```json
{
  "status": "success",
  "message": "Note sent to actor system for processing"
}
```

## Configuration Management

### Get Current Configuration

```bash
# Python
curl http://localhost:8000/config

# Go
curl http://localhost:8001/config

# Rust
curl http://localhost:8002/config
```

Expected response:
```json
{
  "attack": 0.005,
  "decay": 0.1,
  "sustain": 0.3,
  "release": 1.0,
  "waveform": "sine",
  "volume": 0.5
}
```

### Update Configuration

**Change to Sawtooth Wave:**
```bash
# Python
curl -X POST http://localhost:8000/config \
  -H "Content-Type: application/json" \
  -d '{
    "attack": 0.01,
    "decay": 0.2,
    "sustain": 0.5,
    "release": 1.5,
    "waveform": "sawtooth",
    "volume": 0.7
  }'
```

**Adjust ADSR for Piano-like Sound:**
```bash
curl -X POST http://localhost:8001/config \
  -H "Content-Type: application/json" \
  -d '{
    "attack": 0.002,
    "decay": 0.3,
    "sustain": 0.2,
    "release": 2.0,
    "waveform": "triangle",
    "volume": 0.6
  }'
```

**Adjust for Organ-like Sound:**
```bash
curl -X POST http://localhost:8002/config \
  -H "Content-Type: application/json" \
  -d '{
    "attack": 0.001,
    "decay": 0.0,
    "sustain": 1.0,
    "release": 0.1,
    "waveform": "square",
    "volume": 0.5
  }'
```

## MIDI File Upload (Python Only)

```bash
curl -X POST http://localhost:8000/midi/upload \
  -F "file=@path/to/your/song.mid"
```

Expected response:
```json
{
  "status": "success",
  "file_id": "midi_0",
  "filename": "song.mid",
  "events_count": 250,
  "events": [
    {
      "timestamp": 0.0,
      "note": "C4",
      "velocity": 100,
      "type": "note_on"
    },
    ...
  ]
}
```

**Get MIDI Events:**
```bash
curl http://localhost:8000/midi/midi_0/events
```

## WebSocket Testing

### Using websocat (CLI tool)

Install websocat:
```bash
# macOS
brew install websocat

# Linux
cargo install websocat
```

**Connect to Python WebSocket:**
```bash
websocat ws://localhost:8000/ws/realtime
```

Then send:
```json
{
  "type": "note",
  "data": {
    "note": "C4",
    "velocity": 0.8,
    "duration": 1.0
  }
}
```

**Connect to Go WebSocket:**
```bash
websocat ws://localhost:8001/ws/realtime
```

### Using JavaScript

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/realtime');

ws.onopen = () => {
  // Send note request
  ws.send(JSON.stringify({
    type: 'note',
    data: {
      note: 'A4',
      velocity: 0.8,
      duration: 1.0
    }
  }));
};

ws.onmessage = (event) => {
  const response = JSON.parse(event.data);
  console.log('Received:', response);
};
```

## Python Test Script

Create `test_backend.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Test health
response = requests.get(f"{BASE_URL}/health")
print("Health:", response.json())

# Test synthesis
note_request = {
    "note": "C4",
    "velocity": 0.8,
    "duration": 1.0
}
response = requests.post(f"{BASE_URL}/synthesize", json=note_request)
print("Synthesis:", response.json())

# Test config update
config = {
    "attack": 0.01,
    "decay": 0.2,
    "sustain": 0.5,
    "release": 1.5,
    "waveform": "sawtooth",
    "volume": 0.7
}
response = requests.post(f"{BASE_URL}/config", json=config)
print("Config update:", response.json())

# Get config
response = requests.get(f"{BASE_URL}/config")
print("Current config:", response.json())
```

Run:
```bash
python test_backend.py
```

## JavaScript/Node.js Test Script

Create `test_backend.js`:

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8001';

async function testBackend() {
  try {
    // Test health
    let response = await axios.get(`${BASE_URL}/health`);
    console.log('Health:', response.data);

    // Test synthesis
    response = await axios.post(`${BASE_URL}/synthesize`, {
      note: 'D4',
      velocity: 0.75,
      duration: 1.5
    });
    console.log('Synthesis:', response.data);

    // Update config
    response = await axios.post(`${BASE_URL}/config`, {
      attack: 0.005,
      decay: 0.15,
      sustain: 0.4,
      release: 1.2,
      waveform: 'triangle',
      volume: 0.65
    });
    console.log('Config update:', response.data);

    // Get config
    response = await axios.get(`${BASE_URL}/config`);
    console.log('Current config:', response.data);

  } catch (error) {
    console.error('Error:', error.message);
  }
}

testBackend();
```

Run:
```bash
npm install axios
node test_backend.js
```

## Load Testing

### Using Apache Bench (ab)

Test synthesis endpoint:
```bash
# 100 requests, 10 concurrent
ab -n 100 -c 10 -p note.json -T application/json http://localhost:8000/synthesize
```

Create `note.json`:
```json
{
  "note": "C4",
  "velocity": 0.8,
  "duration": 1.0
}
```

### Using wrk

```bash
# 30 second test, 4 threads, 10 connections
wrk -t4 -c10 -d30s --latency http://localhost:8000/health
```

With POST requests:
```bash
wrk -t4 -c10 -d30s --latency \
  -s post.lua \
  http://localhost:8001/synthesize
```

Create `post.lua`:
```lua
wrk.method = "POST"
wrk.body = '{"note":"C4","velocity":0.8,"duration":1.0}'
wrk.headers["Content-Type"] = "application/json"
```

## Performance Comparison Script

Create `benchmark.sh`:

```bash
#!/bin/bash

echo "Benchmarking all backends..."

# Function to test latency
test_latency() {
  local url=$1
  local name=$2
  
  echo "Testing $name..."
  time for i in {1..10}; do
    curl -s -X POST $url \
      -H "Content-Type: application/json" \
      -d '{"note":"C4","velocity":0.8,"duration":1.0}' > /dev/null
  done
}

# Test each backend
test_latency "http://localhost:8000/synthesize" "Python"
test_latency "http://localhost:8001/synthesize" "Go"
test_latency "http://localhost:8002/synthesize" "Rust"
```

Run:
```bash
chmod +x benchmark.sh
./benchmark.sh
```

## Troubleshooting

### Connection Refused
```bash
# Check if backend is running
ps aux | grep python  # For Python
ps aux | grep piano   # For Go/Rust

# Check port availability
lsof -i :8000
lsof -i :8001
lsof -i :8002
```

### CORS Errors
All backends have CORS enabled. If you still see errors:
```bash
# Test with curl to verify backend works
curl -v -X POST http://localhost:8000/synthesize \
  -H "Content-Type: application/json" \
  -d '{"note":"C4","velocity":0.8,"duration":1.0}'
```

### Invalid JSON
Ensure JSON is properly formatted:
```bash
# Use jq to validate
echo '{"note":"C4","velocity":0.8}' | jq .

# Pretty print
curl http://localhost:8000/health | jq .
```

## Expected Performance Metrics

| Metric | Python | Go | Rust |
|--------|--------|----|----- |
| Health check | <10ms | <5ms | <3ms |
| Note synthesis | 20-30ms | 10-15ms | 8-12ms |
| Config update | <5ms | <3ms | <2ms |
| Concurrent requests (100) | 5s | 2s | 1.5s |

---

Happy testing! 🎹
