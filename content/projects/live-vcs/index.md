# live-vcs

Git-style version control for Ableton Live projects: saves become commits you can branch from and load back. My MSc dissertation. [Code on GitHub](https://github.com/amelfia/live-vcs)

## Why I built it

When I'm working on a track I want to try ideas without losing the version that already works. In Ableton that meant Save As copies piling up in the project folder, and finding an old idea meant opening them one by one. I wanted something closer to Git: every save recorded with a short note, branches for trying things, and a way to go back.

## How it works

- Run live-vcs in a terminal next to Ableton and point it at your project folder.
- Every time you save, it asks for a short note and stores a copy of the .als as a commit.
- Saving without changes doesn't create a commit, because it compares a hash of the decompressed XML with the last commit.
- `branch` starts a new branch from the current commit, `switch` moves between branches, and `graph` draws the history in the terminal.
- `load` takes a commit's hash, switches to its branch, copies that version over the project file and reopens it in Ableton.

```text
* d4a2f81 Main synth melody sketch
|
* 1a9b2c3 synth double
|\
| * 7f2b1a4 Add vocal chop processing (vocal-chop)
| |
| * 3c8e190 Sidechain sub bass to kick
|/
|
* 0f3e9a2 init
```

## Decisions

- No merge. Two versions of a synth lead aren't competing edits to the same text, they're different ideas, so merging them doesn't mean anything musically.
- It reacts to filesystem events instead of checking the folder every few seconds, so it does nothing until you actually save.
- It asks for a note on every save. That's a small interruption, but it's the price of never having to stop and Save As by hand.

## What was hard

Working out what a save actually is. Ableton doesn't document it, so I had to watch the events myself: [How Ableton saves a file](/blog/ableton-saves).

The other hard part was two threads sharing one terminal. The watcher runs in the background and needs to ask for a note, while the main loop is waiting for your next command. A lock makes sure only one of them reads from the terminal at a time, an event flag pauses commands while a save is being handled, and the main loop polls the terminal with a short timeout instead of blocking.

## Limits

- macOS only for now.
- One .als per project folder, so `load` knows which file to overwrite.

## Next

A Max for Live device, so the note and the graph live inside Ableton instead of a terminal.
