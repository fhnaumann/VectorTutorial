package io.github.wand555;

import org.bukkit.Bukkit;
import org.bukkit.Color;
import org.bukkit.Particle;
import org.bukkit.World;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitTask;
import org.bukkit.util.Vector;

import java.util.concurrent.ThreadLocalRandom;

public class DisplayUtil {

    private static Vector getRandom() {
        return new Vector(ThreadLocalRandom.current().nextDouble(), ThreadLocalRandom.current().nextDouble(), ThreadLocalRandom.current().nextDouble()).normalize();
    }

    private static void spawn(Vector toShow, Vector offsetFromOrigin, Color color, World world) {
        Bukkit.getScheduler().runTaskLater(Main.getPlugin(Main.class), () -> world.spawnParticle(
                Particle.REDSTONE,
                offsetFromOrigin.clone().add(toShow).toLocation(world),
                0,
                0.001,
                1,
                0,
                1,
                new Particle.DustOptions(color, 1)), 0L);
    }

    private static void showTip(Vector toShow, Vector offsetFromOrigin, Color color, World world) {
        Vector rotCenter = toShow.clone().normalize().getCrossProduct(getRandom()); //could potentially fail if the random vector happens to be in parallel with the toShow vector resulting in a cross product of 0, but that's very unlikely
        Vector begin = toShow.clone().multiply(-0.2).rotateAroundAxis(rotCenter.clone().normalize(), Math.PI/6);
        for(double rot=0; rot<2*Math.PI; rot+=0.2) {
            Vector tipResult = begin.clone().rotateAroundAxis(toShow, rot);
            showVector(tipResult, offsetFromOrigin.clone().add(toShow), 4, color, false, world);
        }
    }

    public static void showVector(Vector toShow, Vector offsetFromOrigin, int amount, Color color, boolean tip, World world) {
        double step = toShow.length()/amount;
        double length = toShow.length();
        for(double d=0; d<=length; d+=step) {
            spawn(toShow.clone().normalize().multiply(d), offsetFromOrigin, color, world);
        }
        if(tip) {
            showTip(toShow, offsetFromOrigin, color, world);
        }
    }

    public static void showBasisVector(Vector offsetFromOrigin, double scale, int amount, boolean tip, World world) {
        showVector(new Vector(1, 0, 0).multiply(scale), offsetFromOrigin, amount, Color.RED, tip, world);
        showVector(new Vector(0, 0, 1).multiply(scale), offsetFromOrigin, amount, Color.BLUE, tip, world);
        showVector(new Vector(0, 1, 0).multiply(scale), offsetFromOrigin, amount, Color.GREEN, tip, world);
    }

    public static void showBasisVectorRepeat(Vector offsetFromOrigin, double scale, int amount, boolean tip, World world, JavaPlugin plugin) {
        Bukkit.getScheduler().runTaskTimer(plugin, () -> showBasisVector(offsetFromOrigin, scale, amount, tip, world), 0L, 5L);
    }

    public static void showPlane(Vector v1, Vector v2, Vector v3, Vector offsetFromOrigin, double range, Color color, World world) {
        for(double s=-range; s<=range; s+=0.5) {
            for(double t=-range; t<=range; t+=0.5) {
                Vector x = v1.clone()
                        .add(v2.clone().multiply(s))
                        .add(v3.clone().multiply(t));
                spawn(x, offsetFromOrigin, color, world);
            }
        }
    }

    public static void showXZPlane(Vector offsetFromOrigin, double range, Color color, World world) {
        showPlane(new Vector(0, 0, 0), new Vector(-1, 0, 1), new Vector(1, 0, -1), offsetFromOrigin, range, color, world);
    }

    public static void showXZPlaneRepeat(Vector offsetFromOrigin, double range, Color color, World world, JavaPlugin plugin) {
        Bukkit.getScheduler().runTaskTimer(plugin, () -> showPlane(new Vector(0, 0, 0), new Vector(-1, 0, 1), new Vector(1, 0, 1), offsetFromOrigin, range, color, world), 0L, 5L);
    }

    public static BukkitTask showVectorRepeat(Vector toShow, Vector offsetFromOrigin, int amount, Color color, boolean tip, World world, JavaPlugin plugin) {
        return Bukkit.getScheduler().runTaskTimer(plugin, () -> showVector(toShow, offsetFromOrigin, amount, color, tip, world), 0L, 5L);
    }
}
