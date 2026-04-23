# Pilot Run Sheet: Deep-Research

## Objective

- browsing stack이 아닌 모델 FT가 실제로 citation formatting과 grounded synthesis를 개선하는지 확인한다.
- 최신성 오류와 citation drift를 모델 문제와 tool 문제로 분리한다.

## Run IDs

- `RES-P0`: evidence-grounded dataset 재작성
- `RES-P1`: `Qwen3-8B` grounded answer pilot
- `RES-P2`: strict citation formatting ablation
- `RES-P3`: small model feasibility check

## Dataset Gate

- placeholder answer `0`
- placeholder citation `0`
- absolute URL only
- absolute date only
- question family split:
  - 1-hop factual
  - 2-hop synthesis
  - comparison
  - freshness-sensitive

## Model Matrix

| Run ID | Model | Context | Rank | Output Contract | Purpose |
|---|---|---:|---:|---|---|
| RES-P1 | `Qwen3-8B` | 4096 | 16 | answer + citation list | primary pilot |
| RES-P2 | `Qwen3-8B` | 4096 | 16 | answer + claim-level citations | strict citation ablation |
| RES-P3 | `Qwen3-4B` | 4096 | 16 | answer + citation list | small model floor |

## Fixed Decisions

- date normalization: absolute only
- URL: absolute only
- first stage: SFT only
- browsing-dependent failure는 model regression으로 간주하지 않음

## Primary Metrics

- `answer_accuracy`
- `citation_support`
- dead URL rate
- citation drift

## Slice Metrics

- factual split
- synthesis split
- comparison split
- freshness-sensitive split

## Accept

- `citation_support >= 0.90`
- dead URL rate `<= 5%`
- same query rerun drift `<= 10%`

## Reject

- formatting만 좋아지고 unsupported claim이 늘어남
- freshness-sensitive 질문에서 날짜 오류가 유지됨
- tool layer 문제를 model FT로 오판하는 증거가 있음

## Review Questions

1. 실패의 중심이 answer synthesis인가 citation wiring인가
2. strict claim-level citation이 실제로 필요한가
3. small model은 grounded formatting만 담당하고 synthesis는 상위 모델로 넘겨야 하는가
