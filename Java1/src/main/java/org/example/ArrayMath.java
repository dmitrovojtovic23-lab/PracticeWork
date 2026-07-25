package org.example;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class ArrayMath implements IMath {
    private int[] arr;

    @Override
    public int Max() {
        if (arr == null || arr.length == 0) return 0;
        int max = arr[0];
        for (int num : arr) {
            if (num > max) max = num;
        }
        return max;
    }

    @Override
    public int Min() {
        if (arr == null || arr.length == 0) return 0;
        int min = arr[0];
        for (int num : arr) {
            if (num < min) min = num;
        }
        return min;
    }

    @Override
    public float Avg() {
        if (arr == null || arr.length == 0) return 0;
        int sum = 0;
        for (int num : arr) {
            sum += num;
        }
        return (float) sum / arr.length;
    }
}
