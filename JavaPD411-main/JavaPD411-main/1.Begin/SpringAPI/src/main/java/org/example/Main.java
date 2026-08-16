package org.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Main {
    public static void main(String[] args) {
        System.out.println("Привіт козаки :)");
        SpringApplication.run(Main.class, args);
        new Task1().run();
        new Task2().run();
        new Task3().run();
        new Task4().run();
    }
}