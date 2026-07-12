#!/usr/bin/env python3
"""보이스별 TTS 발화 속도 캘리브레이션 — sound-music.md §4 KR VO 예산의 [PROVISIONAL] 해제 경로.

사용법:
  1. 캘리브레이션 문장 1개를 해당 보이스로 TTS 렌더(audio_tts) → wav/mp3 저장
  2. python3 scripts/calibrate_tts_rate.py <audio> --text "<렌더한 문장>"
  3. 출력된 보이스별 syl/s 상수와 :15/:30/:60 예산을 production_manifest 노트에 기록

원리: ffprobe 실측 길이 ÷ 음절 수 = 그 보이스의 실제 syl/s.
문헌값(낭독 3.3–3.5 syl/s) 대신 측정 상수를 쓰면 사전 예산 게이트(D10)가 보이스에 정확히 맞는다.
EN 텍스트가 섞이면 단어 단위(wpm)도 함께 출력한다.
"""
import argparse
import re
import subprocess
import sys

SHAVE = 0.9  # 브레스 셰이브 — 예산은 원시 속도의 ~90% (sound-music.md §4)
DURATIONS = (15, 30, 60)


def probe_duration(path: str) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"[calibrate] ffprobe 실패: {r.stderr.strip()[-300:]}")
    return float(r.stdout.strip())


def count_units(text: str) -> tuple[int, int]:
    """(한글 음절 수, 라틴 단어 수). 숫자는 자리수당 1음절로 근사(한국어 낭독 관행)."""
    hangul = len(re.findall(r"[가-힣]", text))
    digits = len(re.findall(r"\d", text))
    latin_words = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text))
    return hangul + digits, latin_words


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio", help="캘리브레이션 문장의 TTS 렌더 파일")
    ap.add_argument("--text", required=True, help="렌더에 사용한 문장(원문 그대로)")
    ap.add_argument("--voice", default=None, help="보이스 이름(기록용)")
    args = ap.parse_args()

    dur = probe_duration(args.audio)
    syl, words = count_units(args.text)
    if dur <= 0 or (syl == 0 and words == 0):
        sys.exit("[calibrate] 길이 또는 텍스트 단위가 0 — 입력 확인")

    label = f" ({args.voice})" if args.voice else ""
    print(f"[calibrate]{label} 길이 {dur:.2f}s · 한글 {syl}음절 · 라틴 {words}단어")
    if syl:
        sps = syl / dur
        print(f"  KR: {sps:.2f} syl/s (측정) → 예산(×{SHAVE:.0%} 셰이브): "
              + " · ".join(f":{d}≈{int(sps * d * SHAVE)}음절" for d in DURATIONS))
    if words:
        wpm = words / dur * 60
        print(f"  EN: {wpm:.0f} wpm (측정) → 예산(×{SHAVE:.0%} 셰이브): "
              + " · ".join(f":{d}≈{int(wpm / 60 * d * SHAVE)}w" for d in DURATIONS))
    print("  → production_manifest 노트에 기록하고, 이후 이 보이스의 D10 예산 게이트에 사용")


if __name__ == "__main__":
    main()
