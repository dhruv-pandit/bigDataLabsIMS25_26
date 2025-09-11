
## 4) Spaces in filenames

**Student:** Create a file literally named `team list.txt` in `~/bda/session2_rev` and add one line: `Q1`. Then display its contents.

**Instructor key:**
`cd ~/bda/session2_rev`
`echo "Q1" > "team list.txt"`
`cat "team list.txt"`
Common mistake: forgetting quotes.

---

## 5) Quick reading checks

**Student:** Without opening an editor:

* Show the first **two** lines of `data/roster.txt`.
* Show the **last** line.
* Show the **line count** only.

**Instructor key:**
`head -n 2 data/roster.txt`
`tail -n 1 data/roster.txt`
`wc -l data/roster.txt`

---

## 6) “Why isn’t `pwd` what I expect?”

**Student:** Run the following exactly:

```bash
cd ~/bda/session2_rev
cd data
cd ..
cd ../..
pwd
```

**Question:** Why are you **not** in `~/bda/session2_rev` anymore?
**Task:** Get back to `~/bda/session2_rev` in one command.

**Instructor key:** `cd ../..` climbed two levels (to `~/bda`). Then another `..` went above `~/bda` if structure differs; after the sequence shown you land in `~/`. To return in one step: `cd ~/bda/session2_rev` or `cd -` if appropriate.

---

## 7) Mini “spot the bug” (absolute vs relative)

**Student:** You are in `~/bda/session2_rev`. Which command correctly saves the **current absolute path** into `whereami.txt` **inside** the `data/` folder?

A) `pwd > whereami.txt`
B) `pwd > ~/bda/session2_rev/data/whereami.txt`
C) `pwd > /data/whereami.txt`
D) `pwd > ./data whereami.txt`

**Instructor key:** **B** is correct.
A writes to the current directory, not `data/`.
C targets `/data` at the filesystem root (likely wrong).
D is parsed as two words; missing the slash.

---

## 8) Tiny consolidation task

**Student:** From `~/bda/session2_rev`, create a short report (no pipes):

1. Start `report.txt` with your absolute path.
2. Append a header line `--- ROSTER TOP ---`.
3. Append the **first three** lines of `data/roster.txt`.
4. Append a header `--- COUNT ---` and then append the **line count**.

**Instructor key:**

```bash
pwd > report.txt
echo "--- ROSTER TOP ---" >> report.txt
head -n 3 data/roster.txt >> report.txt
echo "--- COUNT ---" >> report.txt
wc -l data/roster.txt >> report.txt
```

Then `less report.txt`.

---

### Optional 60-second debrief prompts

* What single command returns you to the previous directory? (**`cd -`**)
* Why did `echo "X" > run.log` create a file in the **wrong folder** earlier? (Because redirection writes to the **current** directory unless you provide a path.)
* How do you make a command **not** depend on where you are? (Use an **absolute** path like `~/bda/...`)

---

If you want these as a **printable handout** or a **single slide with steps hidden behind fragments**, I can format it either way.
