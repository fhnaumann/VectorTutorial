package io.github.wand555;

import org.bukkit.Bukkit;
import org.bukkit.Color;
import org.bukkit.entity.Player;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.util.Vector;

public class Main extends JavaPlugin {

    @Override
    public void onEnable() {
        Player player = Bukkit.getPlayer("wand555");
        //DisplayUtil.showXZPlaneRepeat(new Vector(0d, player.getLocation().getY(), 0d), 5, Color.RED, player.getWorld(), this);
        DisplayUtil.showBasisVectorRepeat(player.getLocation().toVector(), 5, 15, true, player.getWorld(), this);
        DisplayUtil.showVectorRepeat(new Vector(4, 2, 4), player.getLocation().toVector(), 10, Color.PURPLE, true, player.getWorld(), this);
    }
}
