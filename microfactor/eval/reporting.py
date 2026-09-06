from __future__ import annotations

import base64
import html
import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import yaml

from microfactor.eval.report import (
    EvaluationReportResult,
    ReportThresholds,
    build_ranked_summary,
    load_quantile_monotonicity,
    render_markdown_report,
)

_HTML_STYLE = (
    ":root{font-family:'Microsoft YaHei','Segoe UI',Arial,sans-serif;color:#1f2937;"
    "background:#f3f5f7;line-height:1.6}*{box-sizing:border-box}"
    "body{margin:0;background:#f3f5f7}"
    ".report-shell{width:calc(100% - 40px);max-width:1600px;margin:0 auto;"
    "padding:32px 0 64px}"
    ".threshold-panel,.index-panel,.factor-section{background:#fff;"
    "border:1px solid #e1e6ec;"
    "border-radius:12px;box-shadow:0 3px 14px rgba(31,41,55,.05)}"
    ".page-title{font-size:2rem;line-height:1.25;margin:0 0 24px;letter-spacing:0;"
    "color:#111827}"
    "h2{font-size:1.35rem;line-height:1.35;margin:0 0 16px;color:#111827}"
    "h3{font-size:1.05rem;line-height:1.4;margin:24px 0 12px;color:#243447}"
    "h4{font-size:.95rem;margin:20px 0 10px;color:#475569}"
    ".threshold-panel,.index-panel{padding:22px 28px;margin-bottom:24px}"
    ".thresholds{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;"
    "list-style:none;padding:0;margin:0}.thresholds li{border:1px solid #e5eaf0;"
    "border-radius:8px;padding:10px 12px;background:#fbfcfd;font-size:.9rem;color:#475569}"
    ".index-table{margin:0}.index-table th,.index-table td{vertical-align:middle}"
    ".index-table th:first-child,.index-table td:first-child{text-align:left}"
    ".index-table a,.back-link,.factor-report-link{color:#2563eb;"
    "text-decoration:none;font-weight:600}"
    ".index-table a:hover,.back-link:hover,.factor-report-link:hover{text-decoration:underline}"
    ".factor-report-current{color:#64748b;font-size:.84rem;font-weight:600}"
    ".factor-section{padding:28px 32px;margin-bottom:24px}"
    ".factor-title{display:flex;align-items:center;justify-content:space-between;gap:12px;"
    "border-bottom:1px solid #edf0f3;padding-bottom:14px}.factor-title h2{margin:0}"
    ".factor-title-main{display:flex;align-items:center;gap:12px;min-width:0}"
    ".pass,.reject{font-size:.8rem;font-weight:700;padding:4px 10px;border-radius:999px;"
    "white-space:nowrap}.pass{color:#166534;background:#dcfce7}.reject{"
    "color:#991b1b;background:#fee2e2}"
    ".contract{color:#526173;margin:14px 0 20px}.contract b{color:#334155}"
    "table{border-collapse:collapse;width:100%;margin:12px 0 20px;"
    "font-size:.88rem;background:#fff}"
    "th,td{border:1px solid #e1e6ec;padding:8px 10px;text-align:right}"
    "th{background:#f7f9fb;color:#475569;font-weight:600}th:first-child,td:first-child{text-align:left}"
    ".table-wrap{width:100%;overflow-x:auto}.annual-table{min-width:680px;table-layout:fixed}"
    ".annual-table th,.annual-table td{text-align:center}.annual-table th:first-child,"
    ".annual-table td:first-child{width:80px;text-align:center;font-weight:600}"
    "img{max-width:100%;height:auto;border:1px solid #e1e6ec;margin:.4rem}"
    ".cards{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));"
    "gap:10px;margin:18px 0 24px}"
    ".card{border:1px solid #e1e6ec;background:#fbfcfd;border-radius:8px;"
    "padding:12px 14px;min-height:72px}"
    ".card b{display:block;font-size:.75rem;color:#64748b;font-weight:600;"
    "margin-bottom:3px}"
    ".card span{font-size:1.2rem;font-weight:700;color:#172033}"
    ".explain{display:block;margin:16px 0 24px}.explain article{border:1px solid #e3e9ef;"
    "border-left:4px solid #4b77be;background:#f8fafc;border-radius:0 8px 8px 0;"
    "padding:14px 16px;line-height:1.75;margin:0 0 12px}.explain article h3{margin:0 0 8px}"
    ".formula{font-family:Consolas,monospace;font-size:1.05rem;background:#eef3f8;"
    "border-radius:6px;padding:10px 12px;overflow:auto;color:#19324d}"
    ".figures{display:block;width:100%;margin:0;padding:0 0 8px}.figures figure{"
    "margin:.2rem 0}"
    ".chart-card{border:1px solid #e1e6ec;background:#fff;border-radius:8px;"
    "padding:10px 0 12px;"
    "width:100%;box-sizing:border-box;margin-bottom:14px}.chart-card figure{margin:0}"
    ".chart-card img{display:block;width:100%;max-width:100%;height:auto;"
    "aspect-ratio:4 / 1;object-fit:contain;margin:0}"
    ".chart-card figcaption{font-size:.92rem;font-weight:700;color:#334155;"
    "padding:10px 14px 0}"
    ".chart-text{line-height:1.65;font-size:.88rem;color:#526173;padding:0 14px}"
    ".report-nav{margin:0 0 18px;font-size:.92rem}"
    "@media(max-width:900px){.report-shell{width:calc(100% - 24px);"
    "padding-top:16px}.factor-section{padding:20px}"
    ".threshold-panel,.index-panel{padding:18px 20px}.thresholds{grid-template-columns:"
    "repeat(2,minmax(0,1fr))}.cards{grid-template-columns:repeat(2,minmax(0,1fr))}"
    ".factor-title{align-items:flex-start;flex-direction:column}.factor-title-main{"
    "align-items:flex-start;flex-wrap:wrap}}"
    "@media(max-width:560px){.page-title{font-size:1.55rem}.thresholds,.cards{"
    "grid-template-columns:1fr}}"
)


