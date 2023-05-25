package de.pdinklag.mcstats.bukkit;

import org.bukkit.Server;

import de.pdinklag.mcstats.Config;
import de.pdinklag.mcstats.LogWriter;
import de.pdinklag.mcstats.PlayerProfileProviderList;
import de.pdinklag.mcstats.Updater;

public class BukkitUpdater extends Updater {
    private final Server server;

    public BukkitUpdater(Server server, Config config, LogWriter log) {
        super(config, log);
        this.server = server;
    }

    @Override
    protected void gatherLocalProfileProviders(PlayerProfileProviderList providers) {
        super.gatherLocalProfileProviders(providers);
        providers.addFirst(new OfflinePlayerProfileProvider(server));
    }

    @Override
    protected String getServerMotd() {
        return server.getMotd();
    }

    @Override
    public void run() {
        log.writeLine("Updating ...");
        super.run();
        log.writeLine("Update complete.");
    }
}
