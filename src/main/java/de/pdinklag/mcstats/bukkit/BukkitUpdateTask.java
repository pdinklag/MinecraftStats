package de.pdinklag.mcstats.bukkit;

import org.bukkit.scheduler.BukkitRunnable;

public class BukkitUpdateTask extends BukkitRunnable {
    private final BukkitUpdater updater;
    private boolean updating = false;

    public BukkitUpdateTask(BukkitUpdater updater) {
        this.updater = updater;
    }

    @Override
    public void run() {
        if(!updating) {
            updating = true;
            updater.run();
            updating = false;
        }
    }
}