@dataclass(frozen=True)
class SummaryRanker:
    thresholds: ReportThresholds

    def rank(
        self,
        summary: pd.DataFrame,
        monotonicity: pd.Series | None = None,
    ) -> pd.DataFrame:
        return build_ranked_summary(summary, self.thresholds, monotonicity=monotonicity)


class QuantileMonotonicityLoader:
    def load(self, run, summary: pd.DataFrame) -> pd.Series:
        return load_quantile_monotonicity(run.run_dir, summary)


class MarkdownReportRenderer:
    def render(
        self,
        run,
        ranked_summary: pd.DataFrame,
        thresholds: ReportThresholds,
    ) -> str:
        return render_markdown_report(
            run_dir=run.run_dir,
            ranked_summary=ranked_summary,
            thresholds=thresholds,
        )


class HtmlReportRenderer:
    """Render a standalone HTML report with embedded factor artifacts."""

    def render(
        self,
        run,
        ranked_summary: pd.DataFrame,
        thresholds: ReportThresholds,
    ) -> str:
        run_id = getattr(run, "run_id", run.run_dir.name)
        sections = [
            "<!doctype html>",
            '<html lang="zh-CN"><head><meta charset="utf-8">',
            f"<title>Microfactor 因子评估汇总 {html.escape(run_id)}</title>",
            f"<style>{_HTML_STYLE}</style></head><body><main class='report-shell'>",
            "<h1 class='page-title'>Microfactor 因子评估汇总</h1>",
            "<section class='threshold-panel'><h2>门槛判定</h2><ul class='thresholds'>"
            f"<li>|RankIC 均值| &ge; {thresholds.min_ic}</li>"
            f"<li>调整后 ICIR &ge; {thresholds.min_icir}</li>"
            f"<li>方向化 IC 胜率 &ge; {thresholds.min_win_rate}%</li>"
            f"<li>调整后多空价差 &gt; {thresholds.min_spread_bps} bps</li>"
            f"<li>有效样本数 &ge; {thresholds.min_sample_count}</li>"
            f"<li>单调性 &ge; {thresholds.min_monotonicity}</li></ul></section>",
        ]
        sections.append(_render_factor_index(ranked_summary))
        for _, row in ranked_summary.iterrows():
            factor_name = str(row["factor_name"])
            factor_dir = (
                run.factor_dir(factor_name)
                if hasattr(run, "factor_dir")
                else run.run_dir / "factors" / factor_name
            )
            factor_dir.mkdir(parents=True, exist_ok=True)
            contract = _factor_contract(factor_name)
            status = "passed" if bool(row.get("passed", False)) else "rejected"
            css = "pass" if status == "passed" else "reject"
            section_start = len(sections)
            sections.append(
                "<section class='factor-section'><div class='factor-title'>"
                "<div class='factor-title-main'><h2>"
                f"{html.escape(factor_name)}</h2> "
                f"<a class='factor-report-link' href='factors/"
                f"{html.escape(factor_name, quote=True)}/report.html'>"
                "查看独立报告</a></div>"
                f"<span class='{css}'>[{status}]</span></div>"
            )
            sections.append(
                "<p class='contract'><b>公式：</b> " + html.escape(str(contract.get("formula", "")))
                + "<br><b>来源：</b> " + html.escape(str(contract.get("source", "")))
                + "<br><b>来源状态：</b> " + html.escape(str(contract.get("source_status", "")))
                + "<br><b>输入字段：</b> " + html.escape(", ".join(contract.get("inputs", [])))
                + "<br><b>复权模式：</b> " + html.escape(str(contract.get("adjust", ""))) + "</p>"
            )
            sections.append(_render_beginner_explanation(contract))
            sections.append(_render_metric_cards(row))
            sections.append("<h3>核心统计图表</h3><div class='figures'>")
            retained_figures = {
                "daily_ic.png",
                "cumulative_ic.png",
                "five_bucket_cumulative_1D.png",
                "rolling_ic_63.png",
            }
            for image_path in sorted((factor_dir / "figures").glob("*.png")):
                if image_path.name not in retained_figures:
                    continue
                encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
                meaning, trend = _chart_interpretation(image_path.stem, factor_dir, row)
                sections.append(
                    "<article class='chart-card'><figure>"
                    f"<img alt='{html.escape(image_path.stem)}' "
                    f"src='data:image/png;base64,{encoded}'>"
                    f"<figcaption>{html.escape(_figure_caption(image_path.stem))}</figcaption>"
                    "</figure>"
                    f"<div class='chart-text'><b>图表含义：</b>{html.escape(meaning)}"
                    f"<br><b>当前趋势：</b>{html.escape(trend)}</div></article>"
                )
            sections.append("</div>")
            five_bucket_path = factor_dir / "five_bucket_returns.parquet"
            if five_bucket_path.exists():
                sections.append(_render_five_bucket_summary(pd.read_parquet(five_bucket_path)))
            sections.append("</section>")
            factor_section = "\n".join(sections[section_start:])
            _write_factor_report(
                factor_dir=factor_dir,
                factor_name=factor_name,
                run_id=run_id,
                factor_section=factor_section,
            )
            _write_factor_result(factor_dir, row, contract, run)
        sections.append("</main></body></html>")
        return "\n".join(sections)


