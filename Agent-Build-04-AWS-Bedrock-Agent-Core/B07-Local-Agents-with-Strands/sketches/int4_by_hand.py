"""Symmetric linear INT4 quantisation of one weight, the way §4 does it on a whiteboard. Same numbers as F07.
Prints: scale 0.142857, q=3 (0011), deq 0.428571, error 15.8 %."""
w, lo, hi = 0.37, -1.0, 1.0
qmin, qmax = -8, 7                      # 4-bit signed range
scale = max(abs(lo), abs(hi)) / qmax    # 1/7 ≈ 0.142857
q = max(qmin, min(qmax, round(w / scale)))   # 3
deq = q * scale                          # 0.428571
print(f"scale={scale:.6f} q={q} ({q & 0xF:04b}) deq={deq:.6f} err={deq - w:+.4f} ({abs(deq - w) / w:.1%})")
print("bits: FP32 32 -> INT4 4 = 87.5% smaller; GGUF Q4_K_M and MXFP4 add per-block scales to cut that error")
