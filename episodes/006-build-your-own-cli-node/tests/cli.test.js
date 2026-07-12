// Sanity test for episode 006 — plain Node assert, no framework.
const assert = require("assert");
const { count } = require("../src/cli");

const c = count("hello there\nfriend\n");
assert.strictEqual(c.lines, 2);
assert.strictEqual(c.words, 3);
assert.strictEqual(c.chars, "hello there\nfriend\n".length);

assert.strictEqual(count("one two").lines, 1);

console.log("ok - episode 006 node sanity test passed");
