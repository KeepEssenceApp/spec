// Local check for spec#7 (#109): what a D1 batch does and does not guarantee.
//
// Carrier: Miniflare's local D1 (workerd + SQLite), opened with wrangler's getPlatformProxy, in memory.
// It is NOT the production D1 and NOT a remote D1 test database: nothing here talks to Cloudflare.
//
// Every check has the value it must produce. A line ends in [OK] or [MISMATCH, expected ...];
// the process exits 1 if any line is a mismatch. The result is also written to last-run.txt.
// Run it with `npm install` then `npm run check` (see README.md).
import { getPlatformProxy } from "wrangler";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const wranglerVersion = JSON.parse(readFileSync(join(here, "node_modules", "wrangler", "package.json"), "utf8")).version;

const lines = [];
let checks = 0;
let mismatches = 0;
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
function emit(line) {
  lines.push(line);
  console.log(line);
}
// say(label, actual, expected): `expected` is what the spec relies on; a difference is reported, never hidden.
function say(label, actual, expected) {
  checks += 1;
  const ok = same(actual, expected);
  if (!ok) mismatches += 1;
  emit(`${label} => ${JSON.stringify(actual)}  ${ok ? "[OK]" : `[MISMATCH, expected ${JSON.stringify(expected)}]`}`);
}

emit("# spec#7 (#109) D1 batch check");
emit(`# run at (UTC): ${new Date().toISOString()}`);
emit(`# wrangler ${wranglerVersion}, node ${process.version}`);
emit("# carrier: Miniflare local D1 (workerd + SQLite) through getPlatformProxy, persist=false. NOT a remote D1.");

const proxy = await getPlatformProxy({ configPath: join(here, "wrangler.toml"), persist: false });
const db = proxy.env.DB;
const count = async (sql) => (await db.prepare(sql).first()).c;
const UNIQUE_ERROR = "UNIQUE constraint failed: usage_records.request_id";

async function reset() {
  await db.exec("DROP TABLE IF EXISTS work");
  await db.exec("DROP TABLE IF EXISTS ledger");
  await db.exec("DROP TABLE IF EXISTS usage_records");
  await db.exec("CREATE TABLE work (id TEXT PRIMARY KEY, started INTEGER NOT NULL, next_at INTEGER NOT NULL)");
  await db.exec("CREATE TABLE ledger (id INTEGER PRIMARY KEY AUTOINCREMENT, work_id TEXT NOT NULL, attempt INTEGER NOT NULL, state TEXT NOT NULL)");
  await db.exec("CREATE TABLE usage_records (id INTEGER PRIMARY KEY AUTOINCREMENT, request_id INTEGER NOT NULL UNIQUE, tokens INTEGER NOT NULL)");
}

// ---- T1: a batch is NOT a fence. The UPDATE matches 0 rows, the next statement still runs.
await reset();
await db.exec("INSERT INTO ledger (work_id, attempt, state) VALUES ('w', 1, 'recycled')");
let r = await db.batch([
  db.prepare("UPDATE ledger SET state='with_usage' WHERE id=1 AND attempt=1 AND state='in_progress'"),
  db.prepare("INSERT INTO usage_records (request_id, tokens) VALUES (1, 100)"),
]);
say("T1 per-statement meta.changes", r.map((x) => x.meta.changes), [0, 1]);
say("T1 usage rows after a fenced-out UPDATE + plain INSERT (1 = the batch did not stop the INSERT)", await count("SELECT count(*) c FROM usage_records"), 1);

// ---- T2: make the second statement conditional on the first having matched, via changes()
await reset();
await db.exec("INSERT INTO ledger (work_id, attempt, state) VALUES ('w', 1, 'recycled')");
r = await db.batch([
  db.prepare("UPDATE ledger SET state='with_usage' WHERE id=1 AND attempt=1 AND state='in_progress'"),
  db.prepare("INSERT INTO usage_records (request_id, tokens) SELECT 1, 100 WHERE changes() > 0"),
]);
say("T2 changes() variant, row not in_progress: usage rows", await count("SELECT count(*) c FROM usage_records"), 0);
await reset();
await db.exec("INSERT INTO ledger (work_id, attempt, state) VALUES ('w', 1, 'in_progress')");
r = await db.batch([
  db.prepare("UPDATE ledger SET state='with_usage' WHERE id=1 AND attempt=1 AND state='in_progress'"),
  db.prepare("INSERT INTO usage_records (request_id, tokens) SELECT 1, 100 WHERE changes() > 0"),
]);
say("T2 changes() variant, row in_progress: usage rows", await count("SELECT count(*) c FROM usage_records"), 1);

