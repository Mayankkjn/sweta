import sys, json, numpy as np, soundfile as sf, sherpa_onnx
M=sys.argv[1]; wav=sys.argv[2]; out=sys.argv[3]
d=M+"/sherpa-onnx-whisper-small.en/"
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d+"small.en-encoder.int8.onnx",decoder=d+"small.en-decoder.int8.onnx",tokens=d+"small.en-tokens.txt",num_threads=4)
cfg=sherpa_onnx.VadModelConfig(); cfg.silero_vad.model=M+"/silero_vad.onnx"; cfg.silero_vad.min_silence_duration=0.5; cfg.silero_vad.min_speech_duration=0.25; cfg.silero_vad.max_speech_duration=20; cfg.sample_rate=16000
vad=sherpa_onnx.VoiceActivityDetector(cfg,buffer_size_in_seconds=900)
a,sr=sf.read(wav,dtype='float32'); assert sr==16000
segs=[]
def drain():
    while not vad.empty():
        s=vad.front; st=s.start/16000; samples=np.array(s.samples,dtype=np.float32); vad.pop()
        stream=rec.create_stream(); stream.accept_waveform(16000,samples); rec.decode_stream(stream)
        t=stream.result.text.strip()
        segs.append(dict(start=round(st,2),end=round(st+len(samples)/16000,2),text=t)); print(f"[{st:7.2f}-{st+len(samples)/16000:7.2f}] {t}",flush=True)
w=512
for i in range(0,len(a),w):
    vad.accept_waveform(a[i:i+w]); drain()
vad.flush(); drain()
json.dump(segs,open(out,'w'),indent=1)
