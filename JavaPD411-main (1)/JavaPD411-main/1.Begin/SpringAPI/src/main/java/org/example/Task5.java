package org.example;

import java.io.*;
import java.util.*;

class Employee {
    String name, surname;
    int age;
    Employee(String n, String s, int a) { name = n; surname = s; age = a; }
    public String toString() { return name + " " + surname + ", " + age; }
}

public class Task5 {
    public static void run(Scanner scanner) {
        List<Employee> emps = new ArrayList<>();
        System.out.print("Шлях до файлу: ");
        String path = scanner.nextLine();
        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] p = line.split(",");
                if (p.length == 3) emps.add(new Employee(p[0], p[1], Integer.parseInt(p[2])));
            }
        } catch (IOException ignored) {}

        System.out.println("1. Додати, 2. Редагувати, 3. Видалити, 4. Пошук, 0. Вихід");
        int ch = scanner.nextInt(); scanner.nextLine();
        if (ch == 1) {
            System.out.print("Ім'я, Прізвище, Вік: ");
            String[] data = scanner.nextLine().split(" ");
            emps.add(new Employee(data[0], data[1], Integer.parseInt(data[2])));
        }
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(path))) {
            for (Employee e : emps) bw.write(e.name + "," + e.surname + "," + e.age + "\\n");
        } catch (IOException e) { e.printStackTrace(); }
    }
}