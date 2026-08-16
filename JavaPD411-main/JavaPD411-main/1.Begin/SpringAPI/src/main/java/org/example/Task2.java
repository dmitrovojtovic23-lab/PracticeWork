package org.example;

import java.util.function.BiFunction;

public class Task2 {
    public static class Fraction {
        int numerator, denominator;
        public Fraction(int n, int d) { this.numerator = n; this.denominator = d; }
        public String toString() { return numerator + "/" + denominator; }
    }

    public void run() {
        BiFunction<Fraction, Fraction, Fraction> add = (f1, f2) -> new Fraction(f1.numerator * f2.denominator + f2.numerator * f1.denominator, f1.denominator * f2.denominator);
        BiFunction<Fraction, Fraction, Fraction> sub = (f1, f2) -> new Fraction(f1.numerator * f2.denominator - f2.numerator * f1.denominator, f1.denominator * f2.denominator);
        BiFunction<Fraction, Fraction, Fraction> mul = (f1, f2) -> new Fraction(f1.numerator * f2.numerator, f1.denominator * f2.denominator);
        BiFunction<Fraction, Fraction, Fraction> div = (f1, f2) -> new Fraction(f1.numerator * f2.denominator, f1.denominator * f2.numerator);

        System.out.println(add.apply(new Fraction(1, 2), new Fraction(1, 3)));
        System.out.println(sub.apply(new Fraction(1, 2), new Fraction(1, 3)));
        System.out.println(mul.apply(new Fraction(1, 2), new Fraction(1, 3)));
        System.out.println(div.apply(new Fraction(1, 2), new Fraction(1, 3)));
    }
}
