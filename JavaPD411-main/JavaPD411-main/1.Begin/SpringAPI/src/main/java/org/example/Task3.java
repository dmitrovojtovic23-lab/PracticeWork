package org.example;


@FunctionalInterface
interface QuadFunction<T, U, V, W, R> {
    R apply(T t, U u, V v, W w);
}

public class Task3 {
    public void run() {
        QuadFunction<Integer, Integer, Integer, Integer, Integer> max = (a, b, c, d) -> Math.max(Math.max(a, b), Math.max(c, d));
        QuadFunction<Integer, Integer, Integer, Integer, Integer> min = (a, b, c, d) -> Math.min(Math.min(a, b), Math.min(c, d));

        System.out.println(max.apply(5, 12, 3, 9));
        System.out.println(min.apply(5, 12, 3, 9));
    }
}
