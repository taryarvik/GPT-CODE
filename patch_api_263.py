from pathlib import Path

root = Path("src/main/java/com/mobcafeui")

def change(path, transforms):
    file = root / path
    text = file.read_text(encoding="utf-8")
    for before, after in transforms:
        if before not in text:
            raise RuntimeError(f"Expected expression missing in {file}: {before}")
        text = text.replace(before, after)
    file.write_text(text, encoding="utf-8")

change("menu/RestaurantMenu.java", [
    ("player.serverLevel()", "((net.minecraft.server.level.ServerLevel) player.level())"),
    ("player.getScoreboard()", "player.level().getScoreboard()"),
])
change("menu/CatalogOpener.java", [
    ("player.getScoreboard()", "player.level().getScoreboard()"),
    ("player.displayClientMessage(", "player.sendSystemMessage("),
])
change("order/LiteOrderBridge.java", [
    ("import net.minecraft.world.entity.EntityType;", "import net.minecraft.world.entity.EntityTypes;"),
    ("EntityType.ITEM_DISPLAY", "EntityTypes.ITEM_DISPLAY"),
    ("display.setItemStack(product.item().copyWithCount(1));", "display.getSlot(0).set(product.item().copyWithCount(1));"),
    ("        display.setItemTransform(ItemDisplayContext.FIXED);\n", ""),
    ("getTags()", "entityTags()"),
    ("player.serverLevel()", "((net.minecraft.server.level.ServerLevel) player.level())"),
    ("player.displayClientMessage(", "player.sendSystemMessage("),
])
print("Patched Minecraft 26.3 method names")
