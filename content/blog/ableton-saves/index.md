# How Ableton saves a file

live-vcs turns every save in Ableton into a commit. To do that it has to notice the save, which sounds easy: watch the project folder and react when the .als file changes. The hard part was knowing which filesystem event actually means "the user saved", because Ableton doesn't document how it saves.

## What a save really does

I printed every event a save produced, stepped through it with the debugger, and saved again and again until the pattern was clear. One save is four steps:

```text
1. move     Song.als         ->  Backup/song [timestamp].als
2. create   AbletonTmp-0000
3. write    AbletonTmp-0000
4. rename   AbletonTmp-0000  ->  Song.als
```

Ableton never edits the project file in place. It moves the old one out of the way, writes a new one under a temp name, then renames it into place. Because the original is already gone when the rename happens, the operating system reports it as a move, not a modification.

## Picking the right event

My first attempts relied on a single event type, and none of them caught every save on its own.

```text
on_created   fires only for the temp file, which isn't an .als. Dropped.
on_moved     the rename at the end of the save. This is the real signal.
on_modified  also fires on the project file right after the rename.
             A duplicate of the move, but it covers in-place saves, so I kept it.
```

The duplicate is handled by content, not by event. live-vcs decompresses the .als (it's gzipped XML), hashes the XML, and skips the commit if the hash matches the branch's last commit.

## The Backup folder trap

Step 1 is a move too, and its destination is an .als file. With only an extension check, that move committed the old version of the project on every save. The fix was a second check: the file has to sit in the project folder itself, not in Backup.

## What I'd tell myself if I could go back in time before building this project

Don't trust what you think the program does. Save more than once, print the events, step through with the debugger, and watch how the state changes. 
