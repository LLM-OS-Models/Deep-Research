# Labeling Guide: Deep-Research

## Goal

- grounded answer와 citation을 분리 가능하게 저장한다.
- 최신성, URL 정확도, 날짜 정규화를 라벨 수준에서 고정한다.

## Required Fields

- `claim_units`
- `citations.title`
- `citations.url`
- `citations.publication_date`
- `answer_format`

## Labeling Rules

- citation은 absolute URL만 허용한다.
- 날짜는 absolute date만 허용한다.
- answer 안의 각 핵심 claim은 근거 citation과 연결 가능해야 한다.
- domain name만 있는 citation은 gold로 승인하지 않는다.

## Verification

1. question family 태그 확인
2. claim unit 분리
3. citation URL 확인
4. publication date 절대 날짜 확인
5. unsupported claim 제거

## Common Mistakes

- 최신성 민감 질문인데 날짜를 상대 표현으로 저장
- source title만 있고 URL이 없음
- synthesis answer에 근거 없는 연결 문장이 섞임
