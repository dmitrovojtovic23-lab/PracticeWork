package org.example;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Human {
    private int age = 20;
    private String name = "Ivan";

    @Override
    public String toString() {
        return "Age: " + age + " Name: " + name;
    }
}

@Data
@AllArgsConstructor
@NoArgsConstructor
class Builder extends Human {
    private String company;
}

@Data
@AllArgsConstructor
@NoArgsConstructor
class Sailor extends Human {
    private String ship;
}

@Data
@AllArgsConstructor
@NoArgsConstructor
class Pilot extends Human {
    private String aircraft;
}
