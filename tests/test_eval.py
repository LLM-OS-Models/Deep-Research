from __future__ import annotations
import json
from pathlib import Path
from unittest.mock import MagicMock
from llm_os_eval.schemas.sample import EvalSample
from llm_os_eval.schemas.result import EvalResult
from llm_os_eval.graders.deep_research import DeepResearchEvaluator

SAMPLES_PATH = Path(__file__).parent.parent / "eval" / "internal" / "v0.jsonl"


def _load_samples():
    samples = []
    with open(SAMPLES_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                samples.append(EvalSample.model_validate_json(line))
    return samples


def _make_runner_mock(response_text=""):
    runner = MagicMock()
    runner.generate.return_value = {
        "text": response_text,
        "tool_calls": [],
        "latency_ms": 100,
        "input_tokens": 10,
        "output_tokens": 20,
    }
    return runner


class TestSchemaValidation:
    def test_jsonl_schema_valid(self):
        samples = _load_samples()
        assert len(samples) >= 2
        for s in samples:
            assert s.task_type == "deep_research"
            assert s.difficulty in ("easy", "medium", "hard")
            assert s.user_query


class TestGraderIntegration:
    def setup_method(self):
        self.samples = _load_samples()
        self.runner = _make_runner_mock()
        self.evaluator = DeepResearchEvaluator(
            runner=self.runner, model_name="test", checkpoint_name="base"
        )

    def test_build_prompt(self):
        for sample in self.samples:
            sys_prompt, user_prompt = self.evaluator.build_prompt(sample)
            assert sample.user_query in user_prompt

    def test_grade_returns_metrics(self):
        mock_output = (
            "ANSWER: Terminal-Bench와 Terminal-Bench 2.0은 대표적인 오픈소스 "
            "terminal agent 벤치마크입니다.\n"
            "CITATIONS: [https://github.com/terminal-bench]"
        )
        for sample in self.samples:
            result = EvalResult(
                run_id="test",
                sample_id=sample.sample_id,
                task_type=sample.task_type,
                model_name="test",
                checkpoint_name="base",
                prompt_version="v1",
                raw_output=mock_output,
            )
            graded = self.evaluator.grade(sample, result)
            assert len(graded.metric_values) > 0
            # At least one metric should be non-zero
            assert any(v > 0 for v in graded.metric_values.values())
            # Verify key metrics are present
            assert "answer_accuracy" in graded.metric_values
            assert "answer_accuracy_proxy" in graded.metric_values
            assert "citation_support" in graded.metric_values
            assert "citation_support_proxy" in graded.metric_values
