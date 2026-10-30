"""Untested sketch. Symmetric linear INT4 quantisation in plain numpy, the way README §4 does it on a whiteboard.

Run:  python int4_by_hand.py
The single-weight check from §4 is given (0.37 -> 3 -> 0.428571). The block functions are TODO(learner).
"""

import numpy as np

QMIN, QMAX = -8, 7  # 4-bit signed range


def scale_for(block: np.ndarray) -> float:
    """Symmetric scale for one block: max |w| / QMAX. For a block spanning [-1, 1] this is 1/7."""
    # TODO(learner)
    raise NotImplementedError


def quantise(block: np.ndarray, scale: float) -> np.ndarray:
    """Round w / scale to the nearest integer and clip to [QMIN, QMAX]. Return int8 holding 4-bit values."""
    # TODO(learner)
    raise NotImplementedError


def dequantise(q: np.ndarray, scale: float) -> np.ndarray:
    """q * scale, back to float32."""
    # TODO(learner)
    raise NotImplementedError


def single_weight_check(w: float = 0.37) -> None:
    """The §4 example, no functions needed, so the arithmetic is on the page."""
    scale = 1.0 / QMAX  # 0.142857 for weights in [-1, 1]
    q = max(QMIN, min(QMAX, round(w / scale)))  # 3
    deq = q * scale  # 0.428571
    print(
        f"scale={scale:.6f} q={q} ({q & 0xF:04b}) deq={deq:.6f} err={deq - w:+.4f} ({abs(deq - w) / w:.1%})"
    )
    print(
        "bits: FP32 32 -> INT4 4 = 87.5% smaller; the error is why you run the G05 evalset after quantising"
    )


if __name__ == "__main__":
    single_weight_check()
    rng = np.random.default_rng(7)
    block = rng.uniform(-1.0, 1.0, size=32).astype(
        np.float32
    )  # one 32-value block, the granularity per-block schemes use
    try:
        s = scale_for(block)
        q = quantise(block, s)
        back = dequantise(q, s)
        err = np.abs(back - block)
        print(
            f"block of {block.size}: scale={s:.6f} mean abs err={err.mean():.4f} max abs err={err.max():.4f}"
        )
        print(
            "try: split the block into two halves with their own scale and compare the mean error (per-block scaling)"
        )
    except NotImplementedError:
        print(
            "block functions are TODO(learner); the single-weight check above is the whiteboard version"
        )
