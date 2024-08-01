package de.pdinklag.mcstats.bukkit.webserver;

import java.lang.reflect.Constructor;
import java.nio.file.Path;

import org.bukkit.Server;
import org.bukkit.plugin.Plugin;
import org.bukkit.plugin.PluginManager;

public abstract class PluginWebserver {
    private static <T extends PluginWebserver> T getPluginWebserver(PluginManager pluginManager, String pluginName,
            Class<T> clazz) {
        try {
            Plugin plugin = pluginManager.getPlugin(pluginName);
            if (plugin != null) {
                Constructor<T> ctor = clazz.getConstructor(Plugin.class);
                return ctor.newInstance(plugin);
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return null;
    }

    public static PluginWebserver find(Server server) {
        final PluginManager pluginManager = server.getPluginManager();

        PluginWebserver webserver;
        if ((webserver = getPluginWebserver(pluginManager, "dynmap", DynmapWebserver.class)) != null)
            return webserver;
        if ((webserver = getPluginWebserver(pluginManager, "BlueMap", BlueMapWebserver.class)) != null)
            return webserver;
        if ((webserver = getPluginWebserver(pluginManager, "squaremap", SquaremapWebserver.class)) != null)
            return webserver;
        if ((webserver = getPluginWebserver(pluginManager, "Pl3xMap", Pl3xMapWebserver.class)) != null)
            return webserver;
        return null;
    }

    public abstract Path getDocumentRoot();
}
