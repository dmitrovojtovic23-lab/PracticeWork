package org.example;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Fraction {
    private int numerator = 1;
    private int denominator = 2;

    @Override
    public String toString() {
        return "%d/%d".formatted(numerator, denominator);
    }

    private int gcd(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    public void reduce() {
        int gcdValue = gcd(Math.abs(numerator), Math.abs(denominator));
        numerator /= gcdValue;
        denominator /= gcdValue;
    }

    public void add(Fraction other) {
        numerator = numerator * other.denominator + other.numerator * denominator;
        denominator = denominator * other.denominator;
        reduce();
    }

    public void subtract(Fraction other) {
        numerator = numerator * other.denominator - other.numerator * denominator;
        denominator = denominator * other.denominator;
        reduce();
    }

    public void multiply(Fraction other) {
        numerator *= other.numerator;
        denominator *= other.denominator;
        reduce();
    }

    public void divide(Fraction other) {
        numerator *= other.denominator;
        denominator *= other.numerator;
        reduce();
    }

    public double toDouble() {
        return (double) numerator / denominator;
    }
}
