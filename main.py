"""
Python Backend - Microservices Architecture
Uses FastAPI with separate services for audio synthesis, MIDI processing, and file management
"""

from fastapi import FastAPI, WebSocket, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
import asyncio
import json
from dataclasses import dataclass
import wave
import io

app = FastAPI(title="Piano Synthesizer Backend - Python")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Data Models ====================

class NoteRequest(BaseModel):
    note: str
    velocity: float = 0.8
    duration: float = 1.0

class SynthConfig(BaseModel):
    attack: float = 0.005
    decay: float = 0.1
    sustain: float = 0.3
    release: float = 1.0
    waveform: str = "sine"
    volume: float = 0.5

@dataclass
class MIDIEvent:
    timestamp: float
    note: int
    velocity: int
    event_type: str  # 'note_on' or 'note_off'

# ==================== Audio Synthesis Service ====================

class AudioSynthesizer:
    """Microservice for audio synthesis"""
    
    SAMPLE_RATE = 44100
    NOTE_FREQUENCIES = {
        'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
        'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
        'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
    }
    
    def __init__(self):
        self.config = SynthConfig()
    
    def update_config(self, config: SynthConfig):
        self.config = config
    
    def generate_waveform(self, frequency: float, duration: float, waveform: str = "sine") -> np.ndarray:
        """Generate a waveform at the specified frequency"""
        t = np.linspace(0, duration, int(self.SAMPLE_RATE * duration))
        
        if waveform == "sine":
            wave = np.sin(2 * np.pi * frequency * t)
        elif waveform == "square":
            wave = np.sign(np.sin(2 * np.pi * frequency * t))
        elif waveform == "sawtooth":
            wave = 2 * (t * frequency - np.floor(0.5 + t * frequency))
        elif waveform == "triangle":
            wave = 2 * np.abs(2 * (t * frequency - np.floor(0.5 + t * frequency))) - 1
        else:
            wave = np.sin(2 * np.pi * frequency * t)
        
        return wave
    
    def apply_adsr_envelope(self, wave: np.ndarray, duration: float) -> np.ndarray:
        """Apply ADSR envelope to the waveform"""
        total_samples = len(wave)
        attack_samples = int(self.config.attack * self.SAMPLE_RATE)
        decay_samples = int(self.config.decay * self.SAMPLE_RATE)
        release_samples = int(self.config.release * self.SAMPLE_RATE)
        
        envelope = np.ones(total_samples)
        
        # Attack
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # Decay
        if decay_samples > 0 and attack_samples + decay_samples < total_samples:
            decay_end = attack_samples + decay_samples
            envelope[attack_samples:decay_end] = np.linspace(1, self.config.sustain, decay_samples)
        
        # Sustain
        sustain_start = attack_samples + decay_samples
        sustain_end = total_samples - release_samples
        if sustain_start < sustain_end:
            envelope[sustain_start:sustain_end] = self.config.sustain
        
        # Release
        if release_samples > 0:
            envelope[-release_samples:] = np.linspace(self.config.sustain, 0, release_samples)
        
        return wave * envelope * self.config.volume
    
    def synthesize_note(self, note: str, velocity: float, duration: float) -> bytes:
        """Synthesize a single note and return as WAV bytes"""
        # Parse note (e.g., "C4" -> "C" and octave 4)
        note_name = note[:-1] if note[-1].isdigit() else note
        octave = int(note[-1]) if note[-1].isdigit() else 4
        
        # Calculate frequency
        base_freq = self.NOTE_FREQUENCIES.get(note_name, 440.0)
        frequency = base_freq * (2 ** (octave - 4))
        
        # Generate waveform
        wave = self.generate_waveform(frequency, duration, self.config.waveform)
        
        # Apply envelope
        wave = self.apply_adsr_envelope(wave, duration)
        
        # Apply velocity
        wave = wave * velocity
        
        # Convert to 16-bit PCM
        wave_int = np.int16(wave * 32767)
        
        # Create WAV file in memory
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.SAMPLE_RATE)
            wav_file.writeframes(wave_int.tobytes())
        
        return wav_buffer.getvalue()

# ==================== MIDI Processing Service ====================

