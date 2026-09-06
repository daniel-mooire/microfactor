from __future__ import annotations

import json
import multiprocessing
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from typing import Protocol

import pandas as pd

from microfactor.eval.artifacts import EvaluationArtifactStore
from microfactor.eval.calculator import (
    MetricsCalculator,
    suppress_known_evaluation_warnings,
)
from microfactor.eval.data import EvaluationDataLoader
from microfactor.eval.domain import (
    EvaluationRun,
    FactorEvaluationResult,
)
from microfactor.eval.evaluator import EvaluationSharedData, FactorEvaluator
from microfactor.eval.figures import FactorFigureWriter

FactorCompletedCallback = Callable[[int, int], None]


class EvaluationExecutor(Protocol):
    def execute(self, run: EvaluationRun) -> tuple[FactorEvaluationResult, ...]:
        ...


@dataclass
class SerialEvaluationExecutor:
    evaluator: object
    data_loader: object | None
    log_info: Callable[[str], None] | None = None
    on_factor_completed: FactorCompletedCallback | None = None

    def execute(self, run: EvaluationRun) -> tuple[FactorEvaluationResult, ...]:
        shared_data = self._load_shared_data(run)
        results: list[FactorEvaluationResult] = []
        with suppress_known_evaluation_warnings():
            for factor_name in run.config.factor_names:
                _log(self.log_info, f"evaluation_factor_started factor={factor_name}")
                try:
                    result = self.evaluator.evaluate(
                        factor_name,
                        run,
                        shared_data=shared_data,
                    )
                except Exception as exc:  # isolate one bad factor from the batch
                    _log(
                        self.log_info,
                        f"evaluation_factor_failed factor={factor_name} error={exc}",
                    )
                    result = _failed_result(run, factor_name, exc)
                results.append(result)
                done = len(results)
                if self.on_factor_completed is not None:
                    self.on_factor_completed(done, len(run.config.factor_names))
        return tuple(results)

    def _load_shared_data(self, run: EvaluationRun) -> EvaluationSharedData | None:
        if self.data_loader is None:
            return None

        config = run.config
        price_end_date = config.end_date or self.data_loader.max_factor_trade_date(
            config.factor_names,
            start_date=config.start_date,
        )
        _log(
            self.log_info,
            "evaluation_price_load_started "
            f"start_date={config.start_date} end_date={price_end_date}",
        )
        price_data = self.data_loader.load_prices(
            start_date=config.start_date,
            end_date=price_end_date,
            periods=config.periods,
            universe_name=config.universe,
        )
        _log(self.log_info, f"evaluation_price_load_finished rows={len(price_data)}")
        universe_panel = self.data_loader.load_universe(
            universe_name=config.universe,
            start_date=config.start_date,
            end_date=config.end_date,
        )
        load_tradability = getattr(self.data_loader, "load_tradability", None)
        tradability = (
            load_tradability(
                start_date=config.start_date,
                end_date=price_end_date,
                universe_name=config.universe,
            )
            if load_tradability is not None
            else None
        )
        return EvaluationSharedData(
            price_data=price_data,
            universe_panel=universe_panel,
            tradability=tradability,
        )


@dataclass
class ProcessPoolEvaluationExecutor:
    storage: object
    pro: object
    data_loader: object
    workers: int
    log_info: Callable[[str], None] | None = None
    on_factor_completed: FactorCompletedCallback | None = None

    def execute(self, run: EvaluationRun) -> tuple[FactorEvaluationResult, ...]:
        shared_data = self._load_shared_data(run)
        context = _EvaluationWorkerContext(
            storage=self.storage,
            pro=self.pro,
            run=run,
            price_data=shared_data.price_data,
            universe_panel=shared_data.universe_panel,
            tradability=shared_data.tradability,
        )
        summaries: dict[str, pd.DataFrame] = {}
        ctx = multiprocessing.get_context("spawn")
        max_workers = min(self.workers, len(run.config.factor_names))
        with ProcessPoolExecutor(
            max_workers=max_workers,
            mp_context=ctx,
            initializer=_init_evaluation_worker,
            initargs=(context,),
        ) as pool:
            for factor_name, summary in pool.map(_evaluate_factor_task, run.config.factor_names):
                _log(self.log_info, f"evaluation_factor_finished factor={factor_name}")
                summaries[factor_name] = summary
                done = len(summaries)
                if self.on_factor_completed is not None:
                    self.on_factor_completed(done, len(run.config.factor_names))

        empty = pd.DataFrame()
        return tuple(
            FactorEvaluationResult(
                factor_name=factor_name,
                clean_factor_data=empty,
                summary=summaries[factor_name],
                daily_ic=empty,
                quantile_returns=empty,
                output_dir=run.factor_dir(factor_name),
            )
            for factor_name in run.config.factor_names
        )

    def _load_shared_data(self, run: EvaluationRun) -> EvaluationSharedData:
        config = run.config
        price_end_date = config.end_date or self.data_loader.max_factor_trade_date(
            config.factor_names,
            start_date=config.start_date,
        )
        _log(
            self.log_info,
            "evaluation_price_load_started "
            f"start_date={config.start_date} end_date={price_end_date}",
        )
        price_data = self.data_loader.load_prices(
            start_date=config.start_date,
            end_date=price_end_date,
            periods=config.periods,
            universe_name=config.universe,
        )
        _log(self.log_info, f"evaluation_price_load_finished rows={len(price_data)}")
        universe_panel = self.data_loader.load_universe(
            universe_name=config.universe,
            start_date=config.start_date,
            end_date=config.end_date,
        )
        load_tradability = getattr(self.data_loader, "load_tradability", None)
        tradability = (
            load_tradability(
                start_date=config.start_date,
                end_date=price_end_date,
                universe_name=config.universe,
            )
            if load_tradability is not None
            else None
        )
        return EvaluationSharedData(
            price_data=price_data,
            universe_panel=universe_panel,
            tradability=tradability,
        )


