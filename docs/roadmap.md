# Roadmap

This page describes **possible directions** for **entie** and **entei-core**. It is a planning aid, not a release contract: ordering, scope, and timing can change. Use [GitHub issues](https://github.com/eddiethedean/entie/issues) to argue for or refine items.

## Where things stand today

Understanding the baseline avoids duplicating work or promising what the stack already does.

- **entei-core** materializes a collection snapshot with `find()` into columnar `dict[str, list]` (top-level keys only). It is small, testable, and dependency-light.
- **entie** layers **connect** / **EntieDatabase**, **EnteiDataFrame** (lazy until `collect`, then full materialization + Python filters), **Records** (`insert_many`), and trivial expression helpers.
- **Design tension:** the DataFrame API feels “lazy,” but today it always pulls the full result set that `MongoRoot` + `mongo_root_to_column_dict` implies. Many roadmap items are about narrowing that gap or making the tradeoff explicit.

## PyMongo capabilities to draw on (research notes)

**entie** is intentionally thin over [PyMongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/). The driver already exposes rich behavior; the roadmap is about **when** to wrap, **when** to document recipes, and **when** to stay out of the way. Below is a concise map of features worth aligning with—see the [PyMongo API reference](https://pymongo.readthedocs.io/en/stable/) and [MongoDB PyMongo docs](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/) for details and server requirements.

### Reads and cursors

- **`Collection.find` / `find_one`** — `filter`, `projection`, `sort`, `skip`, `limit`, `batch_size`, `hint`, `max_time_ms`, `comment`, `collation`, `session`, `read_preference`, `read_concern`, `allow_disk_use` (aggregation only). Many of these reduce bytes, bound work, or steer index use before data hits Python.
- **`Collection.aggregate`** — pipeline stages, `allow_disk_use` for large sorts/group, `batchSize` on the cursor, same session / read concern / collation patterns as `find`.
- **`Cursor`** — iteration, `batch_size`, addressable as a stream instead of `list(cursor)` for future streaming work.

### Writes

- **`insert_one` / `insert_many`** — `ordered` vs unordered bulk insert semantics; `bypass_document_validation`; write concern via client/database or operation options.
- **`bulk_write`** (collection scope) — mixed `InsertOne`, `UpdateOne`, `ReplaceOne`, `DeleteOne`, etc., in one round trip.
- **`MongoClient.bulk_write`** (PyMongo 4.9+) — batched writes **across namespaces** in fewer round trips; requires a **minimum server version** (see current PyMongo release notes—typically MongoDB 8.0+). Worth a first-class mention for ETL that touches many collections.
- **`replace_one` / `update_one` / `update_many` / `delete_one` / `delete_many`** — filters and upserts for “records keyed by field” workflows.

### Sessions, transactions, consistency

- **`MongoClient.start_session`** — causal consistency, retryable reads/writes in session context.
- **Multi-document transactions** — `session.start_transaction()` / `with_transaction` for patterns that must commit atomically across collections (where the deployment supports it).

### Change streams and events

- **`Collection.watch` / `Database.watch` / `MongoClient.watch`** — change streams with optional aggregation `pipeline` on events (`$match`, `$project`, etc.). Useful for **incremental** or **reactive** pipelines; a different shape of problem than batch `collect()`.

### Topology, encryption, and operations

- **`MongoClient`** — connection options (TLS, compression, timeouts, retry writes, `server_api` for versioned API on Atlas/serverless), plus **CSFLE** / **Queryable Encryption** via client-side encryption types when applications need them.
- **Index and collection metadata** — `create_index`, `list_indexes`, `estimated_document_count`, `count_documents` (with filters) for observability and tooling around frames and inserts.
- **GridFS** — `GridFSBucket` for large blobs; likely **documentation-only** or a small helper unless entie grows a file-focused API.

### Observability

- **Event listeners** (e.g. command monitoring) for tracing slow queries and correlating application work with MongoDB commands—often better documented as **patterns** than wrapped, unless we add optional hooks.

This map should inform the sections below; not every knob needs a wrapper in **entie**.

## Scale and performance

### Streaming and bounded memory

**Problem:** `collect()` loads every matching document into Python lists. That is fine for tests and modest data, but risky for multi-gigabyte collections.

**Directions:**

- Add an optional code path that iterates a **PyMongo cursor** in batches (`Cursor` with explicit `batch_size`, or `find(..., batch_size=...)`) instead of `list(find())`, and feed partial column buffers or row iterators.
- Surface **`max_time_ms`** and **`allow_disk_use`** (for aggregation paths) where users need server-side caps and spill-to-disk behavior for large analytics.
- Define **semantics**: streaming might mean “row iterator only,” “incremental column append with fixed schema,” or “export to disk / Arrow without full RAM.” Each has different API surface and guarantees.
- **entei-core** might expose a lower-level “append batch into column dicts” helper; **entie** would own user-facing ergonomics.

### Columnar interop (optional extras)

**Problem:** Many workflows want **Polars**, **pandas**, or **Apache Arrow** without hand-rolling `dict[str, list]` conversion.

**Directions:**

- Optional dependencies (`entie[polars]`, etc.) with thin `to_polars()` / `to_arrow()`-style helpers built on existing columnar output.
- Clearly document **dtype** rules (MongoDB’s dynamic typing vs. strict Arrow schemas), **null** handling, and interaction with PyMongo’s **BSON** decoding (including recent improvements around NumPy-friendly types where applicable).

### Benchmarks and regression guardrails

**Directions:**

- A small **benchmark harness** (not necessarily in CI on every PR): fixed seeds, document shapes, and reported wall time / RSS for materialization and `collect`.
- Optional **perf budgets** in CI only if noise can be controlled (often Linux-only, pinned runners).

## Query and server-side work

### Predicate push-down (hard but valuable)

**Problem:** `filter_rows(lambda r: ...)` runs in Python after a full read. For large data, pushing work to MongoDB is essential.

**Constraints:**

- Arbitrary Python callables **cannot** be translated to query documents. Any push-down would start with a **restricted** expression layer (comparisons on known fields, `and` / `or`, membership) or an explicit **parallel** API that accepts a MongoDB **filter dict** compatible with `find`.
- Needs a clear story when a user mixes “pushable” filters with arbitrary lambdas (split query vs. post-filter, or reject unsupported combinations).

**Directions:**

- Introduce something like `find_filter: dict | None` on `from_collection`, or a small **expression AST** that compiles to `find` / aggregation `$match`.
- Pass through **`collation`** and **`comment`** on the underlying `find` / `aggregate` where they matter for correctness and observability.
- Document **equivalence**: results must match today’s semantics for the subset of operations that map 1:1.

### Aggregation pipelines

**Problem:** Real analytics often need `$group`, `$lookup`, `$unwind`, not only `find`.

**Directions:**

- A separate entry point (e.g. `EnteiDataFrame.from_aggregation(pipeline, ...)`) that uses **`Collection.aggregate`** under the hood and treats the **aggregation cursor** like a `find` cursor for column materialization.
- Plumb **`allow_disk_use`**, **`batchSize`**, and session options for large pipelines.
- Decide whether **entei-core** stays “raw documents only” or gains optional helpers for “flatten pipeline output to columns.”

### Projection, sort, limit, hints, read preferences

**Problem:** PyMongo can reduce bytes and use indexes before Python runs; the high-level API does not expose that yet.

**Directions:**

- Thread **`projection`** into `MongoRoot` / `find` so unused fields never leave the server when the user specifies a column list early.
- Optional **`sort`**, **`limit`**, **`skip`** on `find` for ordered, windowed reads (with warnings when combined with Python `filter_rows` that assumes full-set semantics).
- **`hint`**, **`read_preference`**, **`read_concern`**, and **`session`** for performance tuning, replica routing, and causal reads—likely on `from_collection` or connection options documented next to **`connect`**.

## Sessions, transactions, and change streams

These are first-class PyMongo features that deserve explicit roadmap treatment.

### Sessions and multi-document transactions

**Directions:**

- Document **recommended patterns**: passing a **`ClientSession`** into operations that **entie** wraps (once we accept optional `session=`), or using **`with_collection`/`database` raw** for transactional blocks today.
- Longer term: optional **`session=`** on `Records`, `EnteiDataFrame.collect`, or context managers that pair **`start_session`** with **`with_transaction`** for multi-collection workflows (where supported).

### Change streams

**Directions:**

- Treat **`watch()`** as a **separate track** from batch frames: document how to combine change events with incremental processing, or offer a thin iterator helper that does not pretend to be `EnteiDataFrame`.
- Allow **pipeline**-filtered streams (`$match` on change events) in any wrapper, aligned with [MongoDB change stream](https://www.mongodb.com/docs/manual/changeStreams/) semantics.

## Data model and types

### Nested and dotted fields

**Problem:** Only top-level keys become columns today; nested documents are single BSON values.

**Directions:**

- Opt-in **flattening rules**: e.g. `fields=("addr.city", "addr.zip")` or a small schema object describing paths.
- **Arrays:** decide between “take first element,” “JSON stringify,” “explode rows” (1:n expansion), or “not supported” by default—each is a product decision.

### Static typing

**Directions:**

- **Protocols** for “collection-like” and “database-like” objects used in tests and typing.
- Optional **TypedDict** generics on helpers where row shape is stable enough to matter.
- Keep **runtime** permissive: Mongo documents remain dynamic at heart.

## Connectivity and runtimes

### Motor and asyncio

**Problem:** Many services use **Motor**; synchronous PyMongo-only APIs do not compose with async routes.

**Directions:**

- Parallel **async** `connect` / database types, or official **documentation recipes** (“run entie in `asyncio.to_thread`”, or “use Motor’s collection with **entei-core** materialization in a thread pool”) before committing to a full async surface.
- If async first-class: clarify **thread safety** and **client sharing** across tasks (same as PyMongo’s guidance).

### Operations and lifecycle

**Directions:**

- Document **when to close** clients, interaction with **fork** (e.g. Celery prefork), **connection string** rotation, and driver defaults for **retryable reads/writes**.
- Optional thin methods on **`EntieDatabase`** mirroring **`database.command`**, **`list_collection_names`**, **`create_collection`**, or **index** helpers—only where they reduce repeated boilerplate without hiding errors.

## Ergonomics and data movement

### Richer `Records` and bulk writes

**Directions:**

- **`replace_one` / `update_one`** patterns for upserts keyed by a field; expose **`ordered`** / **`bypass_document_validation`** where inserts are bulk.
- **`Collection.bulk_write`** for mixed operations in one request.
- **`MongoClient.bulk_write`** for cross-collection batches where server version permits—document **minimum MongoDB / PyMongo versions** clearly.
- Optional **schema validation** hooks (pre-insert callable) without requiring a specific validation library.

### Imports and exports

**Directions:**

- **CSV / JSON lines** helpers for “dump this frame” or “load these rows” that delegate to `Records` + stdlib or optional **orjson**.
- **Parquet** as an extra, if Polars/Arrow land first.

### Encryption and large blobs

**Directions:**

- **Client-side field level encryption** and **Queryable Encryption**: prefer **documentation and examples** using PyMongo’s APIs unless entie adds typed helpers later.
- **GridFS**: remain **out of core** unless a concrete use case justifies a small wrapper (see [non-goals](#non-goals-for-now)).

## Testing, quality, and documentation

**Directions:**

- **Link checking** in CI (`lyche`, `markdown-link-check`, or RTD’s hooks) for `docs/` and README URLs.
- **Fixture library**: reusable mongomock patterns or docker-compose recipe for local integration tests (optional, not default CI).
- **Examples gallery** on the doc site: snippets that show **raw PyMongo** + **entie** together (sessions, `hint`, `collation`, transactions) so users know how to combine layers.

## Non-goals (for now)

Declaring non-goals reduces confusion:

- Replacing **PyMongo** or hiding connection semantics entirely.
- A full **SQL query compiler** to MongoDB.
- **ORM-style** document classes and migrations (out of scope unless the project direction changes explicitly).
- **Guaranteed** sub-millisecond latency; Python + full-document reads will always have limits.
- Re-implementing **GridFS**, **CSFLE**, or **Atlas Search** inside **entie** instead of documenting how to use them alongside the library.

## How to influence this roadmap

- Open an issue with **problem statement**, **approximate data size**, **sync vs async**, and whether you care about **ente** ergonomics vs **entei-core** primitives only.
- For concrete work: follow [CONTRIBUTING.md](https://github.com/eddiethedean/entie/blob/main/CONTRIBUTING.md), update **CHANGELOG** and **docs** when behavior or public API changes.
