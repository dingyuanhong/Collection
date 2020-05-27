-- 去重

db.szse_company.aggregate([
    {
        $group:{_id:{stodkId:'$zqdm'},count:{$sum:1},dups:{$addToSet:'$_id'}}
    },
    {
        $match:{count:{$gt:1}}
    }
]).forEach(function(it){
    it.dups.shift();
    db.szse_company.remove({_id: {$in: it.dups}});
});