class EvaluationReporter:
    def __init__(
        self,
        *,
        ranker: SummaryRanker,
        monotonicity_loader: QuantileMonotonicityLoader,
        renderer: MarkdownReportRenderer,
        html_renderer: HtmlReportRenderer | None = None,
    ) -> None:
        self.ranker = ranker
        self.monotonicity_loader = monotonicity_loader
        self.renderer = renderer
        self.html_renderer = html_renderer or HtmlReportRenderer()

    def generate(self, run, summary: pd.DataFrame) -> EvaluationReportResult:
        monotonicity = self.monotonicity_loader.load(run, summary)
        ranked = self.ranker.rank(summary, monotonicity)
        ranked.to_csv(run.ranked_summary_csv, index=False)
        run.report_md.write_text(
            self.renderer.render(run, ranked, self.ranker.thresholds),
            encoding="utf-8",
        )
        run.report_html.write_text(
            self.html_renderer.render(run, ranked, self.ranker.thresholds),
            encoding="utf-8",
        )
        return EvaluationReportResult(
            run_dir=run.run_dir,
            report_path=run.report_md,
            ranked_summary_path=run.ranked_summary_csv,
            ranked_summary=ranked,
            html_path=run.report_html,
        )


def _render_factor_index(ranked_summary: pd.DataFrame) -> str:
    """Render the run-level index that links to every factor report."""
    rows = []
    for _, row in ranked_summary.iterrows():
        factor_name = str(row.get("factor_name", ""))
        status = "通过" if bool(row.get("passed", False)) else "未通过"
        css = "pass" if status == "通过" else "reject"
        href = f"factors/{html.escape(factor_name, quote=True)}/report.html"
        rows.append(
            "<tr>"
            f"<td><a href='{href}'>{html.escape(factor_name)}</a></td>"
            f"<td><span class='{css}'>{status}</span></td>"
            f"<td>{_display_value(row.get('IC Mean'), '.5f')}</td>"
            f"<td>{_display_value(row.get('adjusted_ICIR'), '.4f')}</td>"
            f"<td>{_display_value(row.get('long_short_spread_bps'), '.2f')}</td>"
            f"<td>{_display_value(row.get('sample_count'), ',.0f')}</td>"
            f"<td>{_display_value(row.get('ls_ann_ret'), '.2%')}</td>"
            "</tr>"
        )
    passed = int(ranked_summary.get("passed", pd.Series(dtype=bool)).sum())
    total = len(ranked_summary)
    return (
        "<section class='index-panel'><h2>因子结果索引</h2>"
        f"<p>共 {total} 个因子，{passed} 个通过、{total - passed} 个未通过。"
        "点击因子名称打开独立评估报告。</p>"
        "<div class='table-wrap'><table class='index-table'><thead><tr>"
        "<th>因子</th><th>状态</th><th>RankIC 均值</th><th>调整后 ICIR</th>"
        "<th>多空价差 (bps)</th><th>样本数</th><th>年化多空收益</th>"
        "</tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></div></section>"
    )


