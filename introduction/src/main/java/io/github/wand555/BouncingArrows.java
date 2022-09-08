package io.github.wand555;

import com.jeff_media.morepersistentdatatypes.DataType;
import org.bukkit.Color;
import org.bukkit.Location;
import org.bukkit.NamespacedKey;
import org.bukkit.World;
import org.bukkit.block.BlockFace;
import org.bukkit.entity.Arrow;
import org.bukkit.event.EventHandler;
import org.bukkit.event.HandlerList;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.ProjectileHitEvent;
import org.bukkit.event.entity.ProjectileLaunchEvent;
import org.bukkit.persistence.PersistentDataContainer;
import org.bukkit.persistence.PersistentDataType;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitTask;
import org.bukkit.util.Vector;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * Makes arrows bouncy by reflecting them upon impact with a block.
 */
public class BouncingArrows implements Listener {

    /**
     * The java plugin mainly needed for registering the events.
     */
    private final JavaPlugin plugin;

    /**
     * Flag to plot interesting vectors in the calculation.
     */
    private boolean showVisually;

    /**
     * Key for PDC containing the position as a vector.
     */
    private final NamespacedKey posKey;
    /**
     * Key for PDC containing the current number of reflections that occurred on the arrow the PDC is attached to.
     */
    private final NamespacedKey reflCountKey;

    /**
     * Maximum number of times an arrow may bounce/reflect of a surface.
     */
    private final int maxReflCount;

    /**
     * Keeps track of repeating tasks for each arrow when {@link BouncingArrows#showVisually} is true. Otherwise not used.
     */
    private final Map<UUID, List<BukkitTask>> visualTrackingMap = new HashMap<>();

    /**
     * Creates an object containing all the necessary information.
     * @param reflectionCount maximum number of times an arrow may bounce/reflect.
     * @param plugin The java plugin mainly needed for registering the events.
     */
    public BouncingArrows(int reflectionCount, JavaPlugin plugin) {
        this.plugin = plugin;
        this.maxReflCount = reflectionCount;
        posKey = new NamespacedKey(plugin, "pos");
        reflCountKey = new NamespacedKey(plugin, "no_reflection");
    }

    /**
     * Registers all the events.
     * @param showVisually if interesting vectors should be drawn via the {@link DisplayUtil} class.
     */
    public void start(boolean showVisually) {
        this.showVisually = showVisually;
        plugin.getServer().getPluginManager().registerEvents(this, plugin);
    }

    /**
     * Terminates the project. Cleans up afterwards.
     */
    public void end() {
        HandlerList.unregisterAll(this);
    }

    @EventHandler
    private void onLaunch(ProjectileLaunchEvent event) {
        if(event.getEntity() instanceof Arrow arrow) {
            PersistentDataContainer pdc = event.getEntity().getPersistentDataContainer();
            Location spawnLoc = event.getLocation();
            //arrow is launched by a player and not the result of a previous reflection
            if(!pdc.has(reflCountKey, PersistentDataType.INTEGER)) {
                //write launching position into PDC of the arrow
                pdc.set(posKey, DataType.VECTOR, spawnLoc.toVector());
                //start the reflection count at 0
                pdc.set(reflCountKey, PersistentDataType.INTEGER, 0);
                // fill tracking map needed for plotting vectors
                if(showVisually) {
                    visualTrackingMap.put(arrow.getUniqueId(), new ArrayList<>());
                }
            }
            // fill tracking map needed for plotting vectors
            else if(showVisually) {
                visualTrackingMap.compute(arrow.getUniqueId(), (uuid, bukkitTasks) -> bukkitTasks);
            }
        }
    }

    @EventHandler
    private void onHit(ProjectileHitEvent event) {
        //don't do anything if something other than a block was hit (e.g. an entity)
        if(event.getHitBlock() == null) {
            return;
        }
        BlockFace hitFace = event.getHitBlockFace();
        PersistentDataContainer pdc = event.getEntity().getPersistentDataContainer();

        //don't do anything if the PDC of the projectile does not have our set PDC
        if(!pdc.has(posKey, DataType.VECTOR)) {
            return;
        }

        //if the arrow has reached its maximum amount of bounces, stop early
        if(pdc.get(reflCountKey, PersistentDataType.INTEGER) >= maxReflCount) {
            visualTrackingMap.remove(event.getEntity().getUniqueId()).forEach(BukkitTask::cancel);
            // visualTrackingMap.get(event.getEntity().getUniqueId()).forEach(BukkitTask::cancel);
            return;
        }
        Vector prevVec = pdc.get(posKey, DataType.VECTOR);
        Vector currentVec = event.getEntity().getLocation().toVector();
        //calculate the incoming (I) vector
        Vector incoming = currentVec.clone().subtract(prevVec).normalize();
        //get the normal vector of the plane that was hit
        Vector normal = hitFace.getDirection();

        // formula for reflection: R = I - 2*(<I,N>)*N

        // <I,N>
        double dot = incoming.dot(normal);

        // if I and N are (almost) parallel the dot product will be 0.
        // In that case just use the normal vector as the reflection vector.
        Vector reflecting;
        if(Math.abs(dot) < 1e-5) {
            reflecting = normal.clone();
        }
        // else use regular formula
        else {
            // R = I - 2*(<I,N>)*N
            reflecting = incoming.clone().subtract(normal.clone().multiply(2 * dot)).normalize();
        }
        if(Double.isNaN(reflecting.getX()) || Double.isNaN(reflecting.getY()) || Double.isNaN(reflecting.getZ())) {
            visualTrackingMap.remove(event.getEntity().getUniqueId()).forEach(BukkitTask::cancel);
            //visualTrackingMap.get(event.getEntity().getUniqueId()).forEach(BukkitTask::cancel);
            return;
        }
        // finding the speed the reflected arrow should spawn at
        float speed = (float) Math.max(event.getEntity().getVelocity().length() / 2, 0.3);

        // formality: remove the arrow that just landed
        event.getEntity().remove();

        World world = event.getEntity().getWorld();
        //spawn in the reflected arrow
        Arrow reflectedArrow = world.spawnArrow(event.getEntity().getLocation(), reflecting, speed, 0);
        Vector reflectedArrowVec = reflectedArrow.getLocation().toVector();
        // write launching position into PDC of the arrow
        reflectedArrow.getPersistentDataContainer().set(posKey, DataType.VECTOR, reflectedArrowVec);
        // increment the reflection count by one
        int tempReflCount = pdc.get(reflCountKey, PersistentDataType.INTEGER);
        reflectedArrow.getPersistentDataContainer().set(reflCountKey, PersistentDataType.INTEGER, ++tempReflCount);

        // plot the three interesting vectors
        if(showVisually) {
            BukkitTask showIncomingTask = DisplayUtil.showVectorRepeat(incoming, event.getEntity().getLocation().toVector().subtract(incoming), 8, Color.BLUE, true, world, plugin);
            BukkitTask showNormalTask = DisplayUtil.showVectorRepeat(normal, event.getEntity().getLocation().toVector(), 8, Color.GREEN, true, world, plugin);
            BukkitTask showReflectingTask = DisplayUtil.showVectorRepeat(reflecting, event.getEntity().getLocation().toVector(), 8, Color.PURPLE, true, world, plugin);

            List<BukkitTask> prevTasks = visualTrackingMap.remove(event.getEntity().getUniqueId());
            prevTasks.add(showIncomingTask);
            prevTasks.add(showNormalTask);
            prevTasks.add(showReflectingTask);
            visualTrackingMap.put(reflectedArrow.getUniqueId(), prevTasks);
        }
    }
}
