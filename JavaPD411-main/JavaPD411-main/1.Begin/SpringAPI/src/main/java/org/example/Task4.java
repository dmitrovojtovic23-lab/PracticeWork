package org.example;


import java.util.function.Predicate;

public class Task4 {
    public void run() {
        int[] arr = { -5, 2, 10, 15, -3, 8 };
        System.out.println(sum(arr, n -> n == 10));
        System.out.println(sum(arr, n -> n < 3 || n > 12));
        System.out.println(sum(arr, n -> n > 0));
        System.out.println(sum(arr, n -> n < 0));
    }

    private int sum(int[] array, Predicate<Integer> condition) {
        int s = 0;
        for (int n : array) {
            if (condition.test(n)) s += n;
        }
        return s;
    }
}
