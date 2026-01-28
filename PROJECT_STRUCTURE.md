# Project Structure

```
piano-app/
│
├── 📱 frontend/
│   └── piano.html                    # React-based 128-key piano interface
│                                     # - Neon cyberpunk design
│                                     # - MIDI device support
│                                     # - Real-time synthesis with Tone.js
│                                     # - Frequency visualizer
│
├── 🐍 backend-python/               # MICROSERVICES ARCHITECTURE
│   ├── main.py                      # FastAPI application
│   │   ├── AudioSynthesizer         # Service: Waveform generation
│   │   ├── MIDIProcessor            # Service: MIDI file parsing
│   │   └── FileManager              # Service: File storage
│   ├── requirements.txt             # Python dependencies
│   └── Dockerfile                   # Container definition
│
├── 🔷 backend-go/                   # PIPELINE ARCHITECTURE
│   ├── main.go                      # Concurrent pipeline
│   │   ├── NoteGenerator            # Stage 1: Frequency calculation
│   │   ├── WaveformGenerator        # Stage 2: Audio synthesis
│   │   └── EnvelopeProcessor        # Stage 3: ADSR envelope
│   ├── go.mod                       # Go module definition
│   ├── go.sum                       # Dependency checksums
│   └── Dockerfile                   # Container definition
│
├── 🦀 backend-rust/                 # ACTOR-BASED ARCHITECTURE
│   ├── src/
│   │   └── main.rs                  # Actix actor system
│   │       ├── FrequencyCalculator  # Actor: Note frequencies
│   │       ├── WaveformGenerator    # Actor: Sample generation
│   │       ├── EnvelopeProcessor    # Actor: ADSR processing
│   │       └── SynthesisCoordinator # Actor: System orchestration
│   ├── Cargo.toml                   # Rust package manifest
│   └── Dockerfile                   # Container definition
│
├── 📚 Documentation/
│   ├── README.md                    # Main documentation
│   ├── ARCHITECTURE.md              # Detailed architecture guide
│   └── TESTING.md                   # API testing guide
│
├── 🚀 Deployment/
│   ├── docker-compose.yml           # Multi-container setup
│   └── start.sh                     # Quick start script
│
└── 📊 Project Stats/
    ├── Total Files: 15+
    ├── Languages: JavaScript, Python, Go, Rust
    ├── Total Lines: 3000+
    └── Architectures: 3 distinct patterns
```

## File Descriptions

### Frontend Files

**piano.html** (700+ lines)
- Complete React application in a single file
- Tone.js integration for audio synthesis
- Web MIDI API for hardware keyboard support
- Custom neon UI design (no generic AI aesthetics)
- Real-time frequency visualization
- ADSR envelope controls
- Multiple waveform types

### Python Backend Files

**main.py** (400+ lines)
```python
# Key Components:
- FastAPI application server
- AudioSynthesizer class (waveform generation)
- MIDIProcessor class (MIDI parsing)
- FileManager class (storage management)
- WebSocket support for real-time
- RESTful API endpoints
```

**requirements.txt**
```
fastapi==0.104.1      # Web framework
uvicorn==0.24.0       # ASGI server
websockets==12.0      # WebSocket support
numpy==1.24.3         # Audio processing
pydantic==2.5.0       # Data validation
```

### Go Backend Files

**main.go** (600+ lines)
```go
// Key Components:
- HTTP server with Gorilla Mux
- Three-stage concurrent pipeline
- Channel-based communication
- sync.WaitGroup coordination
- Configuration management
- WebSocket handler
```

**go.mod**
```
module piano-backend-go
go 1.21

require (
    github.com/gorilla/mux v1.8.1
    github.com/gorilla/websocket v1.5.1
)
```

### Rust Backend Files

**main.rs** (800+ lines)
```rust
// Key Components:
- Actix actor system
- Four specialized actors
- Message-passing architecture
- Actor pools (3 instances each)
- HTTP server with Actix-web
- Type-safe message handling
```

**Cargo.toml**
```toml
[dependencies]
actix = "0.13"
actix-web = "4.4"
actix-web-actors = "4.2"
actix-cors = "0.7"
serde = { version = "1.0", features = ["derive"] }
```

