# Task Profiles

Adapt the work items and evidence to the task rather than forcing every task into code-development language.

## Bug repair

Capture the failure, intended behavior, smallest repair boundary, and validation that reaches the original path.

## Feature or refactor

Capture current and target behavior, preserved invariants, affected callers, coherent implementation slices, and behavior-focused validation.

## Test work

Capture the risk or evidence gap, fixture and oracle, why the test reaches the target behavior, and relevant environment or flakiness constraints.

## Research or design

Capture the question, evidence sources, facts versus inferences, decision criteria, conclusions, and remaining material uncertainty. Research completion is not implementation authorization.

## Run or experiment

Capture the relevant configuration, environment, stop and success conditions, result location, and cleanup. Add detailed command or timing records only when reproducibility or cost requires them.

## Migration or external operation

Capture the exact target, authorization, destructive boundary, backup or recovery needs, validation, and rollback or irreversibility.

## Documentation or policy

Capture authoritative sources, audience, navigation, terminology, and consistency with current implementation.

For mixed work, use distinct items or sections where the evidence differs. Separate files are optional.
