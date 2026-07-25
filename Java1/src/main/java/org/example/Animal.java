package org.example;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Animal {
    protected String name;
    protected int age;
    protected double weight;

    public void sound() {
    }

    public void show() {
        System.out.println("Name: " + name + ", Age: " + age + ", Weight: " + weight);
    }

    public void desc() {
        System.out.println("Animal: " + name);
    }
}

@Data
@AllArgsConstructor
@NoArgsConstructor
class Tiger extends Animal {
    private boolean striped;

    public Tiger(String name, int age, double weight, boolean striped) {
        super(name, age, weight);
        this.striped = striped;
    }

    @Override
    public void sound() {
        System.out.println("Rooooar!");
    }

    @Override
    public void desc() {
        System.out.println("Tiger: " + name + (striped ? " (striped)" : ""));
    }
}

@Data
@AllArgsConstructor
@NoArgsConstructor
class Crocodile extends Animal {
    private int teethCount;

    public Crocodile(String name, int age, double weight, int teethCount) {
        super(name, age, weight);
        this.teethCount = teethCount;
    }

    @Override
    public void sound() {
        System.out.println("Hiss!");
    }

    @Override
    public void desc() {
        System.out.println("Crocodile: " + name + " (" + teethCount + " teeth)");
    }
}

@Data
@AllArgsConstructor
@NoArgsConstructor
class Kangaroo extends Animal {
    private double jumpHeight;

    public Kangaroo(String name, int age, double weight, double jumpHeight) {
        super(name, age, weight);
        this.jumpHeight = jumpHeight;
    }

    @Override
    public void sound() {
        System.out.println("Boom boom!");
    }

    @Override
    public void desc() {
        System.out.println("Kangaroo: " + name + " (can jump " + jumpHeight + " m)");
    }
}
