package org.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.util.Scanner;

@SpringBootApplication
public class Main {
    public static void main(String[] args) {
        System.out.println("Привіт козаки :)");
        SpringApplication.run(Main.class, args);
        Scanner scanner = new Scanner(System.in);
        while (true) {
            System.out.println("Завдання 1");
            System.out.println("Завдання 2");
            System.out.println("Завдання 3");
            System.out.println("Завдання 4");
            System.out.println("Завдання 5");
            System.out.println("Вихід");
            int choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {
                case 1: Task1.run(scanner); break;
                case 2: Task2.run(scanner); break;
                case 3: Task3.run(scanner); break;
                case 4: Task4.run(scanner); break;
                case 5: Task5.run(scanner); break;
                case 0: System.exit(0);
                default: System.out.println("Невірний вибір.");
            }
        }
    }
}