# Self-check — Phase 2: Docker Compose (no XP, honor system)

Score 7+ before the boss fight.

**1. What is Compose, and what is it not?**
<details><summary>Show answer</summary>
Compose is a declarative multi-container dev environment: one YAML file describes services, networks, volumes, and env, and `docker compose up` builds the whole world while `down` removes it. It is not production orchestration; that is ECS or Kubernetes. Think "my laptop's data center," version-controlled.
</details>

**2. What is the difference between `build: ./app` and `image:` in a service?**
<details><summary>Show answer</summary>
`build` compiles a Dockerfile locally into an image. `image` pulls a prebuilt image from a registry. Our stack uses both: the app builds, the emulator pulls.
</details>

**3. `depends_on: [emulator]` starts the emulator first. What breaks, and why?**
<details><summary>Show answer</summary>
`depends_on` orders startup but does not wait for readiness. The emulator container may be running but not yet accepting requests, so the app can fail on its first call. Real stacks add healthchecks and wait for healthy; our stack lets you observe the race.
</details>

**4. Why must the app use `http://emulator:4566` instead of `http://localhost:4566`?**
<details><summary>Show answer</summary>
Inside the app container, `localhost` is the app itself. The emulator lives at its service name on the Compose network, so `http://emulator:4566` resolves correctly. Always ask "localhost from whose perspective?"
</details>

**5. You edit `app/app.py`, run `docker compose up -d`, and nothing changes. What went wrong?**
<details><summary>Show answer</summary>
You forgot `--build`. Without it Compose reuses the old image, so your edit never enters the container. Use `docker compose up -d --build`.
</details>

**6. What breaks if you run `docker compose down` and expect seed data to still be there, but actually ran `down -v`?**
<details><summary>Show answer</summary>
`down -v` deletes named volumes, so the emulator's data is wiped. `down` alone keeps volumes. After `down -v` you must `up` again and re-run the seed script, because the bucket, queue, and table are gone.
</details>

**7. In Compose `ports: ["8080:8080"]`, which side is which?**
<details><summary>Show answer</summary>
Same semantics as `docker run -p`: host port on the left, container port on the right. `8080:8080` maps host 8080 to container 8080. A mismatch (like host 8080 to container 80) means you curl `localhost:8080` and reach container port 80.
</details>

**8. How does the app reach the emulator by name without any DNS setup?**
<details><summary>Show answer</summary>
Compose creates a network automatically and joins every service to it. On that network each service gets DNS equal to its service name, so `emulator` resolves to the emulator container.
</details>

**9. `shared/seed.sh` runs from the host. Which endpoint does it use, and why?**
<details><summary>Show answer</summary>
It uses `localhost:4566`, because from the host the emulator is published on the host port. Host reaches `localhost`, containers reach the service name.
</details>

**10. You swap the emulator image from MiniStack to LocalStack (plus a token). What changes in the app?**
<details><summary>Show answer</summary>
Nothing. Only the `image:` line (and the auth token) changes. Same port, same endpoint pattern, app untouched. Portable interfaces are the point of the exercise.
</details>

**11. Why is `docker compose logs -f app` better than reading raw container logs for debugging?**
<details><summary>Show answer</summary>
It scopes the output to one service instead of the firehose from every container, so you see just the app's logs as they stream.
</details>

**12. Boss run: `down -v` then `up -d --build`, no seed. `curl localhost:8080/s3` returns an empty list, not an error. Why?**
<details><summary>Show answer</summary>
The stack is healthy, but `down -v` deleted the volume and the fresh emulator has no bucket yet. The app asks S3 for objects and gets an empty result, not a failure. Re-run the seed script to recreate the bucket, then `/s3` lists it.
</details>
