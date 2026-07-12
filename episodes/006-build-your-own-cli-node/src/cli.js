// Episode 006 — build your own CLI (Node): a tiny wordcount tool.
"use strict";

const fs = require("fs");

/**
 * Count lines, words, and characters. Pure and testable.
 * @param {string} text
 * @returns {{lines: number, words: number, chars: number}}
 */
function count(text) {
  const newlineCount = (text.match(/\n/g) || []).length;
  const lines = newlineCount + (text && !text.endsWith("\n") ? 1 : 0);
  const words = text.split(/\s+/).filter(Boolean).length;
  const chars = text.length;
  return { lines, words, chars };
}

function readInput(args) {
  const path = args.find((a) => !a.startsWith("-"));
  if (path) {
    return fs.readFileSync(path, "utf8");
  }
  return fs.readFileSync(0, "utf8"); // fd 0 == stdin
}

function main(argv) {
  const args = argv.slice(2);
  const text = readInput(args);
  const result = count(text);

  const wantLines = args.includes("-l") || args.includes("--lines");
  const wantWords = args.includes("-w") || args.includes("--words");
  const wantChars = args.includes("-c") || args.includes("--chars");
  const showAll = !(wantLines || wantWords || wantChars);

  const parts = [];
  if (showAll || wantLines) parts.push(result.lines);
  if (showAll || wantWords) parts.push(result.words);
  if (showAll || wantChars) parts.push(result.chars);
  console.log(parts.join("\t"));
  return 0;
}

if (require.main === module) {
  process.exit(main(process.argv));
}

module.exports = { count };
