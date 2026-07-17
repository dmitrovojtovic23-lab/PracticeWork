package org.example;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Country {
    private int population = 500000;
    private String name = "Uganda";
    private double area = 40004.59;
    private String independenceDay = "1950-07-17";

    @Override
    public String toString() {
        return "Name: %s Population: %d Area: %.2f Independence: %s".formatted(name, population, area, independenceDay);
    }
}
