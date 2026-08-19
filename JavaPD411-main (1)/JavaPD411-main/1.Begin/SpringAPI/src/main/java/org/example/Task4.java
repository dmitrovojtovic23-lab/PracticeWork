package org.example;
import java.io.*;
import java.util.*;

public class Task4 {
    public static void run(Scanner scanner) {
        System.out.print("Шлях до файлу: ");
        String path = scanner.nextLine();
        System.out.print("Кількість чисел: ");
        int n = scanner.nextInt();
        int[] arr = new int[n];
        List<Integer> even = new ArrayList<>(), odd = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            arr[i] = scanner.nextInt();
            if (arr[i] % 2 == 0) even.add(arr[i]); else odd.add(arr[i]);
        }
        scanner.nextLine();
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(path))) {
            for (int x : arr) bw.write(x + " "); bw.newLine();
            for (int x : even) bw.write(x + " "); bw.newLine();
            for (int x : odd) bw.write(x + " "); bw.newLine();
            for (int i = n - 1; i >= 0; i--) bw.write(arr[i] + " ");
        } catch (IOException e) { e.printStackTrace(); }
    }
}
