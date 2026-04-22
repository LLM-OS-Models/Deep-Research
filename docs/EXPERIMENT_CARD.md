# Experiment Card: Deep-Research

## task_type
`deep_research`

## 목적
브라우징/리서치형 에이전트 실험을 통해 내부 평가 결과와 외부 deep-research 계열 비교선의 방향성을 확인한다.

## 핵심 지표
- answer_accuracy_proxy — 답변 존재 프록시 (길이 >= 20자, 0/1)
- answer_accuracy — 필수 키워드 커버리지 (0~1)
- citation_support_proxy — 인용 존재 프록시 (0/1)
- citation_support — 필수 인용 커버리지 (0~1)

## 평가 실행
```bash
bash eval/run_phase1.sh
bash eval/run_phase2.sh
```

## 평가 모델
- Phase 1: 8개 모델
- Phase 2: Qwen3.6-27B + LFM 모델
