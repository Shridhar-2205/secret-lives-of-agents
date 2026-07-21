# 🗣️ Agents Invent Their Own Language

Two agents start with **no shared words** and play a signaling game. From "did the guess
land?" alone they converge on a private code (~**97%**). Reseed and they invent a *different*
one — arbitrary, but agreed. Remove their memory and it never sets (~56%, chance).

Pure standard library. No GPU, no API key.

```bash
python demo.py
```

```mermaid
flowchart TD
    A["Sender sees a secret object"] --> B["Sender emits one (meaningless) symbol"]
    B --> C["Receiver sees only the symbol, guesses the object"]
    C --> D{"Correct?"}
    D -- yes --> E["Both strengthen that object↔symbol link"]
    D -- no --> A
    E --> G["Links compound → a shared code emerges (~97%)"]
    E --> A
```

📖 Full write-up: [BLOG.md](./BLOG.md)