@dataclass(frozen=True)
class _EvaluationWorkerContext:
    storage: object
    pro: object
    run: EvaluationRun
    price_data: pd.DataFrame | None
    universe_panel: pd.DataFrame | None
    tradability: pd.DataFrame | None


_WORKER_EVAL_CONTEXT: _EvaluationWorkerContext | None = None


def _init_evaluation_worker(context: _EvaluationWorkerContext) -> None:
    global _WORKER_EVAL_CONTEXT
    _WORKER_EVAL_CONTEXT = context


def _evaluate_factor_task(factor_name: str) -> tuple[str, pd.DataFrame]:
    context = _WORKER_EVAL_CONTEXT
    if context is None:
        raise RuntimeError("evaluation worker is not initialized")

    evaluator = FactorEvaluator(
        data_loader=EvaluationDataLoader(context.storage, context.pro),
        metric_calculator=MetricsCalculator(),
        artifact_store=EvaluationArtifactStore(),
        figure_writer=FactorFigureWriter(),
    )
    try:
        with suppress_known_evaluation_warnings():
            result = evaluator.evaluate(
                factor_name,
                context.run,
                shared_data=EvaluationSharedData(
                    price_data=context.price_data,
                    universe_panel=context.universe_panel,
                    tradability=context.tradability,
                ),
            )
        return factor_name, result.summary
    except Exception as exc:
        return factor_name, _failed_summary(context.run, factor_name, exc)


def _failed_summary(run: EvaluationRun, factor_name: str, exc: Exception) -> pd.DataFrame:
    period = run.config.periods[0]
    status = _failure_status(exc)
    return pd.DataFrame(
        [{
            "factor_name": factor_name,
            "period": period,
            "sample_count": 0,
            "IC Mean": float("nan"),
            "adjusted_ICIR": float("nan"),
            "directional_IC>0 %": float("nan"),
            "long_short_spread_bps": float("nan"),
            "factor_direction": 1,
            "status": status,
            "error": f"{type(exc).__name__}: {exc}",
        }]
    )


def _failed_result(run: EvaluationRun, factor_name: str, exc: Exception) -> FactorEvaluationResult:
    output_dir = run.factor_dir(factor_name)
    output_dir.mkdir(parents=True, exist_ok=True)
    status = _failure_status(exc)
    failure = {
        "factor_name": factor_name,
        "status": status,
        "error": f"{type(exc).__name__}: {exc}",
    }
    (output_dir / "failure.json").write_text(
        json.dumps(failure, indent=2),
        encoding="utf-8",
    )
    result = FactorEvaluationResult(
        factor_name=factor_name,
        summary=_failed_summary(run, factor_name, exc),
        output_dir=output_dir,
        clean_factor_data=pd.DataFrame(),
        daily_ic=pd.DataFrame(),
        quantile_returns=pd.DataFrame(),
    )
    EvaluationArtifactStore().write_factor_artifacts(result)
    result.summary.to_csv(output_dir / "summary.csv", index=False)
    return result


def _failure_status(exc: Exception) -> str:
    message = str(exc).lower()
    if (
        "no factor data" in message
        or "max_loss" in message
        or "period_len" in message
        or "no clean factor data" in message
    ):
        return "insufficient_data"
    return "failed"


def _log(log_info: Callable[[str], None] | None, message: str) -> None:
    if log_info is not None:
        log_info(message)