class MIDIProcessor:
    """Microservice for MIDI file processing"""
    
    @staticmethod
    def parse_midi_file(file_data: bytes) -> List[MIDIEvent]:
        """Parse MIDI file and extract events"""
        # This is a simplified parser - in production, use mido library
        events = []
        
        # For demonstration, generate sample events
        # In real implementation, parse the actual MIDI file format
        for i in range(10):
            events.append(MIDIEvent(
                timestamp=i * 0.5,
                note=60 + i,
                velocity=100,
                event_type='note_on'
            ))
            events.append(MIDIEvent(
                timestamp=i * 0.5 + 0.4,
                note=60 + i,
                velocity=0,
                event_type='note_off'
            ))
        
        return events
    
    @staticmethod
    def midi_note_to_name(midi_note: int) -> str:
        """Convert MIDI note number to note name"""
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = (midi_note // 12) - 1
        note_index = midi_note % 12
        return f"{notes[note_index]}{octave}"

# ==================== File Management Service ====================

class FileManager:
    """Microservice for file storage and management"""
    
    def __init__(self):
        self.midi_files = {}
        self.audio_files = {}
    
    def store_midi_file(self, filename: str, data: bytes) -> str:
        """Store MIDI file and return ID"""
        file_id = f"midi_{len(self.midi_files)}"
        self.midi_files[file_id] = {
            'filename': filename,
            'data': data,
            'size': len(data)
        }
        return file_id
    
    def get_midi_file(self, file_id: str) -> Optional[bytes]:
        """Retrieve MIDI file data"""
        return self.midi_files.get(file_id, {}).get('data')
    
    def store_audio_file(self, filename: str, data: bytes) -> str:
        """Store audio file and return ID"""
        file_id = f"audio_{len(self.audio_files)}"
        self.audio_files[file_id] = {
            'filename': filename,
            'data': data,
            'size': len(data)
        }
        return file_id

# ==================== Service Instances ====================

synthesizer = AudioSynthesizer()
midi_processor = MIDIProcessor()
file_manager = FileManager()

# ==================== API Endpoints ====================

@app.get("/")
async def root():
    return {
        "service": "Piano Synthesizer - Python Backend",
        "architecture": "Microservices",
        "version": "1.0.0",
        "services": ["audio_synthesis", "midi_processing", "file_management"]
    }

@app.post("/synthesize")
async def synthesize_note(request: NoteRequest):
    """Synthesize a single note"""
    try:
        audio_data = synthesizer.synthesize_note(
            request.note,
            request.velocity,
            request.duration
        )
        
        # Store the audio file
        file_id = file_manager.store_audio_file(
            f"{request.note}.wav",
            audio_data
        )
        
        return {
            "status": "success",
            "file_id": file_id,
            "note": request.note,
            "size": len(audio_data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/config")
async def update_config(config: SynthConfig):
    """Update synthesizer configuration"""
    synthesizer.update_config(config)
    return {
        "status": "success",
        "config": config.dict()
    }

@app.get("/config")
async def get_config():
    """Get current synthesizer configuration"""
    return synthesizer.config.dict()

@app.post("/midi/upload")
async def upload_midi(file: UploadFile = File(...)):
    """Upload and process MIDI file"""
    try:
        file_data = await file.read()
        
        # Store file
        file_id = file_manager.store_midi_file(file.filename, file_data)
        
        # Parse MIDI events
        events = midi_processor.parse_midi_file(file_data)
        
        return {
            "status": "success",
            "file_id": file_id,
            "filename": file.filename,
            "events_count": len(events),
            "events": [
                {
                    "timestamp": e.timestamp,
                    "note": midi_processor.midi_note_to_name(e.note),
                    "velocity": e.velocity,
                    "type": e.event_type
                }
                for e in events[:10]  # Return first 10 events as sample
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/midi/{file_id}/events")
async def get_midi_events(file_id: str):
    """Get events from a stored MIDI file"""
    file_data = file_manager.get_midi_file(file_id)
    if not file_data:
        raise HTTPException(status_code=404, detail="File not found")
    
    events = midi_processor.parse_midi_file(file_data)
    return {
        "file_id": file_id,
        "events": [
            {
                "timestamp": e.timestamp,
                "note": midi_processor.midi_note_to_name(e.note),
                "velocity": e.velocity,
                "type": e.event_type
            }
            for e in events
        ]
    }

@app.websocket("/ws/realtime")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time note synthesis"""
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "note":
                note_request = NoteRequest(**message.get("data", {}))
                audio_data = synthesizer.synthesize_note(
                    note_request.note,
                    note_request.velocity,
                    note_request.duration
                )
                
                await websocket.send_json({
                    "type": "audio",
                    "note": note_request.note,
                    "size": len(audio_data)
                })
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "audio_synthesis": "operational",
            "midi_processing": "operational",
            "file_management": "operational"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