def _write_factor_report(
    *,
    factor_dir: Path,
    factor_name: str,
    run_id: str,
    factor_section: str,
) -> Path:
    """Write one self-contained report for a factor and return its path."""
    escaped_name = html.escape(factor_name, quote=True)
    current_link = (
        f"<a class='factor-report-link' href='factors/{escaped_name}/report.html'>"
        "查看独立报告</a>"
    )
    factor_section = factor_section.replace(
        current_link,
        "<span class='factor-report-current'>当前报告</span>",
    )
    report_path = factor_dir / "report.html"
    report_path.write_text(
        "\n".join(
            (
                "<!doctype html>",
                '<html lang="zh-CN"><head><meta charset="utf-8">',
                f"<title>{escaped_name} 因子评估报告 - {html.escape(run_id)}</title>",
                f"<style>{_HTML_STYLE}</style></head><body><main class='report-shell'>",
                "<div class='report-nav'><a class='back-link' href='../../report.html'>"
                "返回汇总</a></div>",
                f"<h1 class='page-title'>{escaped_name} 因子评估报告</h1>",
                factor_section,
                "</main></body></html>",
            )
        ),
        encoding="utf-8",
    )
    return report_path


def _display_value(value: object, format_spec: str) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    try:
        return html.escape(format(float(value), format_spec))
    except (TypeError, ValueError):
        return html.escape(str(value))


def _factor_contract(factor_name: str) -> dict[str, object]:
    try:
        from microfactor.factors.catalog import load_catalog_metadata

        for item in load_catalog_metadata():
            if item.name == factor_name:
                contract = {
                    "formula": item.formula,
                    "source": item.source,
                    "inputs": list(item.inputs),
                    "adjust": item.adjust,
                    "implementation": item.implementation,
                    "source_status": item.status,
                }
                path = Path(__file__).resolve().parents[1] / "catalog" / f"{factor_name}.yaml"
                if path.exists():
                    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
                    formula = raw.get("formula") or {}
                    direction = raw.get("direction") or {}
                    assessment = raw.get("assessment") or {}
                    contract.update(
                        {
                            "formula_interpretation": formula.get("interpretation", ""),
                            "beginner_explanation": formula.get("beginner_explanation") or {},
                            "direction_meaning": direction.get("meaning", ""),
                            "assessment_summary": assessment.get("summary", ""),
                            "most_important_risk": assessment.get("most_important_risk", ""),
                        }
                    )
                return contract
    except (ImportError, OSError):
        pass
    return {}


