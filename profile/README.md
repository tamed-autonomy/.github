# Tamed Autonomy

> **Every step was authorized. The outcome was not.**

Tamed Autonomy explores **path-independent agentic outcome governance**: how to
govern what agentic activity accomplishes across managed and unmanaged actors,
whether they use cooperative or alternate paths.

Existing security is good at deciding whether an actor may perform the next
action. An AI agent can still combine individually permitted actions into a
result the organization never authorized or should not allow. Tamed Autonomy
asks whether a system can recognize that emerging outcome and intervene before
the final action completes it—while preserving meaningful human agency.

This is an evolving research and engineering environment, not a claim that a
production platform, adopted standard or company structure is complete.

## Normative Layer

The Normative Layer applies organizational constraints at action time. It is
being developed as three independently owned projects with a one-way dependency
direction:

```text
UI -> service -> core
```

- **Normative Core** is the deterministic Python decision library. It owns
  constraint evaluation and canonical decision receipts, without depending on
  web frameworks, product workflows or infrastructure.
- **Normative Layer Service** is the headless Python service. It resolves
  operational context, invokes the core, persists results and integrates with
  authentication, enforcement and oversight systems.
- **Normative Layer UI** is a framework-neutral set of embeddable governance UI
  components. It consumes the service API and remains separate so product and
  frontend teams can choose their own application framework.

These boundaries allow the core to evolve as a reusable library—and potentially
as an open-source project—without coupling it to a particular service deployment
or product interface. The three repositories are currently private while their
interfaces and release model are being established.

## Public repositories

<!-- REPOSITORY-CATALOG:START -->
| Repository | Role in the architecture | Current status |
|---|---|---|
| [`agentic-governance-drafts`](https://github.com/tamed-autonomy/agentic-governance-drafts) | Internet-Drafts for portable intent, authority, trust, normative and layer-handoff artifacts. | Public pre-submission work; open for review and not an adopted standard. |
| [`.github`](https://github.com/tamed-autonomy/.github) | Public organization overview and automatically maintained repository catalog. | Organization profile. |
<!-- REPOSITORY-CATALOG:END -->

## Learn more

- Read the research and public essays at [tamedautonomy.ai](https://www.tamedautonomy.ai/).
- Review the public Internet-Drafts and open issues in
  [`agentic-governance-drafts`](https://github.com/tamed-autonomy/agentic-governance-drafts).
