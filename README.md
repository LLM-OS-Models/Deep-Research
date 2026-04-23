# Deep-Research

딥 리서치 에이전트 평가 트랙.

질문이 주어지면, 모델이 상세한 답변을 생성하고 신뢰할 수 있는 출처(citation)를 포함하는 능력을 평가한다. 답변 정확도와 인용 신뢰도를 모두 측정하여, 단순한 사실 나열이 아닌 근거 기반 응답을 요구한다.

## 평가 메트릭

| 메트릭 | 설명 |
|--------|------|
| `answer_accuracy_proxy` | 응답 길이 >= 20자 (0/1) |
| `answer_accuracy` | gold required_content 키워드 중 응답에 포함된 비율 (0~1) |
| `citation_support_proxy` | 인용을 포함했는지 (0/1) |
| `citation_support` | gold required_citations 중 모델 인용에 포함된 비율 (0~1) |

**성공 조건**: `answer_accuracy >= 0.5 AND citation_support > 0`

> **참고**: 평가 파이프라인은 multi-query decomposition을 지원한다. 복잡한 질문은 하위 질문으로 분해되어 각각 독립적으로 평가된 후 결과가 통합된다.

## 샘플 데이터 형식

```json
{
  "sample_id": "research_0001",
  "user_query": "최근 오픈소스 terminal agent 벤치마크 중 널리 쓰이는 것을 2개만 비교해줘.",
  "artifacts": {"allowed_tools": ["web_search", "open_page"]},
  "gold": {
    "required_content": ["Terminal-Bench", "Terminal-Bench 2.0"],
    "required_citations": ["github.com", "arxiv.org"]
  }
}
```

## 모델 출력 형식

```
ANSWER: 질문에 대한 상세한 답변
CITATIONS: [https://example.com/source1, https://arxiv.org/abs/...]
```

## 프로젝트 구조

```
Deep-Research/
├── README.md
├── pyproject.toml
├── eval/
│   ├── internal/
│   │   └── v0.jsonl        # 평가 데이터셋 (2샘플)
│   └── results/
├── tests/
└── data/
```

## 실행

```bash
uv sync

llm-os-eval run deep_research \
  --model Qwen/Qwen3-4B \
  --samples eval/internal/v0.jsonl \
  --output eval/results/Qwen3-4B_v0.jsonl \
  --base-url http://localhost:8001/v1
```

## 벤치마크 결과 (2026-04-23, Round 3)

| 모델 | Size | answer_accuracy | citation_support | 성공률 |
|------|------|----------------|-----------------|--------|
| Nemotron-Terminal-8B | 8B | 17% | **25%** | 0% |
| Qwen2.5-14B-Instruct | 14B | 17% | **25%** | 0% |
| 나머지 전체 | — | 17% | 0% | 0% |

모든 모델이 answer_accuracy 17% (6개 키워드 중 1개 매칭)를 기록한다. Citation의 경우 실제 웹 검색이 불가능한 환경에서는 도메인(github.com, arxiv.org)을 포함한 URL을 생성하기 어렵다. 답변 내용은 관련성이 있으나, 평가 기준인 특정 키워드 포함과 인용 URL 생성 요구사항을 충족하지 못한다.
