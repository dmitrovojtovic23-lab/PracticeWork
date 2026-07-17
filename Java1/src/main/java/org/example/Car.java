package org.example;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Car {
    private String name = "Camry";
    private String manufacturer = "Toyota";
    private int year = 2015;
    private double volume = 3.5;

    @Override
    public String toString() {
        return "Name: %s, Manufacturer: %s, Year: %d, Volume:%.2f".formatted(name, manufacturer, year, volume);
    }
}
