package org.example;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Book {
    private String name = "Atomic Habits";
    private String authorName = "James Clear";
    private int publishYear = 2018;
    private String publisher = "British Book";
    private String genre = "Self-Help";
    private int numberOfPages = 308;

    @Override
    public String toString() {
        return "Name: %s Author: %s Year: %d publisher: %s genre: %s pages: %d".formatted(name, authorName, publishYear, publisher, genre, numberOfPages);
    }
}
