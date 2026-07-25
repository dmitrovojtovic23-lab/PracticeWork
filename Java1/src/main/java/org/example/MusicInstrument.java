package org.example;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.util.ArrayList;
import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class MusicInstrument {
    protected String name;
    protected String type;
    private List<String> history = new ArrayList<>();

    public void sound() {
    }

    public void show() {
        System.out.println("Name: " + name + ", Type: " + type);
    }

    public void desc() {
        System.out.println("Instrument: " + name);
    }

    public void addHistory(String event) {
        history.add(event);
    }

    public void showHistory() {
        System.out.println("History of " + name + ":");
        for (String event : history) {
            System.out.println("  - " + event);
        }
    }
}

@Data
@AllArgsConstructor
@NoArgsConstructor
class Violin extends MusicInstrument {
    private int strings;

    public Violin(String name, String type, int strings) {
        super(name, type);
        this.strings = strings;
    }

    @Override
    public void sound() {
        System.out.println("Violin sound: bow on strings");
    }

    @Override
    public void desc() {
        System.out.println("Violin: " + name + " (" + strings + " strings)");
    }
}

@Data
@AllArgsConstructor
@NoArgsConstructor
class Trombone extends MusicInstrument {
    private double slideRange;

    public Trombone(String name, String type, double slideRange) {
        super(name, type);
        this.slideRange = slideRange;
    }

    @Override
    public void sound() {
        System.out.println("Trombone sound: slide moves");
    }

    @Override
    public void desc() {
        System.out.println("Trombone: " + name + " (slide range: " + slideRange + ")");
    }
}

@Data
@AllArgsConstructor
@NoArgsConstructor
class Trumpet extends MusicInstrument {
    private int valves;

    public Trumpet(String name, String type, int valves) {
        super(name, type);
        this.valves = valves;
    }

    @Override
    public void sound() {
        System.out.println("Trumpet sound: bright and clear");
    }

    @Override
    public void desc() {
        System.out.println("Trumpet: " + name + " (" + valves + " valves)");
    }
}

@Data
@AllArgsConstructor
@NoArgsConstructor
class Vibraphone extends MusicInstrument {
    private int bars;

    public Vibraphone(String name, String type, int bars) {
        super(name, type);
        this.bars = bars;
    }

    @Override
    public void sound() {
        System.out.println("Vibraphone sound: resonant tones");
    }

    @Override
    public void desc() {
        System.out.println("Vibraphone: " + name + " (" + bars + " bars)");
    }
}
