from pathlib import Path
root=Path('MobCafe-2.0-NeoForge-WIP/src/main/java/com/mobcafe')
p=root/'neoforge/CafeRuntime.java'; s=p.read_text()
s=s.replace('import net.minecraft.world.entity.npc.Villager;\n','').replace('import net.minecraft.world.entity.npc.WanderingTrader;\n','')
s=s.replace('import net.minecraft.world.level.block.state.properties.StairShape;\n','')
s=s.replace('private boolean dirty;', 'private boolean dirty;\n    private final java.util.Set<java.util.UUID> generatedGuests = new java.util.HashSet<>();')
s=s.replace('selectedByPlayer.clear();ticks=0;dirty=false;', 'selectedByPlayer.clear();generatedGuests.clear();ticks=0;dirty=false;')
s=s.replace('player.displayClientMessage(MobCafeMod.msg(message),true)', 'player.sendSystemMessage(MobCafeMod.msg(message))')
s=s.replace('if(!player.addItem(emeralds) && !emeralds.isEmpty())player.drop(emeralds,false);','if(!player.addItem(emeralds) && !emeralds.isEmpty()) {\n                                player.level().addFreshEntity(new net.minecraft.world.entity.item.ItemEntity(player.level(),player.getX(),player.getY(),player.getZ(),emeralds));\n                            }')
s=s.replace('return mob instanceof Villager || mob instanceof WanderingTrader || mob instanceof Witch || mob instanceof Creeper;','return java.util.Set.of("minecraft:villager", "minecraft:wandering_trader", "minecraft:witch", "minecraft:creeper")\n            .contains(EntityType.getKey(mob.getType()).toString());')
s=s.replace('level.getRandom());dirty=true;', 'new java.util.Random(level.getRandom().nextLong()));dirty=true;')
s=s.replace('level.getRandom()).isEmpty()', 'new java.util.Random(level.getRandom().nextLong())).isEmpty()')
s=s.replace('if(mob.getTags().contains("mobcafe_generated"))mob.discard();','if(generatedGuests.remove(mob.getUUID()))mob.discard();')
s=s.replace('EntityType.VILLAGER.create(level,EntitySpawnReason.COMMAND)', 'EntityTypes.VILLAGER.create(level,EntitySpawnReason.COMMAND)')
s=s.replace('mob.moveTo(spawn.x()+0.5,spawn.y(),spawn.z()+0.5,0,0);','mob.setPos(spawn.x()+0.5,spawn.y(),spawn.z()+0.5);')
s=s.replace('mob.addTag("mobcafe_generated");mob.setPersistenceRequired();','generatedGuests.add(mob.getUUID());mob.setPersistenceRequired();')
p.write_text(s)
p=root/'neoforge/CafeEvents.java'; s=p.read_text().replace('import net.neoforged.neoforge.event.level.BlockEvent;', 'import net.neoforged.neoforge.event.level.block.BreakBlockEvent;').replace('BlockEvent.BreakEvent event', 'BreakBlockEvent event');p.write_text(s)
p=root/'neoforge/client/CafeClient.java'; s=p.read_text().replace('mc.screen instanceof','mc.gui.screen() instanceof').replace('mc.setScreen(new CafeScreen(view))','mc.gui.setScreen(new CafeScreen(view))');p.write_text(s)
print('Applied Minecraft 26.3 source fixes')

# Network IDs are namespaced identifiers, not default-namespace paths.
p=root/'neoforge/net/CafeNetwork.java'
s=p.read_text()
s=s.replace('import net.minecraft.network.RegistryFriendlyByteBuf;', 'import net.minecraft.network.RegistryFriendlyByteBuf;\nimport net.minecraft.resources.Identifier;')
s=s.replace('CustomPacketPayload.createType("mobcafe:cafe_view")', 'new CustomPacketPayload.Type<>(Identifier.fromNamespaceAndPath("mobcafe", "cafe_view"))')
s=s.replace('CustomPacketPayload.createType("mobcafe:cafe_action")', 'new CustomPacketPayload.Type<>(Identifier.fromNamespaceAndPath("mobcafe", "cafe_action"))')
assert 'CustomPacketPayload.createType(' not in s
p.write_text(s)
print('Fixed network payload identifiers (mobcafe:cafe_view, mobcafe:cafe_action)')

# The management wand recipe schema changed in Minecraft 26.3.
# Temporarily remove the unverified recipe; wand remains registered and /give works.
recipe=Path('MobCafe-2.0-NeoForge-WIP/src/main/resources/data/mobcafe/recipe/management_wand.json')
if recipe.exists():
    recipe.unlink()
    print('Removed incompatible wand recipe for startup compatibility')
