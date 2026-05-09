import discord
import asyncio
import random
import time
import re

# ================== YOU CAN ADD TOKENS MORE ==================
TOKENS = [
    "ENTER_YOUR_TOKEN_HERE", 
    "ENTER_YOUR_TOKEN_HERE",
]

CHANNEL_ID = ENTER_YOUR_CHANNEL_ID

# Cooldown'lar
HUNT_COOLDOWN       = (14.0, 16.5)
BATTLE_COOLDOWN     = (15.0, 18.0)
PRAY_COOLDOWN       = (300, 310.0)
OWO_SPAM_COOLDOWN   = (20.0, 23.0)

INV_COOLDOWN        = (185, 210.0)
SHOP_SEED_COOLDOWN  = (1180, 1320.0)
RANDOM_TEXT_COOLDOWN = (55, 75.0)
GEM_CHECK_COOLDOWN  = (720, 1080.0)   # ~12-18 m

RANDOM_PHRASES = ["bonecan", "bonekun", "bqne", "bwwne", "yo", "hi", "hello"]

class OwoFarmer(discord.Client):
    def __init__(self, num):
        super().__init__()
        self.num = num
        self.channel = None

        self.next_hunt = 0.0
        self.next_battle = 0.0
        self.next_pray = 0.0
        self.next_owo = 0.0
        self.next_random = 0.0
        self.next_inv = 0.0
        self.next_shop_seed = 0.0
        self.next_pup = 0.0
        self.next_piku = 0.0
        self.next_cash = 0.0
        self.next_gem_check = 0.0

        self.is_real_inventory = False

    async def on_ready(self):
        print(f"[+] {self.user} ({self.num}. hesap) started ")
        self.channel = self.get_channel(CHANNEL_ID)
        if not self.channel:
            print(f"[-] cannot found channel")
            await self.close()
            return

        offset = (self.num - 1) * 4.0
        now = time.monotonic()

        self.next_hunt = now + offset
        self.next_battle = now + offset + 1.2
        self.next_pray = now + offset + 2.5
        self.next_owo = now + offset + 0.8
        self.next_random = now + offset + 5
        self.next_inv = now + offset + 25
        self.next_shop_seed = now + offset + 60
        self.next_pup = now + offset + 120
        self.next_piku = now + offset + 130
        self.next_cash = now + offset + 40
        self.next_gem_check = now + offset + 40

        print(f"[+] {self.num}. hesap → 'winv' yazınca sadece gerçek gemleri kullanacak")
        await self.farmer_loop()

    async def safe_send(self, content: str):
        try:
            await self.channel.send(content)
            print(f"[{self.num}] → {content}")
            return True
        except Exception as e:
            print(f"[{self.num}] Hata: {e}")
            return False

    async def on_message(self, message):
        if message.channel.id != CHANNEL_ID:
            return

        content_lower = message.content.strip().lower()

        if message.author.id == self.user.id and content_lower == "winv":
            print(f"[{self.num}] winv → owo inv atılıyor...")
            await asyncio.sleep(1.2)
            await self.safe_send("owo inv")
            self.is_real_inventory = True
            return

        if not message.author.bot:
            return

        is_owo = "OwO" in str(message.author) or "owo" in str(message.author).lower()

        if is_owo:
            if "inventory" in content_lower:
                self.is_real_inventory = True
                await self.parse_gems_only(message)
            elif "empowered by" in content_lower:
                print(f"[{self.num}] Hunt empowered mesajı (ignore edildi)")
                self.is_real_inventory = False
            elif self.is_real_inventory and "gem" in content_lower:
                await self.parse_gems_only(message)

    async def parse_gems_only(self, message):
        if not self.is_real_inventory:
            return

        full_text = message.content.lower()
        for embed in message.embeds:
            if embed.description:
                full_text += " " + embed.description.lower()
            for field in embed.fields:
                full_text += " " + (field.name or "").lower() + " " + (field.value or "").lower()

        # SADECE 40 ile 80 arası sayıları gem ID olarak al
        gem_ids = re.findall(r'(?:id|kod|#|:)[:\s]*(\d{2,3})', full_text, re.IGNORECASE)
        gem_ids = [id_str for id_str in gem_ids if id_str.isdigit() and 40 <= int(id_str) <= 80]

        if gem_ids:
            gem_ids = sorted(set(gem_ids), key=int, reverse=True)  # En yüksek ID'leri öne al
            use_str = " ".join(gem_ids[:3])  # Maks 3 gem (birer tip)
            print(f"[{self.num}] Gerçek Gem ID'leri bulundu → owo use {use_str}")
            await asyncio.sleep(2.0)
            await self.safe_send(f"owo use {use_str}")
        else:
            print(f"[{self.num}] cannot find gem")

        self.is_real_inventory = False

    async def farmer_loop(self):
        while True:
            now = time.monotonic()

            if now >= self.next_owo:
                await self.safe_send("owo")
                self.next_owo = now + random.uniform(*OWO_SPAM_COOLDOWN)

            if now >= self.next_hunt:
                await self.safe_send("owo hunt")
                self.next_hunt = now + random.uniform(*HUNT_COOLDOWN)
            if now >= self.next_battle:
                await self.safe_send("owo battle")
                self.next_battle = now + random.uniform(*BATTLE_COOLDOWN)
            if now >= self.next_pray:
                await self.safe_send("owo pray <@1418886287884292196>")
                self.next_pray = now + random.uniform(*PRAY_COOLDOWN)

            if now >= self.next_random:
                await self.safe_send(random.choice(RANDOM_PHRASES))
                self.next_random = now + random.uniform(*RANDOM_TEXT_COOLDOWN)

            if now >= self.next_inv:
                await self.safe_send("owo inv")
                await asyncio.sleep(2.0)
                if random.random() < 0.65:
                    await self.safe_send("owo lb all")
                if random.random() < 0.45:
                    await self.safe_send("owo crate all")
                self.next_inv = now + random.uniform(*INV_COOLDOWN)

            if now >= self.next_shop_seed:
                await self.safe_send("owo buy 1")
                self.next_shop_seed = now + random.uniform(*SHOP_SEED_COOLDOWN)

            if now >= self.next_cash:
                await self.safe_send("owo cash")
                self.next_cash = now + random.uniform(*CASH_COOLDOWN)
            if now >= self.next_pup:
                await self.safe_send("owo pup")
                self.next_pup = now + random.uniform(*PUP_COOLDOWN)
            if now >= self.next_piku:
                await self.safe_send("owo piku")
                self.next_piku = now + random.uniform(*PIKU_COOLDOWN)

            if now >= self.next_gem_check:
                print(f"[{self.num}] Otomatik gem kontrolü → owo inv atılıyor")
                await self.safe_send("owo inv")
                self.is_real_inventory = True
                self.next_gem_check = now + random.uniform(*GEM_CHECK_COOLDOWN)

            next_times = [self.next_hunt, self.next_battle, self.next_pray, self.next_owo,
                          self.next_random, self.next_inv, self.next_shop_seed,
                          self.next_pup, self.next_piku, self.next_cash, self.next_gem_check]
            sleep_time = max(0.08, min(next_times) - now)
            await asyncio.sleep(sleep_time)


async def run_account(token, num):
    client = OwoFarmer(num)
    try:
        await client.start(token, reconnect=True)
    except Exception as e:
        print(f"[{num}] Hata: {e}")


async def main():
    print("=== OwO Farmer\n")
    print("")
    print("")
    tasks = [asyncio.create_task(run_account(token, i+1)) for i, token in enumerate(TOKENS)]
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
