# LLM Application Engineering

## Goal
Treat model output as untrusted, probabilistic input that must be constrained, validated, observed, and recoverable.

## System Boundary
```text
User input → policy checks → prompt assembly → model → schema validation → business rules → response
                                      ↘ tool authorization and execution ↗
```typescript
Do not let the model directly mutate databases, send messages, or access arbitrary URLs. Place deterministic application code between intent and side effect.

## Structured Output
```typescript
type Classification = {
  category: 'billing' | 'technical' | 'other';
  confidence: number;
};

function parseClassification(value: unknown): Classification {
  if (!value || typeof value !== 'object') throw new Error('Invalid model output');
  const candidate = value as Record<string, unknown>;
  if (!['billing', 'technical', 'other'].includes(String(candidate.category))) {
    throw new Error('Unknown category');
  }
  const confidence = Number(candidate.confidence);
  if (!Number.isFinite(confidence) || confidence < 0 || confidence > 1) {
    throw new Error('Invalid confidence');
  }
  return { category: candidate.category as Classification['category'], confidence };
}
```
Use a schema library already present in the application when available. Validate length, enums, URLs, IDs, and authorization context.

## Prompt Contracts
Version prompts with code, define input/output contracts, include explicit refusal and uncertainty behavior, and keep user-provided content delimited. Never place secrets in prompts.

## Tool Use
Each tool should have a narrow schema, permission check, timeout, retry policy, audit event, and idempotency strategy. Require confirmation for irreversible or high-impact actions.

## Prompt Injection Defense
Treat retrieved documents, webpages, emails, and user content as data, not instructions. Separate system policy from untrusted context, restrict tools by user authorization, and test indirect injection scenarios. Output filtering alone is insufficient.

## Reliability and Cost
Set token, time, and concurrency budgets. Use model routing only with measured quality thresholds. Cache deterministic or safely shareable results, never private prompts or outputs in a shared cache without policy.

## Evaluation
Maintain a versioned evaluation set containing happy paths, ambiguous inputs, refusals, injection attempts, tool errors, and multilingual cases. Measure task success, groundedness, safety, latency, cost, and human preference.

## Operational Fallbacks
Return a safe partial response, ask for clarification, route to a human, or use a deterministic fallback when the model times out, violates schema, exceeds budget, or produces low confidence.

## Checklist
- [ ] Model outputs are schema-validated.
- [ ] Tools are allowlisted and authorization-aware.
- [ ] External content is treated as untrusted data.
- [ ] Prompt and model versions are logged safely.
- [ ] Token, latency, concurrency, and cost limits exist.
- [ ] Evaluation covers quality and adversarial behavior.
- [ ] Sensitive data is minimized and redacted.
- [ ] Fallback behavior is tested.
- [ ] High-impact actions require deterministic confirmation.

## References
- https://platform.openai.com/docs/guides/structured-outputs
- https://owasp.org/www-project-top-10-for-large-language-model-applications/
- https://www.nist.gov/itl/ai-risk-management-framework

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
