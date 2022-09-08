package io.github.wand555;

import org.bukkit.Bukkit;
import org.bukkit.Color;
import org.bukkit.Location;
import org.bukkit.entity.LivingEntity;
import org.bukkit.entity.Player;
import org.bukkit.entity.Sheep;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitTask;
import org.bukkit.util.Vector;

/**
 * Makes an entity (sheep in this example) always look at the player.
 */
public class EntityFacePlayer {

    /**
     * The java plugin mainly needed to start the scheduler.
     */
    private final JavaPlugin plugin;

    /**
     * The player the entity is going to look at.
     */
    private final Player playerToLookAt;

    /**
     * The bukkit task running as soon as {@link EntityFacePlayer#start(boolean)} is called.
     */
    private BukkitTask task;


    /**
     * Creates an object containing all the necessary information.
     * @param playerToLookAt The player the entity is going to look at.
     * @param plugin The java plugin mainly needed to start the scheduler.
     */
    public EntityFacePlayer(Player playerToLookAt, JavaPlugin plugin) {
        this.playerToLookAt = playerToLookAt;
        this.plugin = plugin;
    }

    /**
     * Starts the project.
     * @param showVisually if interesting vectors should be drawn via the {@link DisplayUtil} class.
     */
    public void start(boolean showVisually) {
        if(!playerToLookAt.isOnline()) {
            return;
        }
        //spawn in the sheep
        LivingEntity entity = playerToLookAt.getWorld().spawn(playerToLookAt.getLocation(), Sheep.class, sheep -> {
            sheep.setAI(false);
            sheep.setInvulnerable(true);
            sheep.setGravity(false);
        });
        //start a repeating task
        Bukkit.getScheduler().runTaskTimer(plugin, bukkitTask -> {
            this.task = bukkitTask;
            //if anything undesired happened, stop immediately
            if(!playerToLookAt.isOnline() || !playerToLookAt.isValid() || !entity.isValid()) {
                end();
                return;
            }
            Vector playerVec = playerToLookAt.getEyeLocation().toVector().clone();
            Vector entityVec = entity.getEyeLocation().toVector();
            Vector entityToLookAtVec = playerVec.subtract(entityVec);
            // plot interesting vector
            if(showVisually) {
                Bukkit.getScheduler().runTaskLaterAsynchronously(plugin, () -> DisplayUtil.showVector(entityToLookAtVec, entity.getEyeLocation().toVector(), 15, Color.PURPLE, true, playerToLookAt.getWorld()), 0L);
            }

            Location loc = entity.getLocation().setDirection(entityToLookAtVec);
            entity.teleport(loc);
        }, 0L, 1L);
    }

    /**
     * Terminates the project. Cleans up afterwards.
     */
    public void end() {
        task.cancel();
    }
}
