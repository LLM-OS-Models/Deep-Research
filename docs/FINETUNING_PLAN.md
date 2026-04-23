# Finetuning Plan: Deep-Research

## Current State

- `v0` 결과는 그럴듯하지만 live browsing 없는 4샘플 결과다.
- 현재 SFT 데이터 30/30이 placeholder 답변과 placeholder citation이다.
- 이 프로젝트는 파인튜닝보다 browsing stack과 citation normalization 영향이 더 크다.

## Priority

- 우선순위: 중하
- 이유: 답변 품질보다 최신성, URL 정확도, 날짜 처리, source grounding이 핵심이기 때문이다.

## Base Models

- Primary: `Qwen/Qwen3-8B`
- Secondary: `google/gemma-4-26B-A4B`
- Small pilot: `Qwen/Qwen3-4B`

## Phase 0

1. placeholder SFT 30/30을 폐기한다.
2. 답변마다 아래 필드를 가진 teacher dataset을 다시 만든다.
   - claim
   - evidence sentence
   - title
   - source URL
   - publication date
   - final answer
3. citation은 도메인명만이 아니라 실제 absolute URL로 저장한다.
4. 날짜는 반드시 절대 날짜로 정규화한다.

## Phase 1

- 목표: grounded answer + citation formatting 고정
- 학습 대상
  - 1-hop factual search
  - 2-hop synthesis
  - comparison table
  - answer + citation list
- 권장 시작점
  - `max_seq_length=4096`
  - `per_device_train_batch_size=2`
  - `gradient_accumulation_steps=4`
  - `learning_rate=1e-4`
  - `lora_r=16`

## Phase 2

- reward model 또는 GRPO를 쓸 경우 reward는 다음만 쓴다.
  - required citation hit
  - dead URL penalty
  - unsupported claim penalty
  - date mismatch penalty

## Model Notes

- `Qwen3`는 reasoning/non-thinking 전환이 가능하다.
- reasoning 성향을 유지하고 싶으면 reasoning-style 예시 비중을 유지하는 편이 낫다.
- `Gemma 4`는 standard `system/user/assistant` role을 쓰므로 dataset 포맷을 섞지 말아야 한다.

## Exit Criteria

- `answer_accuracy >= 0.9`
- `citation_support >= 0.9`
- dead URL rate `<= 5%`
- same query rerun 시 citation drift `<= 10%`