// ---- T3: dedup by the UNIQUE constraint (the same result written twice; a late write of a recycled row)
await reset();
await db.exec("INSERT INTO ledger (work_id, attempt, state) VALUES ('w', 1, 'recycled')");
const lateWrite = () => db.batch([
  db.prepare("UPDATE ledger SET state='with_usage' WHERE id=1 AND state IN ('in_progress','recycled')"),
  db.prepare("INSERT OR IGNORE INTO usage_records (request_id, tokens) SELECT 1, 100 WHERE EXISTS (SELECT 1 FROM ledger WHERE id=1 AND state='with_usage')"),
]);
const a = await lateWrite();
const b = await lateWrite();
say("T3 first write meta.changes", a.map((x) => x.meta.changes), [1, 1]);
say("T3 second write meta.changes", b.map((x) => x.meta.changes), [0, 0]);
say("T3 usage rows after the same result written twice", await count("SELECT count(*) c FROM usage_records"), 1);
// Without OR IGNORE: a plain INSERT of the duplicate request_id must be refused by the UNIQUE constraint.
// (The first statement is a valid UPDATE on purpose: an earlier version of this check used a column that
// does not exist, so it failed on that and never reached the constraint.)
let dupErr = null;
try {
  await db.batch([
    db.prepare("UPDATE ledger SET state='with_usage' WHERE id=1"),
    db.prepare("INSERT INTO usage_records (request_id, tokens) VALUES (1, 100)"),
  ]);
} catch (e) {
  dupErr = String(e.message || e);
}
emit(`#   T3 the error the plain duplicate INSERT raised: ${JSON.stringify(dupErr && dupErr.slice(0, 140))}`);
say(`T3 plain INSERT of a duplicate request_id inside a batch raises "${UNIQUE_ERROR}"`, dupErr !== null && dupErr.includes(UNIQUE_ERROR), true);
say("T3 usage rows after the refused duplicate (still 1)", await count("SELECT count(*) c FROM usage_records"), 1);

// ---- T4: atomicity: a later statement fails -> the earlier UPDATE is rolled back
await reset();
await db.exec("INSERT INTO ledger (work_id, attempt, state) VALUES ('w', 1, 'in_progress')");
await db.exec("INSERT INTO usage_records (request_id, tokens) VALUES (1, 50)");
let err = null;
try {
  await db.batch([
    db.prepare("UPDATE ledger SET state='with_usage' WHERE id=1"),
    db.prepare("INSERT INTO usage_records (request_id, tokens) VALUES (1, 100)"), // UNIQUE violation
  ]);
} catch (e) {
  err = String(e.message || e);
}
say(`T4 batch with a failing 2nd statement raises "${UNIQUE_ERROR}"`, err !== null && err.includes(UNIQUE_ERROR), true);
say("T4 ledger state after the failed batch (in_progress = the UPDATE was rolled back)", (await db.prepare("SELECT state FROM ledger WHERE id=1").first()).state, "in_progress");

// ---- T5: taking an attempt: the counter write is the fence; the recycle of rows must be conditioned on it
async function seedWork(started, nextAt) {
  await reset();
  await db.exec(`INSERT INTO work VALUES ('w', ${started}, ${nextAt})`);
  await db.exec(`INSERT INTO ledger (work_id, attempt, state) VALUES ('w', ${started}, 'in_progress'), ('w', ${started}, 'in_progress')`);
}
const now = 1000;
// 5a: too early (next_at in the future): the counter write loses; an unconditioned second statement still recycles the live attempt's rows (WRONG)
await seedWork(1, 2000);
r = await db.batch([
  db.prepare("UPDATE work SET started=started+1, next_at=? WHERE id='w' AND started=1 AND started<4 AND next_at<=?").bind(5000, now),
  db.prepare("UPDATE ledger SET state='recycled' WHERE work_id='w' AND attempt=1 AND state='in_progress'"),
]);
say("T5a too early, unconditioned recycle: changes", r.map((x) => x.meta.changes), [0, 2]);
say("T5a rows recycled although no new attempt started (2 = the wrong result)", await count("SELECT count(*) c FROM ledger WHERE state='recycled'"), 2);
// 5b: conditioned on the counter having moved to n+1 in this same transaction
await seedWork(1, 2000);
r = await db.batch([
  db.prepare("UPDATE work SET started=started+1, next_at=? WHERE id='w' AND started=1 AND started<4 AND next_at<=?").bind(5000, now),
  db.prepare("UPDATE ledger SET state='recycled' WHERE work_id='w' AND attempt=1 AND state='in_progress' AND (SELECT started FROM work WHERE id='w')=2"),
]);
say("T5b too early, conditioned recycle: changes", r.map((x) => x.meta.changes), [0, 0]);
say("T5b rows recycled (0 expected)", await count("SELECT count(*) c FROM ledger WHERE state='recycled'"), 0);
// 5c: due: both apply
await seedWork(1, 500);
r = await db.batch([
  db.prepare("UPDATE work SET started=started+1, next_at=? WHERE id='w' AND started=1 AND started<4 AND next_at<=?").bind(5000, now),
  db.prepare("UPDATE ledger SET state='recycled' WHERE work_id='w' AND attempt=1 AND state='in_progress' AND (SELECT started FROM work WHERE id='w')=2"),
]);
say("T5c due: changes", r.map((x) => x.meta.changes), [1, 2]);
say("T5c rows recycled (2 expected)", await count("SELECT count(*) c FROM ledger WHERE state='recycled'"), 2);

