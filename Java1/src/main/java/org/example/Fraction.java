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
}
