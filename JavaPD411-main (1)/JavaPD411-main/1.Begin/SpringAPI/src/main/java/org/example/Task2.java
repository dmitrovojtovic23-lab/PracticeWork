package org.example;

import java.io.*;
import java.util.*;

public class Task2 {
    public static void run(Scanner scanner) {
        System.out.print("Шлях до файлу: ");
        String path = scanner.nextLine();
        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            String longest = "", line;
            while ((line = br.readLine()) != null) {
                if (line.length() > longest.length()) longest = line;
            }
            System.out.println("Довжина: " + longest.length() + ", Рядок: " + longest);
        } catch (IOException e) { e.printStackTrace(); }
    }
}