// ---- T6: concurrency: 20 concurrent takers of the same attempt; exactly one wins
await seedWork(1, 500);
const takers = Array.from({ length: 20 }, () => db.batch([
  db.prepare("UPDATE work SET started=started+1, next_at=? WHERE id='w' AND started=1 AND started<4 AND next_at<=?").bind(5000, now),
  db.prepare("UPDATE ledger SET state='recycled' WHERE work_id='w' AND attempt=1 AND state='in_progress' AND (SELECT started FROM work WHERE id='w')=2"),
]));
const rs = await Promise.all(takers);
say("T6 winners among 20 concurrent takers (meta.changes of the 1st statement = 1)", rs.filter((x) => x[0].meta.changes === 1).length, 1);
say("T6 final started", (await db.prepare("SELECT started FROM work WHERE id='w'").first()).started, 2);

// ---- T7: concurrency: one conditional INSERT...SELECT placeholder; 30 concurrent, cap 12, per-attempt cap 3
await reset();
await db.exec("INSERT INTO work VALUES ('w', 1, 0)");
const place = () => db.prepare(
  `INSERT INTO ledger (work_id, attempt, state)
   SELECT 'w', 1, 'in_progress'
   WHERE (SELECT count(*) FROM ledger WHERE work_id='w') < 12
     AND (SELECT count(*) FROM ledger WHERE work_id='w' AND attempt=1) < 3
     AND (SELECT started FROM work WHERE id='w') = 1`).run();
const ps = await Promise.all(Array.from({ length: 30 }, place));
say("T7 placeholders granted out of 30 (cap per attempt 3)", ps.filter((x) => x.meta.changes === 1).length, 3);

// ---- T8: a result write racing the recycle write; thunks, so the real dispatch order is the chosen one
const settleUsage = () => db.batch([
  db.prepare("UPDATE ledger SET state='with_usage' WHERE id=1 AND state IN ('in_progress','recycled')"),
  db.prepare("INSERT OR IGNORE INTO usage_records (request_id, tokens) SELECT 1, 100 WHERE changes() > 0"),
]);
const settleNoUsage = () => db.batch([
  db.prepare("UPDATE ledger SET state='no_usage' WHERE id=1 AND attempt=1 AND state='in_progress'"),
]);
const recycleAttempt = () => db.batch([
  db.prepare("UPDATE work SET started=started+1, next_at=? WHERE id='w' AND started=1 AND next_at<=?").bind(5000, now),
  db.prepare("UPDATE ledger SET state='recycled' WHERE work_id='w' AND attempt=1 AND state='in_progress' AND (SELECT started FROM work WHERE id='w')=2"),
]);
async function race(settle, firstIsRecycle) {
  await seedWork(1, 500);
  await db.exec("DELETE FROM ledger WHERE id=2");
  const jobs = firstIsRecycle ? [recycleAttempt, settle] : [settle, recycleAttempt];
  await Promise.all(jobs.map((j) => j()));
  const st = (await db.prepare("SELECT state FROM ledger WHERE id=1").first()).state;
  const tok = await count("SELECT count(*) c FROM usage_records");
  const budgetRows = await count("SELECT count(*) c FROM ledger WHERE work_id='w' AND state IN ('in_progress','recycled','with_usage')");
  return `${st}|tokens=${tok}|budget=${budgetRows}`;
}
const tally = {};
for (let i = 0; i < 100; i++) {
  for (const [name, settle] of [["usage", settleUsage], ["nousage", settleNoUsage]]) {
    for (const rf of [false, true]) {
      const k = `${name} ${rf ? "recycle-dispatched-first" : "result-dispatched-first"} => ${await race(settle, rf)}`;
      tally[k] = (tally[k] || 0) + 1;
    }
  }
}
say("T8 final states over 100 rounds per case", tally, {
  "usage result-dispatched-first => with_usage|tokens=1|budget=1": 100,
  "usage recycle-dispatched-first => with_usage|tokens=1|budget=1": 100,
  "nousage result-dispatched-first => no_usage|tokens=0|budget=0": 100,
  "nousage recycle-dispatched-first => recycled|tokens=0|budget=1": 100,
});

