Vector playerVec = playerToLookAt.getEyeLocation().toVector().clone();
Vector entityVec = entity.getEyeLocation().toVector();
Vector entityToLookAtVec = playerVec.subtract(entityVec);
Location loc = entity.getLocation().setDirection(entityToLookAtVec);
entity.teleport(loc);