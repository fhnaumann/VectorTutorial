package io.github.wand555;

import org.bukkit.Bukkit;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.LivingEntity;
import org.bukkit.entity.Player;
import org.bukkit.plugin.java.JavaPlugin;

public class Main extends JavaPlugin implements CommandExecutor {

    @Override
    public void onEnable() {
        getCommand("entity-look-at-player").setExecutor(this);
        getCommand("arrow-reflection").setExecutor(this);
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if(!(sender instanceof Player)) {
            return false;
        }
        Player player = (Player) sender;
        if(command.getName().equals("entity-look-at-player")) {
            EntityFacePlayer entityFacePlayer = new EntityFacePlayer(player, this);
            entityFacePlayer.start(true);
            return true;
        }
        if(command.getName().equals("arrow-reflection")) {
            BouncingArrows bouncingArrows = new BouncingArrows(5, this);
            bouncingArrows.start(true);
        }
        return false;
    }
}
