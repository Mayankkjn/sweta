"""Original background track for the Finny explainer (procedurally synthesised, royalty-free).
Warm, optimistic: I–vi–IV–V in C, 96 bpm. Pads + piano-like arpeggio + sub bass + soft pulse.
Usage: make_music.py out.wav duration_s [intro_end_s] [lift_start_s] [outro_start_s]"""
import sys, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

out = sys.argv[1]; DUR = float(sys.argv[2])
INTRO = float(sys.argv[3]) if len(sys.argv) > 3 else 3.7
LIFT = float(sys.argv[4]) if len(sys.argv) > 4 else 117.0
OUTRO = float(sys.argv[5]) if len(sys.argv) > 5 else 131.25
SR = 48000; BPM = 96; BEAT = 60 / BPM; BAR = 4 * BEAT
N = int((DUR + 4) * SR); t_all = np.arange(N) / SR
rng = np.random.default_rng(7)

def hz(m): return 440 * 2 ** ((m - 69) / 12)
def env_adsr(n, a, d, s, r, sustain_len):
    a, d, r = int(a * SR), int(d * SR), int(r * SR); sl = max(int(sustain_len * SR) - a - d, 0)
    e = np.concatenate([np.linspace(0, 1, a, False), np.linspace(1, s, d, False), np.full(sl, s), np.linspace(s, 0, r)])
    return e[:n] if len(e) >= n else np.pad(e, (0, n - len(e)))
def lp(x, fc, order=2): return sosfilt(butter(order, fc, "low", fs=SR, output="sos"), x)
def hp(x, fc, order=2): return sosfilt(butter(order, fc, "high", fs=SR, output="sos"), x)

# progression (2 bars each): Cmaj9, Am9, Fmaj9, Gsus2->G
CH = [
    dict(root=48, pad=[60, 64, 67, 71, 74], arp=[72, 76, 79, 83, 79, 76]),
    dict(root=45, pad=[57, 60, 64, 67, 71], arp=[69, 72, 76, 79, 76, 72]),
    dict(root=41, pad=[57, 60, 64, 65, 69], arp=[69, 72, 77, 81, 77, 72]),
    dict(root=43, pad=[55, 59, 62, 67, 69], arp=[67, 71, 74, 79, 74, 71]),
]
L = np.zeros(N); R = np.zeros(N)
def add(sig, start, pan=0.0, gain=1.0):
    i = int(start * SR); j = min(N, i + len(sig))
    if j <= i: return
    s = sig[: j - i] * gain
    L[i:j] += s * np.sqrt(0.5 * (1 - pan)); R[i:j] += s * np.sqrt(0.5 * (1 + pan))

def intensity(t):
    """0..1 arrangement curve: intro pad only, groove, lift, outro."""
    if t < INTRO: return 0.0
    if t < OUTRO: return 1.0
    return 0.0

# --- pads (whole song, chord per 2 bars) ---
seg = 2 * BAR; nseg = int(np.ceil((DUR + 2) / seg))
for k in range(nseg):
    c = CH[k % 4]; st = k * seg; n = int((seg + 1.5) * SR); tt = np.arange(n) / SR
    sig = np.zeros(n)
    for m in c["pad"]:
        f = hz(m)
        for det in (-0.12, 0.0, 0.11):
            ff = f * 2 ** (det / 12)
            sig += np.sin(2 * np.pi * ff * tt + rng.uniform(0, 6)) * 0.6 + 0.25 * np.sin(4 * np.pi * ff * tt) + 0.1 * np.sin(6 * np.pi * ff * tt)
    sig = lp(sig, 1800) * env_adsr(n, 0.9, 0.5, 0.85, 1.4, seg)
    g = 0.022 if st < INTRO else (0.016 if st < OUTRO else 0.02)
    add(sig, st, pan=-0.15, gain=g); add(lp(sig, 900), st + 0.012, pan=0.2, gain=g * 0.8)

# --- piano-like arpeggio (8th notes) ---
def pluck(f, length=1.6):
    n = int(length * SR); tt = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * h * tt) * np.exp(-tt * (2.2 + h * 1.4)) for h, a in ((1, 1), (2, 0.45), (3, 0.2), (4, 0.1)))
    att = np.minimum(tt / 0.004, 1)
    return s * att