// ---- T9: the same result written twice after the recycle (late, with usage): one token row, state unchanged
await seedWork(1, 500);
await db.exec("DELETE FROM ledger WHERE id=2");
await recycleAttempt();
await settleUsage(); await settleUsage();
say("T9 late usage written twice: state / token rows", [(await db.prepare("SELECT state FROM ledger WHERE id=1").first()).state, await count("SELECT count(*) c FROM usage_records")], ["with_usage", 1]);
// a late no-usage write after the recycle: nothing moves
await seedWork(1, 500);
await db.exec("DELETE FROM ledger WHERE id=2");
await recycleAttempt();
r = await settleNoUsage();
say("T9 late no-usage: meta.changes / state", [r[0].meta.changes, (await db.prepare("SELECT state FROM ledger WHERE id=1").first()).state], [0, "recycled"]);

// ---- T10: the token insert guarded by a predicate on the row (no changes()): EXISTS + UNIQUE + OR IGNORE
const settleUsageExists = () => db.batch([
  db.prepare("UPDATE ledger SET state='with_usage' WHERE id=1 AND state IN ('in_progress','recycled')"),
  db.prepare("INSERT OR IGNORE INTO usage_records (request_id, tokens) SELECT 1, 100 WHERE EXISTS (SELECT 1 FROM ledger WHERE id=1 AND state='with_usage')"),
]);
const t10 = {};
for (let i = 0; i < 100; i++) {
  for (const rf of [false, true]) {
    const k = `exists-variant ${rf ? "recycle-first" : "result-first"} => ${await race(settleUsageExists, rf)}`;
    t10[k] = (t10[k] || 0) + 1;
  }
}
say("T10 EXISTS variant, both dispatch orders over 100 rounds", t10, {
  "exists-variant result-first => with_usage|tokens=1|budget=1": 100,
  "exists-variant recycle-first => with_usage|tokens=1|budget=1": 100,
});
// a row that already ended as no_usage (normal settle), then a second, conflicting "with usage" write arrives:
// the UPDATE matches 0 rows and the EXISTS guard keeps the token insert out
await seedWork(1, 500); await db.exec("DELETE FROM ledger WHERE id=2");
await settleNoUsage(); await settleUsageExists();
say("T10 conflicting second write after a no_usage settle: state / token rows", [(await db.prepare("SELECT state FROM ledger WHERE id=1").first()).state, await count("SELECT count(*) c FROM usage_records")], ["no_usage", 0]);

// ---- T11: the additive migration's shape: old rows keep no request id; unique only where it is set
await db.exec("DROP TABLE IF EXISTS ur");
await db.exec("CREATE TABLE ur (id INTEGER PRIMARY KEY AUTOINCREMENT, tokens INTEGER NOT NULL)");
await db.exec("INSERT INTO ur (tokens) VALUES (10), (20)");           // old paid rows
await db.exec("ALTER TABLE ur ADD COLUMN request_id INTEGER");        // additive
await db.exec("CREATE UNIQUE INDEX ur_request ON ur (request_id) WHERE request_id IS NOT NULL");
await db.exec("INSERT INTO ur (tokens) VALUES (30)");                  // another row without an id is still fine
await db.prepare("INSERT OR IGNORE INTO ur (request_id, tokens) VALUES (7, 100)").run();
const dup = await db.prepare("INSERT OR IGNORE INTO ur (request_id, tokens) VALUES (7, 100)").run();
say("T11 old rows without an id stay; a duplicate request_id is ignored: rows / dup meta.changes", [await count("SELECT count(*) c FROM ur"), dup.meta.changes], [4, 0]);

await proxy.dispose();

emit(`# ${checks} checks, ${mismatches} mismatch${mismatches === 1 ? "" : "es"}`);
writeFileSync(join(here, "last-run.txt"), `${lines.join("\n")}\n`);
process.exitCode = mismatches === 0 ? 0 : 1;
