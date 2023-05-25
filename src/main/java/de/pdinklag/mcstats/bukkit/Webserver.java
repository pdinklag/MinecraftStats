package de.pdinklag.mcstats.bukkit;

import java.nio.file.Path;

public class Webserver {
    private static final String TARGET_DIR_NAME = "stats";

    private final Path target;

    public Webserver(Path documentRoot) {
        this.target = documentRoot.resolve(TARGET_DIR_NAME);
    }

    public Path getTarget() {
        return target;
    }
}