eighth = BEAT / 2
t = INTRO
while t < OUTRO - 0.05:
    k = int(t // seg); c = CH[k % 4]; step = int(round((t - k * seg) / eighth))
    m = c["arp"][step % len(c["arp"])]
    vel = 0.75 + 0.25 * (step % 4 == 0) + rng.uniform(-0.08, 0.08)
    lift = 1.15 if t >= LIFT else 1.0
    add(pluck(hz(m)), t + rng.uniform(-0.006, 0.006), pan=0.35 * np.sin(step * 0.9), gain=0.05 * vel * lift)
    t += eighth

# --- intro bells: gentle sparkle under the title card ---
for i, m in enumerate([84, 88, 91, 95, 91]):
    add(pluck(hz(m), 2.5), 0.4 + i * 0.55, pan=(-0.4 + i * 0.2), gain=0.035)

# --- sub bass (root on beats 1 & 3, octave pickup) ---
def bass(f, length):
    n = int(length * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(4 * np.pi * f * tt)) * env_adsr(n, 0.01, 0.15, 0.7, 0.12, length)
t = INTRO
while t < OUTRO - 0.05:
    k = int(t // seg); c = CH[k % 4]; b = int(round((t - k * seg) / BEAT)) % 4
    if b in (0, 2): add(lp(bass(hz(c["root"] - 12), BEAT * 1.7), 400), t, gain=0.045)
    t += BEAT

# --- soft pulse: kick on 1 & 3, shaker on off-beats ---
def kick():
    n = int(0.35 * SR); tt = np.arange(n) / SR
    f = 110 * np.exp(-tt * 25) + 45
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9)
def shaker():
    n = int(0.09 * SR); tt = np.arange(n) / SR
    return hp(rng.standard_normal(n), 6000) * np.exp(-tt * 55)
t = INTRO + 2 * BAR  # let the groove breathe in
while t < OUTRO - 0.05:
    b = int(round((t - INTRO) / (BEAT / 2))) % 8
    if b in (0, 4): add(hp(kick(), 50), t, gain=0.06)
    if b % 2 == 1: add(shaker(), t, pan=0.25, gain=0.014 * (1.25 if t >= LIFT else 1.0))
    t += BEAT / 2

# --- lift: high string-like layer from the advisory section ---
k0 = int(LIFT // seg)
for k in range(k0, int(OUTRO // seg) + 1):
    c = CH[k % 4]; st = max(k * seg, LIFT); n = int((seg + 1.2) * SR); tt = np.arange(n) / SR
    sig = sum(np.sin(2 * np.pi * hz(m + 12) * tt * (1 + 0.002 * np.sin(2 * np.pi * 5 * tt))) for m in c["pad"][1:4])
    add(lp(sig, 3000) * env_adsr(n, 1.2, 0.4, 0.8, 1.0, seg), st, pan=0.1, gain=0.012)

# --- outro: final Cmaj9 ring-out + bell ---
n = int(5 * SR); tt = np.arange(n) / SR
fin = sum(np.sin(2 * np.pi * hz(m) * tt) for m in [48, 60, 64, 67, 71, 74]) * np.exp(-tt * 0.8)
add(lp(fin, 2200), OUTRO, gain=0.03)
for i, m in enumerate([79, 84, 88]): add(pluck(hz(m), 3), OUTRO + 0.1 + i * 0.18, pan=-0.3 + 0.3 * i, gain=0.04)

# --- reverb + master ---
ir_n = int(2.2 * SR); ir_t = np.arange(ir_n) / SR
irL = rng.standard_normal(ir_n) * np.exp(-ir_t * 3.2); irR = rng.standard_normal(ir_n) * np.exp(-ir_t * 3.2)
irL = lp(irL, 5000); irR = lp(irR, 5000); irL /= np.abs(irL).sum() ** 0.5 * 9; irR /= np.abs(irR).sum() ** 0.5 * 9
wetL = fftconvolve(L, irL)[:N]; wetR = fftconvolve(R, irR)[:N]
L2 = L + 0.35 * wetL; R2 = R + 0.35 * wetR
mix = np.stack([L2, R2], 1)[: int(DUR * SR)]
fade_in = int(0.3 * SR); mix[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]
fo = int(min(2.0, DUR - OUTRO) * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
mix = np.tanh(mix / (np.abs(mix).max() * 0.9) * 1.1) * 0.85
sf.write(out, mix.astype(np.float32), SR)
print("wrote", out, mix.shape[0] / SR, "s")
