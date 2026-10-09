"""Paint out the stage label + stepper band (rows Y0..Y1) in Finny_Project_2_V1.mp4."""
import sys, subprocess, numpy as np
src, dst = sys.argv[1], sys.argv[2]
W_, H_ = 720, 1280
Y0, Y1 = 84, 131          # band holding "NN · STAGE" label and stepper dashes
X0, X1, FEA = 150, 570, 24  # columns to repaint, with soft horizontal feather
F0, F1 = 89, 3149         # frames that carry the label (title-card slide and end card untouched)
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W_}x{H_}", "-r", "24", "-i", "-",
                        "-i", src, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
                        "-c:a", "copy", "-movflags", "+faststart", "-shortest", dst], stdin=subprocess.PIPE)
h = Y1 - Y0 + 1
wy = np.linspace(0, 1, h + 2)[1:-1][:, None, None]
xm = np.zeros(W_, np.float32); xm[X0:X1] = 1
ramp = np.linspace(0, 1, FEA); xm[X0 - FEA:X0] = ramp; xm[X1:X1 + FEA] = ramp[::-1]
xm = xm[None, :, None]
size = W_ * H_ * 3; i = 0
while True:
    buf = dec.stdout.read(size)
    if len(buf) < size: break
    if F0 <= i <= F1:
        f = np.frombuffer(buf, np.uint8).reshape(H_, W_, 3).astype(np.float32)
        top = f[Y0 - 3:Y0].mean(0, keepdims=True); bot = f[Y1 + 1:Y1 + 4].mean(0, keepdims=True)
        fill = top * (1 - wy) + bot * wy
        f[Y0:Y1 + 1] = fill * xm + f[Y0:Y1 + 1] * (1 - xm)
        buf = np.clip(f + 0.5, 0, 255).astype(np.uint8).tobytes()
    enc.stdin.write(buf); i += 1
enc.stdin.close(); enc.wait(); print("frames", i)
