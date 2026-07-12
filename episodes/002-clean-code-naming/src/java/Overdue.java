// Episode 002 — intention-revealing names (Java)
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

public class Overdue {

  /** Return how many days late a book was returned (0 if on time). */
  public static long daysOverdue(LocalDate dueDate, LocalDate returnedDate) {
    long lateDays = ChronoUnit.DAYS.between(dueDate, returnedDate);
    return Math.max(lateDays, 0);
  }

  public static void main(String[] args) {
    LocalDate due = LocalDate.of(2026, 7, 1);
    LocalDate returned = LocalDate.of(2026, 7, 12);
    System.out.println("Days overdue: " + daysOverdue(due, returned));
  }
}
