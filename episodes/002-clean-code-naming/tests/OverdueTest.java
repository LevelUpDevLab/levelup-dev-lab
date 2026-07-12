// Sanity test for episode 002 (Java) — plain assertions, no JUnit needed.
import java.time.LocalDate;

public class OverdueTest {
  public static void main(String[] args) {
    long late = Overdue.daysOverdue(LocalDate.of(2026, 7, 1), LocalDate.of(2026, 7, 12));
    if (late != 11) {
      System.err.println("FAIL: expected 11, got " + late);
      System.exit(1);
    }
    long onTime = Overdue.daysOverdue(LocalDate.of(2026, 7, 12), LocalDate.of(2026, 7, 1));
    if (onTime != 0) {
      System.err.println("FAIL: expected 0, got " + onTime);
      System.exit(1);
    }
    System.out.println("ok - episode 002 java sanity test passed");
  }
}
