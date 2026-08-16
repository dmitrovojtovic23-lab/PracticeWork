package org.example;
import java.time.LocalDate;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.function.Predicate;

public class Task1 {
    public void run() {
        Predicate<LocalDate> isLeapYear = date -> date.isLeapYear();
        BiFunction<LocalDate, LocalDate, Long> daysBetween = (d1, d2) -> java.time.temporal.ChronoUnit.DAYS.between(d1, d2);
        BiFunction<LocalDate, LocalDate, Long> weeksBetween = (d1, d2) -> java.time.temporal.ChronoUnit.WEEKS.between(d1, d2);
        Function<LocalDate, java.time.DayOfWeek> dayOfWeek = date -> date.getDayOfWeek();

        System.out.println(isLeapYear.test(LocalDate.of(2024, 1, 1)));
        System.out.println(daysBetween.apply(LocalDate.of(2026, 1, 1), LocalDate.of(2026, 8, 16)));
        System.out.println(weeksBetween.apply(LocalDate.of(2026, 1, 1), LocalDate.of(2026, 8, 16)));
        System.out.println(dayOfWeek.apply(LocalDate.of(1969, 7, 20)));
    }
}
