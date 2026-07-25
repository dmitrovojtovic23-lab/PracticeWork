package org.example;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Device {
    protected String brand;
    protected double price;

    public void sound() {
    }

    public void show() {
        System.out.println("Brand: " + brand + ", Price: " + price);
    }

    public void desc() {
        System.out.println("Device: " + brand);
    }
}

@Data
@AllArgsConstructor
@NoArgsConstructor
class Notebook extends Device {
    private double screenSize;
    private String processor;

    public Notebook(String brand, double price, double screenSize, String processor) {
        super(brand, price);
        this.screenSize = screenSize;
        this.processor = processor;
    }

    @Override
    public void sound() {
        System.out.println("Beep!");
    }

    @Override
    public void show() {
        System.out.println("Brand: " + brand + ", Price: " + price + ", Screen: " + screenSize + "in, Processor: " + processor);
    }

    @Override
    public void desc() {
        System.out.println("Notebook: " + brand + " (" + screenSize + "\" " + processor + ")");
    }
}

@Data
@AllArgsConstructor
@NoArgsConstructor
class Microwave extends Device {
    private double capacity;
    private int power;

    public Microwave(String brand, double price, double capacity, int power) {
        super(brand, price);
        this.capacity = capacity;
        this.power = power;
    }

    @Override
    public void sound() {
        System.out.println("Bip bip!");
    }

    @Override
    public void show() {
        System.out.println("Brand: " + brand + ", Price: " + price + ", Capacity: " + capacity + "L, Power: " + power + "W");
    }

    @Override
    public void desc() {
        System.out.println("Microwave: " + brand + " (" + capacity + "L, " + power + "W)");
    }
}

@Data
@AllArgsConstructor
@NoArgsConstructor
class Car extends Device {
    private String model;
    private int yearOfProduction;

    public Car(String brand, double price, String model, int yearOfProduction) {
        super(brand, price);
        this.model = model;
        this.yearOfProduction = yearOfProduction;
    }

    @Override
    public void sound() {
        System.out.println("Vroom!");
    }

    @Override
    public void show() {
        System.out.println("Brand: " + brand + ", Price: " + price + ", Model: " + model + ", Year: " + yearOfProduction);
    }

    @Override
    public void desc() {
        System.out.println("Car: " + brand + " " + model + " (" + yearOfProduction + ")");
    }
}
