package de.pdinklag.mcstats.bukkit;

import org.bukkit.scheduler.BukkitRunnable;

import de.pdinklag.mcstats.ConsoleWriter;

public class BukkitUpdateTask extends BukkitRunnable {
    private final BukkitUpdater updater;
    private final ConsoleWriter consoleWriter;
    private boolean updating = false;

    public BukkitUpdateTask(BukkitUpdater updater, ConsoleWriter consoleWriter) {
        this.updater = updater;
        this.consoleWriter = consoleWriter;
    }

    @Override
    public void run() {
        if(!updating) {
            updating = true;
            updater.run(consoleWriter);
            updating = false;
        }
    }
}
