package org.example;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class City {
    private String name = "Lviv";
    private int foundation_date = 1199;
    private int population = 2000000;
    private double area = 250000;

    @Override
    public String toString() {
        return "City name: " + name + " Foundation date: " + foundation_date + " Population: " + population + " City area: " + area;
    }
}
