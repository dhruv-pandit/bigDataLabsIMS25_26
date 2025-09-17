## Something is wrong in the state of Amianta 🕵️
---

### Phase 0: Server Discovery 🌐
* **Pure Functions**: The `test_password` function is an example of a **pure function**. It takes a port and a password attempt as input and returns a boolean without causing any side effects, making it predictable and reliable.
* **Lazy Evaluation**: The `brute_force_password` function uses a **generator expression** to produce password combinations one at a time. This is a form of lazy evaluation that is far more memory-efficient than generating a complete list of all possible passwords. The `next` function then retrieves the first combination that satisfies the `test_password` predicate, halting the generation process as soon as the correct password is found.

---


### Phase 1: Data Modeling 🧊
The code uses a **dataclass with `frozen=True`** to create an **immutable `Transaction` object**. This is a core functional programming concept because it prevents the object's state from being changed after it's created, which is crucial for avoiding side effects when processing data through the pipeline.

---

### Phase 2: Building the Parsing Pipeline 📝
* **Pure Functions**: Functions like `parse_line` are **pure**; they always return the same output for a given input and have no side effects, which makes the code predictable and easy to test.
* **Higher-Order Functions & Closures**: The `create_field_updater` function is a **higher-order function** that returns another function (a **closure**). This returned function remembers the `key` and `value` from its creation, allowing it to update a dictionary immutably, one field at a time.
* **`reduce`**: The `parse_transaction` function uses `functools.reduce` to sequentially apply the updater functions, building the final `Transaction` object from the raw text data. This is a classic functional pattern for accumulating a result.

---

### Phase 3: Identifying Suspicious Activity 🕵️‍♀️
* **Predicates**: The `is_master_involved` function acts as a **predicate**—a pure function that returns a boolean. It provides a simple, reusable way to filter the data based on a specific condition without modifying the data itself.

---

### Phase 4: The Main Analysis Pipeline 🚀
* **Lazy Evaluation with Generators**: The pipeline leverages **generators** and **generator expressions** to process file paths and transactions lazily. This means data is processed as needed, which is highly **memory-efficient** and scalable.
* **Concurrency with Functional Tools**: `functools.partial` is used to create a new function with fixed arguments (`port` and `password`). This allows `ThreadPoolExecutor.map` to apply this function concurrently to every file path.
* **Chaining Operations**: The final analysis combines several functional components like generators, `filter`, and `sorted` to create a clear, readable data processing **pipeline**. This approach emphasizes what the program is doing rather than how it's doing it, a key characteristic of functional programming.