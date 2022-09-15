function prepare()
    print("prepare of stress test")
end

function cleanup()
    print("cleanup of stress test")
end

function help()
    print("sysbench stress test; no special command line options available")
end

function thread_init(thread_id)
end

function thread_done(thread_id)
    db_disconnect()
end

function event(thread_id)

    -----------------------------------------------------------------------------------------------------------------------
    -- CONST
    -----------------------------------------------------------------------------------------------------------------------

    local SEARCH_KEY_PH = "^SK"
    local RANDOM_INT_PH = "^RI"

    -----------------------------------------------------------------------------------------------------------------------
    -- PARAMS
    -----------------------------------------------------------------------------------------------------------------------

    local totalRowsOfRecordsInDb = 10000

    local cmdSeed = {
        select = 3000,
        insert = 150,
        delete = 80,
        update = 6770
    }

    selectQueries = {}
    selectQueries["SELECT plantId, userId, seedId, status, growTime, harvestTime, blightTime, rarity, residue, leaf FROM fs2_plant_plants WHERE userId = ^SK;"] = 100
    selectQueries["SELECT userId, finished FROM module_mission_finished WHERE userId = ^SK;"] = 100
    selectQueries["SELECT userId, activityId, decorId, finished, acceptedRewards, expensePoint FROM fs2_activity_party WHERE userId = ^SK;"] = 100
    selectQueries["SELECT userId, customerDefId, level, exp, rewards FROM fs2_customer_friendship WHERE userId = ^SK;"] = 100
    selectQueries["SELECT userId, missionId, progress, acceptTime, expireTime FROM module_mission_in_progress WHERE userId = ^SK;"] = 100
    selectQueries["SELECT userId, activityId, collect FROM fs2_activity_collect WHERE userId = ^SK;"] = 100
    selectQueries["SELECT userId, gridId, layer1Type, layer1, layer2Type, layer2, layer3Type, layer3 FROM fs2_grounds WHERE userId = ^SK;"] = 100
    selectQueries["SELECT decorId, decorDefId, userId, orient, cooldown, buildId, isUpgrade, effectCountLeft, resourceCountLeft, requestAccepted, output, withActivityOutput, freeMode FROM fs2_decoration WHERE userId = ^SK;"] = 100
    selectQueries["SELECT requestId, receiverId, senderId, helpId, type, info, time, expire, platformRequestId FROM fs2_social_request WHERE receiverId = ^SK;"] = 100
    selectQueries["SELECT userId, customerDefIds FROM fs2_customer_event WHERE userId = ^SK;"] = 100


    insertQueries = {}
    insertQueries["insert into `fv_dev`.`fs2_pet` ( `status`, `userId`, `fodderId`, `feedUpCount`, `feedUpTime`, `petDefId`) values ( '0', '89', '780003', '1', '1438223373', '900001');"] = 100
    insertQueries["insert into fs2_plant_plants (userId,seedId,status,growTime,harvestTime,blightTime,rarity,residue,leaf,soilId,soilType,soilCount,harvestCount,wood,requestAccepted,withActivityOutput) values ('57332', '110001', '1', '1428746759', '1428746819', '1429005959', '0', '0', '0', '0', '0', '0', '0', '0', null, null); "]=100


    updateQueries = {}
    updateQueries["UPDATE module_achievement_in_progress SET progress = '[3333333333,44444,5555555555555,7777777777777777777777,^RI,111111111111,22222222222222222222,999999999999999999999999,00000000]' WHERE userId = ^SK;"] = 1000
    updateQueries["UPDATE module_profile_infos SET info = ^RI, time = ^RI WHERE userId = ^SK;"] = 700
    updateQueries["UPDATE fs2_plant_plants SET seedId = ^RI, status = ^RI, growTime = ^RI, harvestTime = ^RI, blightTime = ^RI, rarity = ^RI, leaf = ^RI, residue = ^RI WHERE plantId = ^SK;"] = 700
    updateQueries["UPDATE module_profile SET  exp = exp + 1 WHERE userId = ^SK;"] = 500
    updateQueries["UPDATE module_mission_in_progress SET progress = '[3333333333,44444,5555555555555,7777777777777777777777,^RI,111111111111,22222222222222222222,999999999999999999999999,00000000]', acceptTime = ^RI WHERE userId = ^SK;"] = 300
    updateQueries["UPDATE module_item SET  updateTime = ^RI WHERE userId = ^SK;"] = 700
    updateQueries["UPDATE fs2_plant_seeds SET exp = ^RI WHERE userId = ^SK;"] = 100
    updateQueries["UPDATE fs2_social_feed SET helpId = ^RI, status = ^RI WHERE userId = ^SK;"] = 100
    updateQueries["UPDATE fs2_pet SET feedUpCount = ^RI, feedUpTime = ^RI, status = ^RI WHERE petId = ^SK;"] = 100
    updateQueries["UPDATE fs2_customer SET exp = ^RI, status = ^RI WHERE userId = ^SK;"] = 50
    updateQueries["UPDATE fs2_customer_town SET missionId = ^RI, leaveTime = ^RI WHERE customerId = ^SK;"] = 300
    updateQueries["UPDATE fs2_activity SET count = ^RI, status = ^RI WHERE userId = ^SK;"] = 100

    deleteQueries = {}
    deleteQueries["delete from fs2_plant_plants where userId=57332 limit 1;"] = 500
    deleteQueries["delete from fs2_pet where userId=89 limit 1;"] =500

    -----------------------------------------------------------------------------------------------------------------------
    -- LIB
    -----------------------------------------------------------------------------------------------------------------------

    local function randItem(seedTable)
        local result = 0

        local seedSum = 0
        for key, value in pairs(seedTable) do
            seedSum = seedSum + value
        end

        local randSeed = sb_rand(1, seedSum)

        local sum = 0

        for cmdType, prob in pairs(seedTable) do
            sum = sum + prob
            if randSeed <= sum then
                result = cmdType
            break end
        end



        return result
    end

    local function processSleep()
        os.execute("sleep 0.01") -- 10ms
    end

    -----------------------------------------------------------------------------------------------------------------------
    -- EXEC
    -----------------------------------------------------------------------------------------------------------------------

    local cmdType = randItem(cmdSeed)
    --print(cmdType)

    --if cmdType == "insert" or cmdType == "delete" then
    --    cmdType = "update"
    --end

    local querySeed = _G[cmdType .. "Queries"]

    local sql = randItem(querySeed)
    --print(sql)

    if cmdType == "update" then
        sql = sql:gsub("%^RI", sb_rand(1, totalRowsOfRecordsInDb))
    end
    sql = sql:gsub("%^SK", sb_rand(1, totalRowsOfRecordsInDb))

    --processSleep() -- let the lua script sleep to make qps lower for testing, if necessary

    db_query(sql)

end