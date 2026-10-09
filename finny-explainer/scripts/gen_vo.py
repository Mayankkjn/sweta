import sys,json,os,numpy as np,soundfile as sf
sys.path.insert(0,os.path.dirname(__file__))
from spec import SECTIONS
from kokoro_onnx import Kokoro
M,out=sys.argv[1],sys.argv[2]; os.makedirs(out,exist_ok=True)
k=Kokoro(M+"/kokoro-v1.0.onnx",M+"/voices-v1.0.bin")
meta=[]
for si,s in enumerate(SECTIONS):
  for li,(txt,_) in enumerate(s["lines"]):
    a,sr=k.create(txt,voice="af_heart",speed=1.05,lang="en-us")
    # trim leading/trailing silence
    idx=np.where(np.abs(a)>0.01)[0]; a=a[max(0,idx[0]-400):idx[-1]+1200]
    f=f"{out}/s{si:02d}_l{li}.wav"; sf.write(f,a,sr); meta.append(dict(s=si,l=li,file=f,dur=len(a)/sr,sr=sr,text=txt))
    print(f"{si}.{li} {len(a)/sr:5.2f}s {txt}")
json.dump(meta,open(out+"/vo.json","w"),indent=1)
print("total speech",sum(m['dur'] for m in meta))
