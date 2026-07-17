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
