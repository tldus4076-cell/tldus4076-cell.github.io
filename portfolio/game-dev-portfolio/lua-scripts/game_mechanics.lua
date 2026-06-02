-- ============================================
-- 게임 메커닉스 스크립트 (Lua)
-- 공고 요건: Lua 언어 사용 경험
-- 연구대: 게임 엔지나 서버의 로직 스크립트로 활용
-- ============================================

-- --------------------------------------------
-- 1. 아이템 데이터 테이블 (Item Database)
-- --------------------------------------------
local ItemDB = {
    [1001] = { name = "철검",      type = "weapon",  atk = 10, price = 500 },
    [1002] = { name = "방패",      type = "armor",   def = 5,  price = 300 },
    [1003] = { name = "흘런 포션", type = "potion",  hp = 50,  price = 100 },
    [1004] = { name = "매직 주문서",type = "scroll",  mp = 30,  price = 150 }
}

-- --------------------------------------------
-- 2. 유저 데이터 (User Data)
-- --------------------------------------------
local Player = {
    name = "용사",
    level = 1,
    hp = 100,
    maxHp = 100,
    mp = 50,
    maxMp = 50,
    exp = 0,
    gold = 1000,
    inventory = {},
    equipped = { weapon = nil, armor = nil }
}

-- --------------------------------------------
-- 3. 함수: 아이템 획득
-- --------------------------------------------
function AddItem(player, itemId, count)
    count = count or 1
    local item = ItemDB[itemId]
    if not item then
        print("[오류] 존재하지 않는 아이템 ID: " .. itemId)
        return false
    end
    
    -- 인벤토리에 추가 (스택음료)
    player.inventory[itemId] = (player.inventory[itemId] or 0) + count
    print(string.format("[획득] %s x%d 획득!", item.name, count))
    return true
end

-- --------------------------------------------
-- 4. 함수: 아이템 사용 (포션 먹기)
-- --------------------------------------------
function UseItem(player, itemId)
    local item = ItemDB[itemId]
    if not item then return false end
    
    if (player.inventory[itemId] or 0) <= 0 then
        print("아이템이 없습니다!")
        return false
    end
    
    if item.type == "potion" then
        local healAmount = math.min(item.hp, player.maxHp - player.hp)
        player.hp = player.hp + healAmount
        player.inventory[itemId] = player.inventory[itemId] - 1
        print(string.format("%s 사용! HP +%d (현재 HP: %d/%d)",
            item.name, healAmount, player.hp, player.maxHp))
    else
        print("이 아이템은 사용할 수 없습니다.")
    end
    return true
end

-- --------------------------------------------
-- 5. 함수: 전투 데미지 계산
-- --------------------------------------------
function CalculateDamage(attacker, defender, isSkill)
    local baseDmg = attacker.atk or 10
    local def = defender.def or 0
    local multiplier = isSkill and 1.5 or 1.0
    
    local damage = math.max(1, math.floor((baseDmg * multiplier) - def * 0.5))
    return damage
end

-- --------------------------------------------
-- 6. 함수: 경험치 계산 (Level Up System)
-- --------------------------------------------
function GainExp(player, amount)
    player.exp = player.exp + amount
    local required = player.level * 100
    
    while player.exp >= required do
        player.exp = player.exp - required
        player.level = player.level + 1
        player.maxHp = player.maxHp + 20
        player.hp = player.maxHp
        player.maxMp = player.maxMp + 10
        player.mp = player.maxMp
        print(string.format("✨ 레빌업! Lv.%d 도당! (챔/마나 전부 회복)", player.level))
        required = player.level * 100
    end
    
    print(string.format("경험치 +%d (당장 업: %d/%d)", amount, player.exp, required))
end

-- --------------------------------------------
-- 7. 함수: 인벤토리 출력
-- --------------------------------------------
function ShowInventory(player)
    print("\n=== 인벤토리 ===")
    if not next(player.inventory) then
        print("(비어 있음)")
        return
    end
    
    for itemId, count in pairs(player.inventory) do
        local item = ItemDB[itemId]
        if item then
            print(string.format("  - %s x%d (%s)", item.name, count, item.type))
        end
    end
end

-- --------------------------------------------
-- 8. 함수: 플레이어 정보 출력
-- --------------------------------------------
function ShowStatus(player)
    print("\n=== 용사 정보 ===")
    print(string.format("  이름: %s | Lv.%d", player.name, player.level))
    print(string.format("  HP: %d/%d | MP: %d/%d", player.hp, player.maxHp, player.mp, player.maxMp))
    print(string.format("  EXP: %d | 곰드: %d G", player.exp, player.gold))
end

-- ============================================
-- 데모 실행
-- ============================================
print("🎮 Lua 게임 메커닉스 데모 시작\n")

ShowStatus(Player)

-- 아이템 획득
AddItem(Player, 1003, 3)  -- 포션 3개
AddItem(Player, 1001, 1)  -- 철검 1개

-- 데미지 시뮬레이션
local enemy = { name = "슬라임", atk = 8, def = 2, hp = 30 }
local dmg = CalculateDamage({ atk = 12 }, enemy, false)
print(string.format("\n⚔️ 슬라임에게 공격! 데미지: %d", dmg))

-- 포션 사용
UseItem(Player, 1003)

-- 경험치 획득
GainExp(Player, 250)

-- 인벤토리 확인
ShowInventory(Player)
ShowStatus(Player)

print("\n✅ 데모 종료!")
