# ML Evaluation & MLOps

## Goal
Make model changes reproducible, measurable, reversible, and accountable from data preparation to production monitoring.

## Reproducibility Contract
Version code, dataset snapshot, feature definitions, model artifact, dependency lockfile, configuration, random seeds, and hardware/runtime metadata. A run is not reproducible if only the model weights are stored.

## Dataset Quality
Check schema, missingness, duplicates, label validity, leakage, distribution, PII, and train/validation/test overlap. Keep a data card with source, license, collection period, known gaps, and intended use.

## Evaluation Split
Use a split strategy matching deployment reality. For temporal data, split by time. For grouped entities, prevent the same entity from crossing splits. Preserve an untouched test set and define acceptance thresholds before seeing results.

```yaml
acceptance:
  primary_metric: f1
  minimum: 0.86
  max_regression_on_safety_set: 0.01
  calibration_error_max: 0.05
```

## Model Registry
Promote artifacts through states such as `candidate`, `staging`, `production`, and `retired`. Require lineage, owner, approval, evaluation report, and rollback artifact for promotion.

## Deployment Patterns
- **Shadow:** production traffic is evaluated without affecting responses.
- **Canary:** a small percentage receives the new model.
- **A/B:** randomized comparison with predeclared metrics.
- **Batch:** scheduled predictions with completeness and freshness checks.

Do not choose A/B testing when safety or deterministic routing requirements prohibit experimentation.

## Monitoring
Monitor input schema and drift, missing values, prediction distribution, latency, resource cost, calibration, delayed ground-truth performance, subgroup metrics, and business outcomes. Alert on actionable thresholds, not every distribution change.

## Rollback
Keep the previous artifact and configuration deployable. Define automatic rollback for severe latency, error, or safety regression and manual rollback for ambiguous business metrics.

## Governance
Document intended use, out-of-scope use, limitations, evaluation populations, human oversight, retention, and incident response. Restrict model artifacts and training data access.

## Checklist
- [ ] Dataset, code, configuration, and artifacts are versioned.
- [ ] Split strategy prevents leakage.
- [ ] Acceptance metrics and regression gates are predeclared.
- [ ] Registry promotion requires review and lineage.
- [ ] Shadow/canary plan exists for risky releases.
- [ ] Production monitoring includes delayed quality signals.
- [ ] Subgroup and safety evaluation is included.
- [ ] Rollback has been tested.
- [ ] Model card and data card are maintained.

## References
- https://mlflow.org/docs/latest/ml/tracking/
- https://www.tensorflow.org/tfx/guide
- https://www.nist.gov/itl/ai-risk-management-framework

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