## Architecture Comparison

```
┌─────────────────────────────────────────────────────────────┐
│                    PYTHON - MICROSERVICES                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Audio      │  │    MIDI      │  │    File      │    │
│  │ Synthesizer  │  │  Processor   │  │   Manager    │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│         ▲                 ▲                 ▲             │
│         └─────────────────┴─────────────────┘             │
│                      FastAPI                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      GO - PIPELINE                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Note Request                                               │
│       ↓                                                     │
│  ┌──────────┐  channel  ┌──────────┐  channel ┌─────────┐ │
│  │   Note   │─────────→ │ Waveform │─────────→│Envelope │ │
│  │Generator │           │Generator │          │Processor│ │
│  └──────────┘           └──────────┘          └─────────┘ │
│                                                      ↓     │
│                                                Audio Buffer│
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     RUST - ACTORS                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│               ┌──────────────────┐                         │
│               │   Synthesis      │                         │
│               │  Coordinator     │                         │
│               └────────┬─────────┘                         │
│                        │                                   │
│          ┌─────────────┼─────────────┐                    │
│          ▼             ▼             ▼                    │
│     ┌────────┐   ┌──────────┐  ┌──────────┐             │
│     │ Freq   │   │ Waveform │  │ Envelope │             │
│     │  Calc  │   │Generator │  │Processor │             │
│     └────────┘   └──────────┘  └──────────┘             │
│     (3 actors)   (3 actors)    (3 actors)               │
└─────────────────────────────────────────────────────────────┘
```

## Key Features by File

### piano.html Features
✅ 128 keys (11 octaves)
✅ ADSR envelope control
✅ 4 waveform types
✅ MIDI device integration
✅ MIDI file upload interface
✅ Real-time frequency visualization
✅ Neon cyberpunk UI theme
✅ Touch-responsive keys
✅ Volume control
✅ Backend selection

### Python Backend Features
✅ RESTful API
✅ WebSocket support
✅ MIDI file parsing
✅ File storage management
✅ NumPy audio processing
✅ ADSR envelope synthesis
✅ Service-oriented architecture
✅ Async request handling

### Go Backend Features
✅ Concurrent pipeline processing
✅ Channel-based communication
✅ Buffered stages (100 items)
✅ Low-latency synthesis
✅ Configuration hot-reload
✅ WebSocket support
✅ Gorilla toolkit integration
✅ Efficient memory usage

### Rust Backend Features
✅ Actor-based concurrency
✅ Message passing
✅ Type-safe architecture
✅ Actor pools (3x parallelism)
✅ Fault isolation
✅ Zero-cost abstractions
✅ Memory safety guarantees
✅ High performance

## Lines of Code Breakdown

```
Language          Files    Lines    Percentage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
JavaScript/HTML      1      700      23.3%
Python               1      400      13.3%
Go                   1      600      20.0%
Rust                 1      800      26.7%
Documentation        3      500      16.7%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total               7+     3000+     100%
```

## Deployment Options

1. **Local Development**
   - Open piano.html directly
   - Run backends individually
   - Use start.sh script

2. **Docker Compose**
   - All services in containers
   - Networked backend communication
   - Nginx for frontend

3. **Individual Containers**
   - Python: Port 8000
   - Go: Port 8001
   - Rust: Port 8002
   - Frontend: Port 80

4. **Cloud Deployment**
   - AWS ECS/EKS
   - Google Cloud Run
   - Azure Container Instances
   - Kubernetes

## Development Workflow

```
1. Design Phase
   ├── Architecture selection
   ├── API design
   └── UI/UX mockups

2. Implementation Phase
   ├── Frontend development
   ├── Backend #1 (Python)
   ├── Backend #2 (Go)
   └── Backend #3 (Rust)

3. Testing Phase
   ├── Unit tests
   ├── Integration tests
   ├── Load tests
   └── Cross-backend validation

4. Deployment Phase
   ├── Containerization
   ├── CI/CD pipeline
   └── Production deployment
```

---

This structure demonstrates three fundamentally different approaches to the same problem, allowing developers to compare and contrast architectural patterns.
