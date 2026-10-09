# Backend tests

```sh
./backend/app/tests/run_in_docker.sh            # full suite
./backend/app/tests/run_in_docker.sh -k friends # subset
./backend/app/tests/run_in_docker.sh --cov=backend_app --cov-report=term
```

The script starts a throwaway Postgres, Redis and runner container on their own
network, runs the Alembic migrations, then runs pytest. Your running stack,
its database and `shared/profile_pictures` are never touched.

Tests run inside the backend image because the app hardcodes container paths
(`/app/src/...`) and hostnames (`postgres`, `redis`).

| File | Covers |
| --- | --- |
| `test_auth.py` | signup, login, `/me`, JWT edge cases, logout, RGPD deletion, 42 OAuth |
| `test_friends.py` | friend request lifecycle, authorization, races, privacy |
| `test_user.py` | username change, picture upload/removal, static file serving |
| `test_chat.py` | chat send/list, chatbot |
| `test_game_data.py` | items/traits/units/augments with faked upstream, leaderboard, patch notes, search |
| `test_stats.py` | `/stats/*` incl. upstream failures and event-loop blocking |
| `test_core.py` | helpers, password hashing, rate limiting, websocket manager |
| `test_fuzz.py` | Hypothesis fuzzing of every route: no input may produce a 5xx |

All outbound network calls are blocked (they fail as "connection refused"), so
tests are deterministic and also prove the app degrades gracefully offline.

Tests describe the *correct* behaviour: a failing test is a bug in the app,
not in the test.
