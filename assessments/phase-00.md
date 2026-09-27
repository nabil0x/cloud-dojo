# Self-check — Phase 0: Docker Foundations (no XP, honor system)

Score 7+ before the boss fight.

**1. Explain image vs container in one sentence each.**
<details><summary>Show answer</summary>
An image is a frozen, read-only template: stacked filesystem layers plus metadata. A container is a running instance of that image, with one thin writable layer on top and its own process space and resource limits.
</details>

**2. You delete a container. Is the image gone too? Why do you still need a volume for data?**
<details><summary>Show answer</summary>
No. Deleting a container removes only its writable layer; the image is untouched. Anything written inside the container lived in that writable layer, so it dies with the container. Data that must survive needs a named volume, which lives outside any container's lifecycle.
</details>

**3. Predict the output: you run a container, edit a file inside it with `docker exec`, then `docker rm` it and start a new one. Is your edit there?**
<details><summary>Show answer</summary>
No. The edit lived in the writable layer and vanished with `rm`. A fresh container starts from the image layers, which never saw your change.
</details>

**4. Why does a one-line code edit sometimes rebuild almost the whole image, and how do you stop that?**
<details><summary>Show answer</summary>
Because Docker rebuilds every layer from the first changed instruction onward. If `COPY . .` sits near the top, editing any file invalidates that layer and all layers after it. Put slow-changing steps first (`FROM`, dependency installs) and `COPY` your app code last, so only the final layers rebuild.
</details>

**5. What breaks if your Dockerfile does `COPY . .` before `RUN pip install -r requirements.txt`?**
<details><summary>Show answer</summary>
Every source-code edit invalidates the `COPY` layer, so `pip install` reruns on the next build and re-downloads every dependency. The cache is useless for the slow step. Copy `requirements.txt` and install first, then copy the rest of the code.
</details>

**6. In `-p 8080:80`, which side is the host and which is the container? Can two containers both listen on port 80?**
<details><summary>Show answer</summary>
Host port 8080 forwards to container port 80. Yes, two containers can both listen on 80 internally, as long as their host ports differ (for example `-p 8080:80` and `-p 8081:80`).
</details>

**7. What breaks if you try to reach nginx with `-p 8080:8080`?**
<details><summary>Show answer</summary>
Nothing is listening on port 8080 inside the nginx image; nginx listens on 80. The mapping points at an empty port, so the request fails. The correct mapping is `-p 8080:80`.
</details>

**8. Does `EXPOSE 8080` publish the port? Spot the trap.**
<details><summary>Show answer</summary>
No. `EXPOSE` is documentation and default metadata; it does not publish anything. Only `-p host:container` at run time actually maps the port to the host.
</details>

**9. You rebuild, but the page still shows old content. Name the two most likely causes.**
<details><summary>Show answer</summary>
The build reused a cached layer because the input did not change from Docker's view, or you rebuilt a different tag than the one you ran. Check with `docker image history` and confirm the tag you run matches the tag you built.
</details>

**10. Boss setup: run the emulator as a named container on host port 4570. What is the port flag, and why is 4566 now empty?**
<details><summary>Show answer</summary>
The flag is `-p 4570:4566` (host 4570 to container 4566). Port 4566 is empty because nothing is listening on that host port anymore; the old container was stopped and removed, and the new mapping only exposes the host side as 4570.
</details>

**11. Why does `sudo docker ...` on every command signal a problem, and what is the fix?**
<details><summary>Show answer</summary>
It means your user is not in the `docker` group, so the daemon socket is not accessible without root. Add your user to the `docker` group (then re-login) so plain `docker` works.
</details>
