import sys, numpy as np, soundfile as sf, sherpa_onnx, scipy.signal as ss
M=sys.argv[1]; d=M+"/sherpa-onnx-whisper-small.en/"
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d+"small.en-encoder.int8.onnx",decoder=d+"small.en-decoder.int8.onnx",tokens=d+"small.en-tokens.txt",num_threads=4)
for f in sys.argv[2:]:
    a,sr=sf.read(f,dtype='float32')
    if a.ndim>1: a=a.mean(1)
    if sr!=16000: a=ss.resample_poly(a,16000,sr).astype(np.float32)
    s=rec.create_stream(); s.accept_waveform(16000,a); rec.decode_stream(s); print(f.split('/')[-1],"|",s.result.text)
