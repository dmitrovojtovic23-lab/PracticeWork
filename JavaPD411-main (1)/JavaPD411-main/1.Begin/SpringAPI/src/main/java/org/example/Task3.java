package org.example;

import java.io.*;
import java.util.*;

public class Task3 {
    public static void run(Scanner scanner) {
        System.out.print("Шлях до файлу: ");
        String path = scanner.nextLine();
        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            String line;
            int totalSum = 0;
            while ((line = br.readLine()) != null) {
                if (line.trim().isEmpty()) continue;
                String[] parts = line.trim().split("\\s+");
                int sum = 0, min = Integer.MAX_VALUE, max = Integer.MIN_VALUE;
                for (String p : parts) {
                    int val = Integer.parseInt(p);
                    sum += val;
                    if (val < min) min = val;
                    if (val > max) max = val;
                }
                totalSum += sum;
                System.out.println("Мін: " + min + ", Макс: " + max + ", Сума: " + sum);
            }
            System.out.println("Загальна сума: " + totalSum);
        } catch (IOException e) { e.printStackTrace(); }
    }
}
