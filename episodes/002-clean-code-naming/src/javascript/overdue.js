// Episode 002 — intention-revealing names (JavaScript)

const MS_PER_DAY = 1000 * 60 * 60 * 24;

/**
 * Return how many days late a book was returned (0 if on time).
 * @param {Date} dueDate
 * @param {Date} returnedDate
 * @returns {number}
 */
function daysOverdue(dueDate, returnedDate) {
  const lateDays = Math.round((returnedDate - dueDate) / MS_PER_DAY);
  return Math.max(lateDays, 0);
}

function main() {
  const due = new Date("2026-07-01");
  const returned = new Date("2026-07-12");
  console.log(`Days overdue: ${daysOverdue(due, returned)}`);
}

if (require.main === module) {
  main();
}

module.exports = { daysOverdue };