def _write_factor_result(
    factor_dir: Path,
    row: pd.Series,
    contract: dict[str, object],
    run,
) -> None:
    config = getattr(run, "config", None)
    payload = {
        "factor_name": str(row.get("factor_name", factor_dir.name)),
        "status": "passed" if bool(row.get("passed", False)) else "rejected",
        "source_status": contract.get("source_status", "unknown"),
        "contract": contract,
        "evaluation": {
            "universe": getattr(config, "universe", None),
            "start_date": getattr(config, "start_date", None),
            "end_date": row.get("end_date", getattr(config, "end_date", None)),
            "periods": list(getattr(config, "periods", (1,))),
            "quantiles": getattr(config, "quantiles", 10),
            "return_type": getattr(config, "return_type", "open_t1"),
            "transaction_cost_bps": getattr(config, "transaction_cost_bps", 10.0),
        },
        "metrics": _json_safe(row.to_dict()),
        "artifacts": {
            path.name: str(path.relative_to(factor_dir))
            for path in sorted(factor_dir.rglob("*"))
            if path.is_file() and path.name != "factor_result.json"
        },
    }
    (factor_dir / "factor_result.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )


def _json_safe(values: dict[str, object]) -> dict[str, object]:
    result = {}
    for key, value in values.items():
        if pd.isna(value):
            result[key] = None
        elif hasattr(value, "item"):
            result[key] = value.item()
        else:
            result[key] = value
    return result


def _render_metric_cards(row: pd.Series) -> str:
    labels = (
        ("RankIC 均值", "IC Mean", ".5f"),
        ("RankIC 标准差", "IC Std", ".5f"),
        ("raw ICIR", "raw_ICIR", ".4f"),
        ("HAC t-stat", "adjusted_t-stat", ".3f"),
        ("IC 胜率", "directional_IC>0 %", ".2f"),
        ("覆盖率", "coverage", ".2%"),
        ("单调性", "monotonicity", ".4f"),
        ("多空价差(bps)", "long_short_spread_bps", ".2f"),
        ("年化多空收益", "ls_ann_ret", ".2%"),
        ("多空 Sharpe", "ls_sharpe", ".3f"),
        ("多空最大回撤", "ls_max_dd", ".2%"),
        ("状态", "passed", ""),
    )
    cards = []
    for label, key, fmt in labels:
        value = row.get(key)
        if pd.isna(value):
            display = "N/A"
        elif key == "passed":
            display = "通过" if bool(value) else "未通过"
        elif fmt:
            display = format(float(value), fmt)
        else:
            display = str(value)
        cards.append(f"<div class='card'><b>{label}</b><span>{html.escape(display)}</span></div>")
    return "<div class='cards'>" + "".join(cards) + "</div>"


def _render_beginner_explanation(contract: dict[str, object]) -> str:
    beginner = contract.get("beginner_explanation") or {}
    steps = beginner.get("steps") or []
    steps_html = "".join(f"<li>{html.escape(str(step))}</li>" for step in steps)
    direction = contract.get("direction_meaning") or ""
    assessment = contract.get("assessment_summary") or ""
    risk = contract.get("most_important_risk") or ""
    return (
        "<div class='explain'>"
        "<article><h3>计算公式</h3>"
        f"<div class='formula'>{html.escape(str(contract.get('formula', '')))}</div>"
        f"<p>{html.escape(str(contract.get('formula_interpretation', '')))}</p></article>"
        "<article><h3>小白解读</h3>"
        f"<p><b>一句话：</b>{html.escape(str(beginner.get('one_sentence', '')))}</p>"
        f"<ol>{steps_html}</ol>"
        f"<p><b>高分：</b>{html.escape(str(beginner.get('high_value', '')))}"
        f"<br><b>低分：</b>{html.escape(str(beginner.get('low_value', '')))}"
        f"<br><b>例子：</b>{html.escape(str(beginner.get('example', '')))}</p></article>"
        "<article><h3>本次样本中的原理</h3>"
        f"<p>{html.escape(str(direction))}</p>"
        f"<p><b>结果：</b>{html.escape(str(assessment))}</p>"
        f"<p><b>主要风险：</b>"
        f"{html.escape(str(risk or beginner.get('watch_out', '')))}</p></article>"
        "</div>"
    )


def _render_five_bucket_summary(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "<h3>五档等权超额</h3><p>N/A</p>"
    rows = []
    for bucket in frame.columns:
        series = pd.to_numeric(frame[bucket], errors="coerce").dropna()
        mean_daily = float(series.mean()) if not series.empty else float("nan")
        annualized = (1 + mean_daily) ** 252 - 1 if pd.notna(mean_daily) else float("nan")
        cumulative = float((1 + series).prod() - 1) if not series.empty else float("nan")
        rows.append(
            {
                "五档": str(bucket),
                "日均超额": mean_daily,
                "年化超额": annualized,
                "累计超额": cumulative,
                "有效天数": int(series.size),
            }
        )
    table = pd.DataFrame(rows).rename(columns={"五档": "档位"})
    annual = frame.copy()
    annual.index = pd.to_datetime(annual.index)
    annual_rows = []
    for year, year_frame in annual.groupby(annual.index.year):
        annualized = {}
        for bucket in year_frame.columns:
            series = pd.to_numeric(year_frame[bucket], errors="coerce").dropna()
            if series.empty:
                annualized[str(bucket)] = float("nan")
            else:
                annualized[str(bucket)] = float(
                    (1 + series).prod() ** (252 / len(series)) - 1
                )
        annualized["年度"] = int(year)
        annual_rows.append(annualized)
    annual_table = pd.DataFrame(annual_rows).set_index("年度") if annual_rows else pd.DataFrame()
    if not annual_table.empty:
        annual_table.columns = [f"第{column}档" for column in annual_table.columns]
        annual_table = annual_table.rename_axis("年份").reset_index()
    return (
        "<h3>五档等权超额（累计/年化）</h3>"
        + "<div class='table-wrap'>"
        + table.to_html(
            index=False,
            classes="bucket-table",
            float_format=lambda value: f"{value:.4%}",
        )
        + "</div>"
        + "<h4>五档各年度年化超额</h4>"
        + (
            "<div class='table-wrap'>"
            + annual_table.to_html(
                index=False,
                classes="annual-table",
                float_format=lambda value: f"{value:.4%}",
            )
            + "</div>"
            if not annual_table.empty
            else "<p>没有足够数据。</p>"
        )
    )


def _figure_caption(stem: str) -> str:
    captions = {
        "daily_ic": "每日 RankIC 散点图（含均值线）",
        "cumulative_ic": "累计 RankIC",
        "rolling_ic_63": "63 日滚动 RankIC",
        "quantile_returns_1D": "十分位 1D 收益",
        "quantile_returns_5_bucket_1D": "五档日均超额",
        "five_bucket_cumulative_1D": "五档累计超额",
        "long_short_cumulative": "多空累计收益（含成本前后）",
        "return_distribution": "多空收益分布",
    }
    return captions.get(stem, stem)


def _chart_interpretation(stem: str, factor_dir: Path, row: pd.Series) -> tuple[str, str]:
    """Return a plain-language meaning and data-derived trend for each chart."""
    if stem in {"daily_ic", "cumulative_ic", "rolling_ic_63"}:
        path = factor_dir / "daily_ic.parquet"
        if path.exists():
            frame = pd.read_parquet(path)
            period = str(row.get("period", "1D"))
            series = pd.to_numeric(
                frame.get(period, pd.Series(dtype=float)), errors="coerce"
            ).dropna()
            if not series.empty:
                recent = float(series.tail(min(63, len(series))).mean())
                overall = float(series.mean())
                final_cum = float(series.cumsum().iloc[-1])
                if stem == "daily_ic":
                    meaning = "每天衡量因子排序与下一交易日收益排序的一致程度，0 以上代表正相关。"
                elif stem == "cumulative_ic":
                    meaning = "把每日 RankIC 累加，观察因子的预测优势是否长期积累。"
                else:
                    meaning = "用滚动窗口平滑每日 RankIC，观察稳定性和阶段性变化。"
                if stem == "cumulative_ic":
                    direction = "向上" if final_cum >= 0 else "向下"
                    trend = f"全样本累计 IC 为 {final_cum:.2f}，整体{direction}。"
                else:
                    strength = "强于" if abs(recent) > abs(overall) else "弱于"
                    trend = f"全样本均值 {overall:.4f}，近 63 日均值 {recent:.4f}，"
                    trend += f"近期{strength}长期水平。"
                return meaning, trend
        return "展示 RankIC 的时间序列。", "没有足够数据判断趋势。"
    if stem.startswith("quantile_returns_1D"):
        return (
            "比较 10 个因子分位数组合的平均下一日收益，检查是否单调。",
            _quantile_trend(factor_dir / "quantile_returns.parquet", row),
        )
    if stem == "quantile_returns_5_bucket_1D":
        return (
            "把十分位合并成五档，展示每档的日均等权超额收益。",
            _five_bucket_trend(factor_dir / "five_bucket_returns.parquet"),
        )
    if stem == "five_bucket_cumulative_1D":
        return (
            "展示五档等权超额收益随时间的累计变化，比较不同档位的长期分化。",
            _five_bucket_trend(
                factor_dir / "five_bucket_returns.parquet", cumulative=True
            ),
        )
    if stem == "long_short_cumulative":
        path = factor_dir / "portfolio_returns.parquet"
        if path.exists():
            frame = pd.read_parquet(path)
            values = []
            for col in ("gross_long_short", "net_long_short"):
                if col in frame:
                    s = pd.to_numeric(frame[col], errors="coerce").dropna()
                    if not s.empty:
                        values.append(f"{col} {((1+s).prod()-1):.2%}")
            return "比较多空组合扣除交易成本前后的累计收益。", "；".join(values) + "。"
        return "比较多空组合的累计收益。", "没有足够数据判断趋势。"
    if stem == "return_distribution":
        path = factor_dir / "portfolio_returns.parquet"
        if path.exists():
            frame = pd.read_parquet(path)
            s = pd.to_numeric(
                frame.get("net_long_short", pd.Series(dtype=float)), errors="coerce"
            ).dropna()
            if not s.empty:
                trend = f"净多空日胜率 {s.gt(0).mean():.2%}，中位数 {s.median():.4%}。"
                return "观察多空日收益的中位数、波动和极端值，判断收益是否依赖少数异常日。", trend
        return "观察多空收益分布。", "没有足够数据判断趋势。"
    return "展示该评估图表的时间序列或分组结果。", "请结合上方指标卡判断。"


def _quantile_trend(path: Path, row: pd.Series) -> str:
    if not path.exists():
        return "没有足够数据判断趋势。"
    frame = pd.read_parquet(path)
    period = str(row.get("period", "1D"))
    if period not in frame:
        return "没有足够数据判断趋势。"
    series = pd.to_numeric(frame[period], errors="coerce").dropna()
    if series.empty:
        return "没有足够数据判断趋势。"
    spread = float(row.get("long_short_spread_bps", 0))
    return (
        f"最高档 {series.iloc[-1]:.4%}，最低档 {series.iloc[0]:.4%}；"
        f"方向化后多空价差 {spread:.2f} bps。"
    )


def _five_bucket_trend(path: Path, cumulative: bool = False) -> str:
    if not path.exists():
        return "没有足够数据判断趋势。"
    frame = pd.read_parquet(path)
    if frame.empty:
        return "没有足够数据判断趋势。"
    values = frame.apply(pd.to_numeric, errors="coerce")
    means = values.mean()
    if cumulative:
        ends = (1 + values.fillna(0)).cumprod().iloc[-1] - 1
        strength = "低档更强" if ends.iloc[0] > ends.iloc[-1] else "高档更强"
        return f"累计表现从第 1 档 {ends.iloc[0]:.2%} 到第 5 档 {ends.iloc[-1]:.2%}，{strength}。"
    strength = "低档更强" if means.iloc[0] > means.iloc[-1] else "高档更强"
    return f"日均超额从第 1 档 {means.iloc[0]:.4%} 到第 5 档 {means.iloc[-1]:.4%}，{strength}。"
