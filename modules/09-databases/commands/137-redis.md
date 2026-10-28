# Lesson 137 — Redis: Practice Reference

Use a disposable local Redis instance. These examples create keys prefixed with `demo:` and should not be run against production.

## Strings and TTL
```redis
SET demo:product:42 "Wireless Mouse"
GET demo:product:42
SET demo:session:7 "active" EX 30
TTL demo:session:7
```

## Hashes, sets, and sorted sets
```redis
HSET demo:user:7 name "Asha" plan "premium"
HGETALL demo:user:7
SADD demo:event:42 user:7 user:8
SISMEMBER demo:event:42 user:7
ZADD demo:leaderboard 950 player:7
ZREVRANGE demo:leaderboard 0 -1 WITHSCORES
```

## Counter and expiration experiment
```redis
INCR demo:page:42:views
SET demo:short-lived "hello" EX 5
TTL demo:short-lived
GET demo:short-lived
```
Wait several seconds and read the short-lived key again. It should eventually return nil.

## Cleanup
```redis
DEL demo:product:42 demo:session:7 demo:user:7
DEL demo:event:42 demo:leaderboard demo:short-lived demo:page:42:views
```

## Investigation checklist
- Check cache hit/miss rate and Redis latency.
- Monitor memory usage, evictions, and rejected writes.
- Check TTLs and invalidation behavior for stale values.
- Consider stampedes when many requests load the same missing key.
- Ensure Redis outages cannot trigger uncontrolled load on the source database.
- Review persistence, backups, replication, and recovery against data-loss requirements.

## Safety
- Verify the Redis endpoint before running commands.
- Use a disposable local instance or approved development environment.
- Only delete the explicitly named `demo:` keys created for this exercise.
- Never expose credentials or sensitive cached data in source control or logs.
