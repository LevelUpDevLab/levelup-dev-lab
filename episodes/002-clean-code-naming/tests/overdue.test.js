// Sanity test for episode 002 (JavaScript) — plain Node assert, no framework.
const assert = require("assert");
const { daysOverdue } = require("../src/javascript/overdue");

assert.strictEqual(
  daysOverdue(new Date("2026-07-01"), new Date("2026-07-12")),
  11,
);
assert.strictEqual(
  daysOverdue(new Date("2026-07-12"), new Date("2026-07-01")),
  0,
);

console.log("ok - episode 002 javascript sanity test passed");
