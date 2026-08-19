package org.example;

import java.io.*;
import java.util.*;

public class Task1 {
    public static void run(Scanner scanner) {
        System.out.print("Шлях до першого файлу: ");
        String path1 = scanner.nextLine();
        System.out.print("Шлях до другого файлу: ");
        String path2 = scanner.nextLine();
        try {
            List<String> list1 = new ArrayList<>();
            List<String> list2 = new ArrayList<>();
            try (BufferedReader br1 = new BufferedReader(new FileReader(path1))) {
                String line;
                while ((line = br1.readLine()) != null) list1.add(line);
            }
            try (BufferedReader br2 = new BufferedReader(new FileReader(path2))) {
                String line;
                while ((line = br2.readLine()) != null) list2.add(line);
            }
            System.out.println("Рядки з 1, яких немає у 2:");
            for (String s : list1) if (!list2.contains(s)) System.out.println(s);
            System.out.println("Рядки з 2, яких немає у 1:");
            for (String s : list2) if (!list1.contains(s)) System.out.println(s);
        } catch (IOException e) { e.printStackTrace(); }
    }
}
