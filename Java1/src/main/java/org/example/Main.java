package org.example;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Your time is limited,");
        System.out.println("    so don't waste it");
        System.out.println("        living someone else's life\"");
        System.out.println("            Steve Jobs");

        System.out.print("Enter first number: ");
        int a = scanner.nextInt();
        System.out.print("Enter second number: ");
        int b = scanner.nextInt();
        System.out.println("Sum: " + (a + b));

        System.out.print("Enter three digit number: ");
        int num = scanner.nextInt();
        System.out.println("Number: " + num);

        System.out.print("Enter six digit number: ");
        long num2 = scanner.nextLong();
        System.out.println("Number: " + num2);

        System.out.print("Enter month (1-12): ");
        int month = scanner.nextInt();
        if (month == 12 || month == 1 || month == 2) {
            System.out.println("Season: Winter");
        } else if (month == 3 || month == 4 || month == 5) {
            System.out.println("Season: Spring");
        } else if (month == 6 || month == 7 || month == 8) {
            System.out.println("Season: Summer");
        } else if (month == 9 || month == 10 || month == 11) {
            System.out.println("Season: Autumn");
        } else {
            System.out.println("Invalid month");
        }

        System.out.print("Enter meters: ");
        int meters = scanner.nextInt();
        System.out.println(meters + " m = " + (meters * 1000) + " mm = " + (meters * 100) + " cm");

        System.out.print("Enter first number: ");
        int c = scanner.nextInt();
        System.out.print("Enter second number: ");
        int d = scanner.nextInt();
        int min = c;
        if (d < min) {
            min = d;
        }
        int max = c;
        if (d > max) {
            max = d;
        }
        System.out.println("Normalized: [" + min + ", " + max + "]");

        System.out.print("Enter number: ");
        int n = scanner.nextInt();
        for (int i = 1; i <= 10; i++) {
            System.out.println(n + " * " + i + " = " + (n * i));
        }

        System.out.print("Enter array size: ");
        int size = scanner.nextInt();
        int[] arr = new int[size];
        System.out.println("Enter array elements:");
        for (int i = 0; i < size; i++) {
            arr[i] = scanner.nextInt();
        }
        int minVal = arr[0];
        int maxVal = arr[0];
        for (int i = 0; i < size; i++) {
            if (arr[i] < minVal) {
                minVal = arr[i];
            }
            if (arr[i] > maxVal) {
                maxVal = arr[i];
            }
        }
        int zeroCount = 0;
        for (int i = 0; i < size; i++) {
            if (arr[i] == 0) {
                zeroCount++;
            }
        }
        System.out.println("Min: " + minVal + ", Max: " + maxVal + ", Count of zeros: " + zeroCount);

        System.out.print("Enter array size: ");
        int size2 = scanner.nextInt();
        int[] arr2 = new int[size2];
        System.out.println("Enter array elements:");
        for (int i = 0; i < size2; i++) {
            arr2[i] = scanner.nextInt();
        }
        System.out.print("Unique elements: ");
        for (int i = 0; i < size2; i++) {
            boolean unique = true;
            for (int j = 0; j < size2; j++) {
                if (i != j && arr2[i] == arr2[j]) {
                    unique = false;
                }
            }
            if (unique) {
                System.out.print(arr2[i] + " ");
            }
        }
        System.out.println();

        System.out.print("Enter line: ");
        scanner.nextLine();
        String line = scanner.nextLine();
        System.out.print("Enter symbol: ");
        String symbol = scanner.nextLine();
        for (int i = 0; i < line.length(); i++) {
            System.out.print(symbol);
        }
        System.out.println();
        System.out.println(line);
        for (int i = 0; i < line.length(); i++) {
            System.out.print(symbol);
        }
        System.out.println();

        System.out.print("Enter array size: ");
        int size3 = scanner.nextInt();
        int[] arr3 = new int[size3];
        System.out.println("Enter array elements:");
        for (int i = 0; i < size3; i++) {
            arr3[i] = scanner.nextInt();
        }
        for (int i = 0; i < size3; i++) {
            for (int j = 0; j < size3 - 1; j++) {
                if (arr3[j] > arr3[j + 1]) {
                    int temp = arr3[j];
                    arr3[j] = arr3[j + 1];
                    arr3[j + 1] = temp;
                }
            }
        }
        System.out.print("Sorted array: ");
        for (int i = 0; i < size3; i++) {
            System.out.print(arr3[i] + " ");
        }
        System.out.println();

        scanner.close();
    }
}
